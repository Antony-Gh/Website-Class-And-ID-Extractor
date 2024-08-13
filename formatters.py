import subprocess
import os
import time
from pathlib import Path
from typing import List, Tuple, Dict

# Get the path of the current file
script_path = Path(__file__).resolve()
# Get the parent directory of the current file
script_current_directory_path = script_path.parent

script_current_directory = str(script_current_directory_path)

# Define paths to beautifiers and fixer
html_beautify = Path(script_current_directory + r"/packages/html-beautify.cmd")

css_beautify = Path(script_current_directory + r"/packages/css-beautify.cmd")

js_beautify = Path(script_current_directory + r"/packages/js-beautify.cmd")

php_cs_fixer_path = Path(script_current_directory + r"/packages/Composer/vendor/bin/php-cs-fixer.bat")

# Move one directory up
project_directory = script_current_directory_path.parent

def get_list_of_files(file_types: Tuple[str]) -> List[Path]:
    files_to_format = []
    for root, _, files in os.walk(project_directory):
        if 'node_modules' in root or 'Website Class And ID Extractor' in root:
            continue  # Skip node_modules & script directory
        for file in files:
            file_path = Path(root) / file
            if file.endswith(file_types):
                files_to_format.append(file_path)
    return files_to_format

def run_beautify(command, file_path):
    file_path_str = str(file_path)
    try:
        if command == php_cs_fixer_path:
            result = subprocess.run(
                [str(command), "fix", "--allow-risky=yes", file_path_str],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        else:
            result = subprocess.run(
                [str(command), "--replace", file_path_str],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
    except subprocess.CalledProcessError as e:
        print(f"Error running {command} on {file_path}: {e}")
        print(f"Standard Output: {e.stdout.decode('utf-8')}")
        print(f"Standard Error: {e.stderr.decode('utf-8')}")
        return e.returncode
    return result.returncode


def format_files(progress_var, progress_bar) -> None:
    files_to_format = get_list_of_files((".html", ".css", ".js", ".php"))
    total_files = len(files_to_format)
    for i, file_path in enumerate(files_to_format):
        if file_path.suffix == ".html":
            run_beautify(html_beautify, file_path)
        elif file_path.suffix == ".css":
            run_beautify(css_beautify, file_path)
        elif file_path.suffix == ".js":
            run_beautify(js_beautify, file_path)
        elif file_path.suffix == ".php":
            run_beautify(php_cs_fixer_path, file_path)
        progress_var.set((i + 1) / total_files * 100)
        progress_bar.update()
        time.sleep(0.05)