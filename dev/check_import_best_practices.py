import ast
import os
import sys
from typing import List

def check_import_best_practices(node) -> List[str]:
    messages = []
    if isinstance(node, ast.Import):
        # Check for multiple imports in the same line
        if len(node.names) > 1:
            messages.append("Multiple imports in the same line are not recommended")

    elif isinstance(node, ast.ImportFrom):
        # Check for wildcard imports
        if node.names[0].name == '*':
            messages.append( "Wildcard imports are not recommended")
        
        # Check for multiple imports in the same line
        if len(node.names) > 1:
            messages.append( "Multiple imports in the same line are not recommended")
        
        # Check for relative imports
        if node.level > 0:
            messages.append( "Relative imports are not recommended")
    return messages

def parse_file(file_path) -> List[str]:
    messages = []
    with open(file_path, 'r') as f:
        code = f.read()
        tree = ast.parse(code)
        for node in ast.walk(tree):
            node_messages = check_import_best_practices(node)
            for message in node_messages:                
                messages.append(f"{file_path}: {message}")
        
    return messages

def parse_directory(directory):
    messages = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_messages = parse_file(file_path)
                for message in file_messages:                
                    messages.append(message)
        
    return messages

if __name__ == "__main__":
    directory_messages = parse_directory(".")
    if directory_messages and len(directory_messages) > 0:
        for message in directory_messages:                
            print(message)
        sys.exit(100)
