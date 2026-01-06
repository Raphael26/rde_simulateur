import inspect
import ast
import types


class FunctionLoader:
    """
    A utility class to dynamically load, inspect, and call a Python function
    defined in a code string.

    Attributes:
        code_string (str): The raw code string containing the function.
        function_name (str): The name of the first defined function in the code.
        function (function): The loaded function object.
        signature (inspect.Signature): The function's signature object.
    """
    # 4.1.4
    def __init__(self, code_string):
        """
        Initializes the FunctionLoader with a code string, extracting and
        loading the first function found.

        Args:
            code_string (str): Python code containing at least one function.
        """
        self.code_string = code_string
        self.function_name = self._extract_function_name() # 4.1.5
        self.function = self._load_function() # 4.1.6
        self.signature = inspect.signature(self.function) # 4.1.7

    def _extract_function_name(self):
        """
        Parses the code string and returns the name of the first function defined.

        Returns:
            str: The name of the first function found.
        """
        # 4.1.5
        try:
            parsed = ast.parse(self.code_string)
            for node in parsed.body:
                if isinstance(node, ast.FunctionDef):
                    return node.name
        except Exception as e:
            raise ValueError(f"Failed to parse code: {e}")

        raise ValueError("No function definition found.")

    def _load_function(self):
        """
        Executes the code and extracts the function object by name.

        Returns:
            function: The loaded Python function object.
        """
        # 4.1.6
        local_namespace = {}

        try:
            exec(self.code_string, {}, local_namespace)
        except Exception as e:
            raise RuntimeError(f"Failed to execute code: {e}")

        func = local_namespace.get(self.function_name)

        if not isinstance(func, types.FunctionType):
            raise TypeError(f"{self.function_name} is not a valid function.")

        return func

    def get_signature(self):
        """Returns the function's signature as a string."""
        return str(self.signature)

    def get_parameters(self):
        """
        Returns detailed information about each parameter of the function.

        Returns:
            dict: A dictionary where keys are parameter names, and values are
                  dicts containing 'default', 'kind', 'annotation', and 'required'.
        """
        # 4.1.10
        return {
            name: {
                "default": (
                    param.default if param.default is not inspect._empty else None
                ),
                "kind": str(param.kind),
                "annotation": (
                    str(param.annotation)
                    if param.annotation != inspect._empty
                    else None
                ),
                "required": (
                    param.default is inspect._empty
                    and param.kind in (
                        param.POSITIONAL_OR_KEYWORD,
                        param.KEYWORD_ONLY
                    )
                )
            }
            for name, param in self.signature.parameters.items()
        }

    def call_with_dict(self, arg_dict):
        """
        Calls the function using a dictionary of named arguments.

        Args:
            arg_dict (dict): A dictionary of argument names and values.

        Returns:
            Any: The result of the function call.
        """
        # 4.1.14
        try:
            return self.function(**arg_dict)
        except TypeError as e:
            raise TypeError(f"Error calling function with args {arg_dict}: {e}")