import typer
from rich.console import Console
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
import time
import os

from logrctx.utils.string_matching import reduce as reduce_utility
from logrctx.utils.rag import main as rag_chat_init

app = typer.Typer()
console = Console()

home_dir = os.path.expanduser('~')

# main utility functions

## loki logs retrieval
def loki(support: str = None):
    if support is None:
        console.print("Please provide query to retrieve logs from loki", style="bold red")
        exit()
        
    console.print("Skipping loki logs retrieval with simulated logs...", style="bold yellow")
    with console.status("Retrieving logs..."):
        time.sleep(1)
        #get_logs(support)
    os.system(f"touch {home_dir}/.logrctx/logs/raw.log")
    console.print(f"Logs retrieved successfully! Stored to [bold]{home_dir}/.logrctx/logs/raw.log[/bold]", style="bold green")

## reduce logs
def reduce():

    with console.status("Clearing cache..."):
    # check if cache directory exists and delete
        if os.path.exists(f"{home_dir}/.logrctx/cache"):
            os.system(f"rm -rf {home_dir}/.logrctx/cache")

    # string matching reduce
    with console.status("Reducing logs..."):
        time.sleep(0)
        reduce_utility(
            input_file = f'{home_dir}/.logrctx/logs/raw.log',
            output_file = f'{home_dir}/.logrctx/logs/reduced_raw.log'
            )
    console.print(f"Logs reduced successfully! Stored to {home_dir}/.logrctx/logs/reduced_raw.log", style="bold green")

    to_view = Confirm.ask("Do you want to view the reduced logs?")
    if to_view:
        # load logs from file
        syntax = Syntax.from_path(f"{home_dir}/.logrctx/logs/reduced_raw.log", theme="monokai", line_numbers=True, word_wrap=True)
        print("\n")
        with console.pager():
            console.print(Panel.fit(syntax))
        console.print(f"You can view logs at [bold]{home_dir}/.logrctx/logs/reduced_raw.log[/bold]", style="bold yellow")

## rag chat
def rag():
    # RAG chatbot
    rag_chat_init(
        dir_path=f"{home_dir}/.logrctx/logs/",
        filename=f"reduced_raw.log"
    )

## service management
def service(support: str = None):
    try:
        if support is None:
            console.print("Please provide support to manage service", style="bold red")
            exit()

        if support == "start":
            # start ollama service in brew
            with console.status("Starting ollama service..."):
                os.system("brew services start ollama")
            console.print("✔️ Ollama service started!", style="bold green")

        if support == "stop":
            # stop ollama service in brew
            with console.status("Stopping ollama service..."):
                os.system("brew services stop ollama")
            console.print("❌ Ollama service stopped!", style="bold red")

        if support == "restart":
            # restart ollama service in brew
            with console.status("Restarting ollama service..."):
                os.system("brew services restart ollama")
            console.print("🔄 Ollama service restarted!", style="bold yellow")
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")

## help command
def help():
    console.print("🚀 Welcome to logrctx 🚀", style="bold green")
    console.print("Usage: logrctx \[function] \[support]", style="bold yellow")
    console.print("Functions:", style="bold blue")
    console.print("  loki - Retrieve logs from loki", style="bold blue")
    console.print("  reduce - Reduce logs using string matching", style="bold blue")
    console.print("  rag - Chat with RAG AI for log analysis", style="bold blue")
    console.print("  service - Manage ollama service", style="bold blue")
    console.print("  init - Initialize logrctx with loki, reduce and rag", style="bold blue")
    console.print("  help - Show help", style="bold blue")

# reduce command
@app.command()
def root(
    function: str = typer.Argument("help", help="Function"), 
    support: str = typer.Argument(None, help="Function support")
    ):

    # clear terminal
    console.clear()

    if function == "loki":
        loki(support)

    if function == "reduce":
        reduce()

    if function == "rag":
        rag()

    if function == "init":
        loki(support)
        reduce()
        rag()

    if function == "service":
        service(support)

    if function == "help":
        help()

if __name__ == "__main__":
    app()
