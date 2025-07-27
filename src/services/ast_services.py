import ast 
from typing import Set, Tuple

class ExtractorFunctionsRelation(ast.NodeVisitor):
    def __init__(self,filename)-> None:
        self.filename:str=filename
        self.current_function:str=None
        self.modules:Set[str]=set()
        self.edges=set()

    def visit_FunctionDef(self,node)->None:
        self.current_function=f"""{self.filename}:{node.name}"""
        self.generic_visit(node)

    def visit_ClassDef(self, node) -> None:
        self.current_function = f"{self.filename}:{node.name}"
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.current_function = f"{self.filename}:{node.name}"
        self.generic_visit(node)


    def visit_Call(self, node)->None:
        if isinstance(node.func,ast.Name):
            if self.current_function:
                called_function:str=f"""{self.filename}:{node.func.id}"""
                self.edges.add((self.current_function,called_function))

        elif isinstance(node.func.value,ast.Name):
                if self.current_function :
                    called_class=node.func
                    called_function:str=f"""{called_class.value.id}:{called_class.value.id}-{called_class.attr} """
                    self.edges.add((self.current_function,called_function))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            module_name = node.module
            self.modules.add(module_name.replace('.','/')+'.py')
            
        self.generic_visit(node)


    def get_edges(self) -> Set[Tuple[str, str]]:
        return self.edges

