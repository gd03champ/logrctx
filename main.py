import typer
from rich.console import Console

from utils_sm.string_matching import reduce
from utils_ai.rag_lc import rag_chat_init

app = typer.Typer()
console = Console()

# reduce command
@app.command()
def root(function: str):
    if function == "reduce":

        # get logs from loki
        console.print("Skipping loki logs retrieval with simulated logs...", style="bold yellow")

        # string matching reduce
        console.print("Reducing logs...", style="bold yellow")
        reduce(
            input_file = 'logs/sample full.log',
            output_file = 'logs/reduced_sample.log'
            )
        console.print("Logs reduced successfully!", style="bold green")

    if function == "rag":
        console.print("Initializing RAG chat...", style="bold yellow")
        rag_chat_init(
            dir_path = "logs",
            filename = "reduced_sample.log"
        )

if __name__ == "__main__":
    app()
