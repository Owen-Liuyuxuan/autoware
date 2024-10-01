import os
import ast
import astor
from astroid import parse, extract_node

def update_function(file_path, function_name, new_function_code):
    """
    Updates a function in a Python file with new code.

    Args:
        file_path (str): The path to the Python file.
        function_name (str): The name of the function to be updated.
        new_function_code (str): The new code for the function. This can be either the actual code or the path to a file containing the code.

    Raises:
        ValueError: If the specified function is not found in the file.

    Returns:
        None
    """

    with open(file_path, 'r') as file:
        content = file.read()

    if os.path.exists(new_function_code):
        # new_function_code is a file path
        with open(new_function_code, 'r') as file:
            new_function_code = file.read()

    tree = ast.parse(content)
    new_func = ast.parse(new_function_code).body[0]

    for i, node in enumerate(tree.body):
        ## not only search for functions, but also classes (one layer deep)
        if isinstance(node, ast.ClassDef):
            is_found = False
            for j, subnode in enumerate(node.body):
                if isinstance(subnode, ast.FunctionDef):
                    print(subnode.name)
                if isinstance(subnode, ast.FunctionDef) and subnode.name == function_name:
                    node.body[j] = new_func
                    is_found = True
                    break
            if is_found:
                break
        ## functions directly in the file
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            tree.body[i] = new_func

        if isinstance(node, ast.FunctionDef):
            print(node.name)
    else:
        raise ValueError(f"Function {function_name} not found in {file_path}")

    new_content = astor.to_source(tree)
    # print(new_content)
    with open(file_path, 'w') as file:
        file.write(new_content)

if __name__ == "__main__":
    file_path = os.environ['FILE_PATH']
    function_name = os.environ['FUNCTION_NAME']
    new_function = os.environ['NEW_FUNCTION']
    update_function(file_path, function_name, new_function)
    print("Update completed successfully")
