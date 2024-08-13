import re
import os
import time
from pathlib import Path
from typing import List, Tuple, Dict

# Get the path of the current file
script_path = Path(__file__).resolve()

# Get the parent directory of the current file
script_current_directory = script_path.parent

# Move one directory up
project_directory = script_current_directory.parent

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

def contains_special_chars(string: str) -> bool:
    return string == "\n" or string == " " or string == ""

# Step 2: Extract class and ID names from HTML & PHP files and their locations
def extract_html_classes_and_ids() -> Tuple[Dict[str, List[Tuple[Path, int]]], Dict[str, List[Tuple[Path, int]]]]:
    html_classes = {}
    html_ids = {}

    files = get_list_of_files((".html", ".php"))

    total_files = len(files)
    for idx, file in enumerate(files):
        with open(file, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):

                # Extract classes
                classes = re.findall(r'class="([^"]*)"', line)
                for class_list in classes:
                    for cls in class_list.split():
                        if cls not in html_classes:
                            html_classes[cls] = []
                        html_classes[cls].append((file, line_number))
                # Extract IDs
                ids = re.findall(r'id="([^"]*)"', line)
                for id_ in ids:
                    if id_ not in html_ids:
                        html_ids[id_] = []
                    html_ids[id_].append((file, line_number))
    return html_classes, html_ids

# Step 3: Extract class and ID names from CSS files with their locations
def extract_css_classes_and_ids() -> Tuple[Dict[str, List[Tuple[Path, int]]], Dict[str, List[Tuple[Path, int]]], Dict[str, List[Tuple[Path, int]]], Dict[str, List[Tuple[Path, int]]], Dict[str, List[Tuple[Path, int]]]]:
    css_classes = {}
    css_ids = {}
    css_elements = {}
    css_pseudo = {}
    css_nested = {}
    
    css_class_pattern = re.compile(
        r'(?:[.#]?[a-zA-Z][\w-]*)(?:\s*[:]{1,2}[\w-]+)*(?:\s*(?:[.#]?[a-zA-Z][\w-]*)'
        r'(?:\s*[:]{1,2}[\w-]+)*)*\s*{'
    )
    
    files = get_list_of_files((".css"))
    
    total_files = len(files)
    for i, file in enumerate(files):
        with open(file, "r", encoding="utf-8") as f:
            inside_at_block = False
            count = 0
            inside_second_block = False
            for lineNumber, line in enumerate(f, 1):
                
                if "@" in line:
                    inside_at_block = True
                if "{" in line:
                    count += 1
                if "}" in line:
                    count -= 1    
                    
                if count > 1:
                    inside_second_block = True
                else:
                    inside_second_block = False
                        
                if inside_at_block:
                    if "}" in line and not inside_second_block:
                        inside_at_block = False
                        inside_second_block = False
                        count = 0
                    continue
                    
                if contains_special_chars(line):
                    continue
                    
                classes = css_class_pattern.findall(line)
                    
                if classes:
                    for cls_match in classes:
                        cls = cls_match.strip().rstrip('{')
                        if cls.startswith('.'):
                            class_names = re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]*)', cls)
                            for class_name in class_names:
                                print(class_name)
                                if class_name not in css_classes:
                                    css_classes[class_name] = []
                                css_classes[class_name].append((file, lineNumber))
                                if class_name not in css_nested:
                                    css_nested[class_name] = []
                                css_nested[class_name].append((file, lineNumber))
                                print("Alo")
                        elif cls.startswith('#') or '#' in cls:
                            id_ = cls.strip().lstrip('#').rstrip()
                            if ":" not in id_:
                                if id_ not in css_ids:
                                    css_ids[id_] = []
                                css_ids[id_].append((file, lineNumber))
                            else:
                                if id_ not in css_pseudo:
                                    css_pseudo[id_] = []
                                css_pseudo[id_].append((file, lineNumber))
                        elif cls.isalpha():
                            element_name = cls.strip().rstrip()
                            if ":" not in element_name:
                                if element_name not in css_elements:
                                    css_elements[element_name] = []
                                css_elements[element_name].append((file, lineNumber))
                            else:
                                if element_name not in css_pseudo:
                                    css_pseudo[element_name] = []
                                css_pseudo[element_name].append((file, lineNumber))
                        print("Alo2")        
    return css_classes, css_ids, css_elements, css_pseudo, css_nested

# Step 4: Extract class names from JavaScript files
def extract_js_classes(progress_var, progress_bar) -> Dict[str, List[Tuple[Path, int]]]:
    js_classes = {}

    files = get_list_of_files((".js"))

    class_pattern = re.compile(
        r'\bclass\s*=\s*["\'](?:([^"\']+)\s*)+["\']|'  # Matches class attribute value
        r'\bclassList\.add\((?:"([^"]+)",?\s*)+\)|'  # Matches classList.add
        r'\bclassList\.remove\((?:"([^"]+)",?\s*)+\)|'  # Matches classList.remove
        r'\bclassList\.toggle\((?:"([^"]+)",?\s*)+\)|'  # Matches classList.toggle
        r'\bclassName\s*=\s*["\']((?:\b\w+\b\s*)+)["\']'  # Matches className attribute value
    )

    total_files = len(files)
    for idx, file in enumerate(files):
        with open(file, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                matches = class_pattern.findall(line)
                for match in matches:
                    for cls in match:
                        if cls:
                            class_names = cls.split()
                            for class_name in class_names:
                                if class_name not in js_classes:
                                    js_classes[class_name] = []
                                js_classes[class_name].append((file, line_number))

        progress_var.set((idx + 1) / total_files * 100)
        progress_bar.update()
        time.sleep(0.05)
    return js_classes
