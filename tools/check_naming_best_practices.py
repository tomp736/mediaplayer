import ast
import os
import sys
from typing import List

        
def check_naming_best_practices(node: ast.AST) -> List[str]:
    messages = []    
    for node in ast.walk(node):
        if isinstance(node, ast.FunctionDef):
            # Use snake_case for variables, functions, and method names.
            # Snake case requires that words in a name be separated by underscores, and the entire name be in all lowercase letters.
            if not node.name.islower():
                messages.append(f"{node.lineno}: Function name '{node.name}' should be in snake_case.")
        elif isinstance(node, ast.ClassDef):
            # Use PascalCase for class names.
            # Pascal case requires that the first letter of each word in a name be capitalized, and words are not separated by underscores.
            if not node.name[0].isupper() or "_" in node.name:
                messages.append(f"{node.lineno}: Class name '{node.name}' should be in PascalCase.")
        # elif isinstance(node, ast.Name):
        #     # Start variables with a lowercase letter
        #     pass
        
    return messages


def parse_file(file_path) -> List[str]:
    messages = []
    with open(file_path, 'r') as f:
        code = f.read()
        tree = ast.parse(code)
        for node in ast.walk(tree):
            node_messages = check_naming_best_practices(node)
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
