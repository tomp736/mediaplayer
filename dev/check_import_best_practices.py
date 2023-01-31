import ast
import os


def check_import_best_practices(node):
    if isinstance(node, ast.Import):
        # Check for multiple imports in the same line
        if len(node.names) > 1:
            return "Multiple imports in the same line are not recommended"

    elif isinstance(node, ast.ImportFrom):
        # Check for wildcard imports
        if node.names[0].name == '*':
            return "Wildcard imports are not recommended"
        
        # Check for multiple imports in the same line
        if len(node.names) > 1:
            return "Multiple imports in the same line are not recommended"
        
        # Check for relative imports
        if node.level > 0:
            return "Relative imports are not recommended"

    return None

def parse_file(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
        tree = ast.parse(code)
        for node in ast.walk(tree):
            result = check_import_best_practices(node)
            if result:
                print(f"{file_path}: {result}")

def parse_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                parse_file(file_path)

if __name__ == "__main__":
    parse_directory("../src")
