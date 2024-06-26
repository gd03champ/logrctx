from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager

from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

def rag_chat_init(dir_path, filename):

    console = Console()
    progress = Progress(console=console)
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    # Invoke chain with RAG context
    llm = Ollama(model="phi3", callbacks=callback_manager)
    ## Load log content
    console.print("Loading logs...")
    loader = DirectoryLoader(
        dir_path, 
        glob=filename , 
        #show_progress=True,
        use_multithreading=True
        )
    with progress:
        task = progress.add_task("[cyan]Loading logs...", total=1)
        docs = loader.load()
        progress.update(task, completed=1)
    console.print(f"doc length: {len(docs)}")

    ## Vector store things
    console.print("Creating vector store...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text", show_progress=True)
    text_splitter = RecursiveCharacterTextSplitter()
    split_documents = text_splitter.split_documents(docs)
    vector_store = FAISS.from_documents(split_documents, embeddings)

    ## Prompt construction
    prompt = ChatPromptTemplate.from_template(
        """
<|system|>

You are a log expert assistant that answers questions about logs.

You are given some extracted parts from logs along with a question.

If you don't know the answer, just say "I don't know." Don't try to make up an answer.

Don't provide any information that is not directly relevant to the question. Like debugging information , reasonong, or any extra context unless as. Just provide what's asked from given context.
Make sure to talk only relevant information to keep the output as short and to the point as possible while no leaving any important information out. 

Use only the following pieces of context to answer the question at the end.

<|end|>

<|user|>

Context: {context}

Question: {input}

<|end|>

<|assistant|>
        """
    )

    ## Retrieve context from vector store
    console.print("Retrieving context...")
    docs_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_store.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, docs_chain)

    ## Winner winner chicken dinner
    console.print("Invoking chain...")
    while True:
        query = Prompt.ask("Query: ")
        response = retrieval_chain.invoke({"input": query})
        console.print(response["answer"])

if __name__ == "__main__":
    rag_chat_init(
        dir_path = "../logs",
        filename = "reduced_sample.log"
    )