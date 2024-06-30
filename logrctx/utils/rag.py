import os
import pickle
from langchain_community.llms import Ollama
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm

from concurrent.futures import ThreadPoolExecutor

home_dir = os.path.expanduser('~')

# Initialize the console for rich output
console = Console()

def load_logs(dir_path, filename):
    """Load log files from the specified directory."""
    try:
        #if cache exists, cache will be loaded in create_vector_store, no need to load logs again
        cache_dir = f"{home_dir}/.logrctx/cache"
        if os.path.exists(cache_dir):
            console.print("[yellow]Cached vector db found...")
            return "cache detected"

        loader = DirectoryLoader(
            dir_path,
            glob=filename,
            use_multithreading=True
        )
        with console.status("[cyan]Loading log files..."):
            docs = loader.load()
        console.print(f"Total log files loaded: {len(docs)}")
        return docs
    except Exception as e:
        console.print(f"[red]Error loading log files: {e}")
        return []

def create_vector_store(docs, embedding_model="nomic-embed-text"):
    """Create a vector store from documents using the specified embedding model."""
    try:
        # create cache directory if not exists
        cache_dir = f"{home_dir}/.logrctx/cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        cache_path = f"{home_dir}/.logrctx/cache/vector_store_cache.pkl"
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                vector_store = pickle.load(f)
            console.print("[green]Loaded vector store from cache.")
            return vector_store

        with console.status("[cyan]Creating vector store..."):
            embeddings = OllamaEmbeddings(model=embedding_model)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
            split_documents = text_splitter.split_documents(docs)
            vector_store = FAISS.from_documents(split_documents, embeddings)

        with open(cache_path, 'wb') as f:
            pickle.dump(vector_store, f)
        console.print("[green]Vector store created and cached.")
        return vector_store
    except Exception as e:
        console.print(f"[red]Error creating vector store: {e}")
        return None

def setup_llm(callback_manager):
    """Set up the language model with specified callbacks."""
    try:
        llm = Ollama(model="phi3", callbacks=callback_manager)
        return llm
    except Exception as e:
        console.print(f"[red]Error setting up language model: {e}")
        return None

def construct_prompt():
    """Construct the chat prompt template."""
    prompt = ChatPromptTemplate.from_template(
        """
        You are an intelligent RAG system named logrctx for log analysis and given some extracted parts from logs as context through RAG system along with a question to answer.
        If you don't know the answer, just say "I don't know." Don't try to make up an answer.

        Don't provide any information that is not directly relevant to the question. Like debugging information, reasoning, recommendation, or any extra context unless asked.
        Just provide what's asked from the given context by summarizing the context. Don't demand extra context.

        Prefer to use markdown format wherever possible for visually appealing output and use time from the logs in your response if needed for concise response.
        Keep the response as short and to the point as possible while not leaving any important information out.

        Use only the following pieces of context to answer the question at the end.

        Context: {context}

        Question: {input}
        """
    )
    return prompt

def custom_retrieval_chain(vector_store, docs_chain, query):
    """Custom retrieval and generation process."""
    with console.status("[cyan]Retrieving relevant logs..."):
        docs = vector_store.similarity_search(query, k=5)
        console.print("[green]Context mapped successfully.")
        console.print("Retrieved docs 👇")
        for doc in docs:
            console.print(Panel.fit(f"[cyan]{doc.metadata['source']}[/cyan]\n{doc.page_content}"))
    
    assuring = Confirm.ask("[bold green]Analyze this context with logrctx ai?[/bold green]")
    if not assuring:
        return "# Skipped AI context analysis"

    console.print("[cyan]Generating response...")
    response = docs_chain.invoke({"context": docs, "input": query})
    return response

def main(dir_path, filename):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = setup_llm(callback_manager)
    if not llm:
        return

    docs = load_logs(dir_path, filename)
    if not docs:
        return

    vector_store = create_vector_store(docs)
    if not vector_store:
        return

    prompt = construct_prompt()
    docs_chain = create_stuff_documents_chain(llm, prompt)

    console.print("\n[bold cyan]Invoking chain...")

    while True:
        query = Prompt.ask("[bold green]Prompt[/bold green]")
        if query.lower() in ["exit", "quit"]:
            break

        response = custom_retrieval_chain(vector_store, docs_chain, query)
        console.print("\n")
        console.print(Panel.fit("[bold green] logrctx AI 🧠 [/bold green]"))
        console.print(Panel.fit((Markdown(f"{response}"))))

if __name__ == "__main__":
    home_dir = os.path.expanduser('~')
    dir_path = f"{home_dir}/.logrctx/logs/"
    filename = f"reduced_raw.log"
    main(dir_path, filename)
