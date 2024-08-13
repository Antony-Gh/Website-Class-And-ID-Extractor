from typing import Dict, List, Tuple
from pathlib import Path

def find_missing_css_classes(html_classes: Dict[str, List[Tuple[Path, int]]], css_classes: Dict[str, List[Tuple[Path, int]]], css_ids: Dict[str, List[Tuple[Path, int]]], css_elements: Dict[str, List[Tuple[Path, int]]], css_pseudos: Dict[str, List[Tuple[Path, int]]]) -> Dict[str, List[Tuple[Path, int]]]:
    missing_classes = {}
    for cls, locations in html_classes.items():
        found = False
        for css_cls in css_classes.items():
            if cls in css_cls:
                found = True
                break
        for css_id in css_ids.items():
            if cls in css_id:
                found = True
                break
        for css_element in css_elements.items():
            if cls in css_element:
                found = True
                break   
        for css_pseudo in css_pseudos.keys():
            if cls in css_pseudo:
                found = True
                break   
        if not found:
            missing_classes[cls] = locations
    return missing_classes

def find_unused_css_classes(html_classes: Dict[str, List[Tuple[Path, int]]], css_classes: Dict[str, List[Tuple[Path, int]]], js_classes: Dict[str, List[Tuple[Path, int]]]) -> Dict[str, List[Tuple[Path, int]]]:
    unused_classes = {}
    
    for cls, locations in css_classes.items():
        # Skip classes that contain pseudo-classes or pseudo-elements
        if ":" in cls or "::" in cls:
            continue
        
        # Check if the class is used in HTML or JavaScript
        if not any(cls in html_cls for html_cls in html_classes) and not any(cls in js_cls for js_cls in js_classes):
            unused_classes[cls] = locations
    return unused_classes

def find_unused_css_id_selectors(css_ids, html_ids):
    unused_ids = {}
    for id_, locations in css_ids.items():
        # Skip IDs that contain pseudo-classes or pseudo-elements
        if ":" in id_ or "::" in id_:
            continue
        
        if id_ not in html_ids:
            unused_ids[id_] = locations
    return unused_ids

def find_class_id_conflicts(html_classes: Dict[str, List[Tuple[Path, int]]], html_ids: Dict[str, List[Tuple[Path, int]]], css_classes: Dict[str, List[Tuple[Path, int]]]) -> Dict[str, Dict[str, List[Tuple[Path, int]]]]:
    conflicts = {}
    for cls in html_classes.keys() | css_classes.keys():
        if cls in html_ids:
            conflicts[cls] = {
                "class_locations": html_classes.get(cls, []),
                "id_locations": html_ids[cls]
            }
    return conflicts

def find_duplicated_css_classes(css_classes, css_ids, css_elements):
    duplicated_classes = {}
    if css_classes:
        for cls, locations in css_classes.items():
            if len(locations) > 1:
                duplicated_classes[cls] = locations
    if css_ids:      
        for cls, locations in css_ids.items():
            if len(locations) > 1:
                duplicated_classes[cls] = locations
    if css_elements:
        for cls, locations in css_elements.items():
            if len(locations) > 1:
                duplicated_classes[cls] = locations
    return duplicated_classes