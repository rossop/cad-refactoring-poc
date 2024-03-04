import ast

# Example CadQuery script as a string
cadquery_script = """
import cadquery as cq

result = cq.Workplane("XY").box(60, 20, 10).edges("|Z").fillet(2)
"""

# Parse the CadQuery script using the AST module
parsed_script = ast.parse(cadquery_script)

# Define a visitor class that extends ast.NodeVisitor to process AST nodes
class CadQueryVisitor(ast.NodeVisitor):
    def __init__(self, verbose=False):  
        self.verbose = verbose
        self.function_calls = []
    
    def __repr__(self):
        return f"<CadQueryVisitor verbose={self.verbose}, 
                function_calls={len(self.function_calls)}>"
    
    def __str__(self):
        summary = "CadQuery Script Analysis Summary:\n"
        if not self.detected_patterns:
            return summary + "No specific patterns detected."
        
        # Summarize detected patterns
        for pattern, count in self.detected_patterns.items():
            summary += f"- Detected {count} uses of {pattern}()\n"
        
        # Optionally, add a conclusion or recommendation
        summary += "\nConsider reviewing complex geometries for optimization opportunities."
        return summary
    
    def print_tree(self):
        # Construct a string representation of the construction tree
        tree_str = "CadQuery Construction Tree:\n"
        for i, operation in enumerate(self.operations, start=1):
            tree_str += f"{i}. {operation}\n"
        return tree_str

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            self.function_calls.append(node.func.attr)
            if self.verbose:
                print(f"Function call: {node.func.attr}")
        self.generic_visit(node)

    def print_function_calls(self):
        for call in self.function_calls:
            print(f"Function called: {call}")

    def detailed_report(self):
        report = "CadQueryVisitor Detailed Report:\n"
        report += f"Total Function Calls: {len(self.function_calls)}\n"
        for call in self.function_calls:
            report += f"- {call}\n"
        return report


class CadQueryTreeBuilder(ast.NodeVisitor):
    def __init__(self):
        self.tree = []
        self.current_depth = 0

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            # Append operation with indentation based on current depth
            operation = '    ' * self.current_depth + f"└── {node.func.attr}()"
            self.tree.append(operation)
        # Assume child nodes increase depth
        original_depth = self.current_depth
        self.current_depth += 1
        self.generic_visit(node)
        self.current_depth = original_depth

    def __str__(self):
        if not self.tree:
            return "No operations detected."
        return "CadQuery Script Construction Tree:\n" + "\n".join(self.tree)



class CadQueryRefactor(ast.NodeTransformer):
    def visit_Call(self, node):
        # Check if the function call is a method we want to rename
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'oldMethodName':
            # Rename the method
            node.func.attr = 'newMethodName'
        # Important: return the modified node
        return node
    def write_model(self, parsed_script):
        modified_tree = CadQueryRefactor().visit(parsed_script)
        modified_code = ast.unparse(modified_tree)


# Create an instance of the visitor and use it to traverse the parsed script
visitor = CadQueryVisitor()
visitor.visit(cadquery_script)
visitor.print_function_calls()
