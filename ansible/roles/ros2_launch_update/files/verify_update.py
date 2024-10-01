import os
import ast

def verify_update(file_path, function_name):
    """
    Verifies if a specific function is present in a given file and correctly formatted.

    Args:
        file_path (str): The path to the file to be checked.
        function_name (str): The name of the function to search for.

    Raises:
        ValueError: If the specified function is not found in the file or if the function is not correctly formatted.

    Returns:
        None
    """
    with open(file_path, 'r') as file:
        content = file.read()

    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            print("Update successful")
            return

    raise ValueError(f"Function {function_name} not found in {file_path}")

if __name__ == "__main__":
    file_path = os.environ['FILE_PATH']
    function_name = os.environ['FUNCTION_NAME']
    verify_update(file_path, function_name)
