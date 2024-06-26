from rich.console import Console
import re
from rich.console import Console
import re

def load_logs(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def save_logs(file_path, logs):
    with open(file_path, 'w') as file:
        for log in logs:
            file.write(log)

def load_logs(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def save_logs(file_path, logs):
    with open(file_path, 'w') as file:
        for log in logs:
            file.write(log)

def reduce_logs(logs):
    log_dict = {}
    log_pattern = re.compile(r'^\S+\s+\S+\s+\S+\s+(.*)$')
    
    for index, log in enumerate(logs):
        match = log_pattern.match(log)
        if match:
            log_content = match.group(1)
            # Remove process IDs and other dynamic parts from the log content
            log_content = re.sub(r'\[\d+\]', '[PID]', log_content)
            log_content = re.sub(r'\d{1,3}(?:\.\d{1,3}){3}', 'IP', log_content)
            if log_content not in log_dict:
                log_dict[log_content] = [index, index]
            else:
                log_dict[log_content][1] = index
    
    reduced_logs = []
    for indices in log_dict.values():
        first_index, last_index = indices
        reduced_logs.append(logs[first_index])
        if first_index != last_index:
            reduced_logs.append(logs[last_index])
    
    return reduced_logs

def reduce(input_file, output_file):
    logs = load_logs(input_file)
    reduced_logs = reduce_logs(logs)
    save_logs(output_file, reduced_logs)

if __name__ == "__main__":
    console = Console()
    console.print("[bold]Log Reducer[/bold]")
    console.print("")

    #input_file = console.input("Enter the input file path: ")
    #output_file = console.input("Enter the output file path: ")
    input_file = 'sample full.log'
    output_file = 'reduced_sample.log'

    console.print("")
    console.print("[bold]Reducing logs...[/bold]")
    console.print("")

    reduce(input_file, output_file)

    console.print("")
    console.print("[bold]Logs reduced successfully![/bold]")
    console.print("Output file saved at:", output_file)
