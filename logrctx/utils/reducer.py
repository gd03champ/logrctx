from rich.console import Console
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from collections import defaultdict
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

def reduce_logs(logs):
    unique_logs = defaultdict(int)
    request_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
    
    for log in logs:
        for method in request_methods:
            if method in log:
                start_index = log.index(method)
                normalized_log = log[start_index:].strip()
                unique_logs[normalized_log] += 1
                break
    
    reduced_logs = []
    for log in logs:
        for method in request_methods:
            if method in log:
                start_index = log.index(method)
                normalized_log = log[start_index:].strip()
                count = unique_logs[normalized_log]
                if count > 1:
                    reduced_log = log[:-1] + f' (x{count})\n'
                    unique_logs[normalized_log] = 0  # To avoid appending count multiple times
                    reduced_log = "".join(reduced_log.split(',')[1:])
                    reduced_logs.append(reduced_log)
                elif unique_logs[normalized_log] == 1:
                    log = "".join(log.split(',')[1:])
                    reduced_logs.append(log)
                break
    
    return sorted(reduced_logs)

def drain_logs(logs):
    # Set up Drain3 TemplateMiner
    config = TemplateMinerConfig()
    config.profiling_enabled = False
    template_miner = TemplateMiner(config=config)

    unique_templates = {}
    log_counts = {}

    for log in logs:
        result = template_miner.add_log_message(log)
        template_id = result["cluster_id"]
        template_str = result["template_mined"]

        if template_id not in unique_templates:
            unique_templates[template_id] = template_str
            log_counts[template_id] = 1
        else:
            log_counts[template_id] += 1

    reduced_logs = []
    for template_id, template_str in unique_templates.items():
        count = log_counts[template_id]
        if count > 1:
            reduced_log = f"{template_str} (x{count})"
        else:
            reduced_log = template_str
        reduced_logs.append(reduced_log+"\n")

    return reduced_logs


def reduce(operaton, input_file, output_file):
    logs = load_logs(input_file)
    reduced_logs = reduce_logs(logs) if operagitton == 'reduce' else drain_logs(logs)
    save_logs(output_file, reduced_logs)

if __name__ == "__main__":
    console = Console()
    console.print("[bold]Log Reducer[/bold]")
    console.print("")

    #input_file = console.input("Enter the input file path: ")
    #output_file = console.input("Enter the output file path: ")
    input_file = '../logs/raw.log'
    output_file = '../logs/reduced_raw.log'

    console.print("")
    console.print("[bold]Reducing logs...[/bold]")
    console.print("")

    reduce("drain", input_file, output_file)

    console.print("")
    console.print("[bold]Logs reduced successfully![/bold]")
    console.print("Output file saved at:", output_file)
