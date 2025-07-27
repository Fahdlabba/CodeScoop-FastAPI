from radon.visitors import ComplexityVisitor 
from radon.metrics import mi_visit
from radon.raw import analyze
from typing import List




class StaticMetrics:
    def __init__(self):
        pass 

    def cyclomatic_complexity(self, code: str) ->List:
        try : 
            visitor = ComplexityVisitor.from_code(code)
            return visitor.complexity
        except Exception as e:
            print(f"Error : {e}") 

    def maintainability_index(self, code: str) -> float:
        try:
            return mi_visit(code)
        except Exception as e:
            print(f"Error : {e}")
            return 0.0
    def raw_metrics(self, code: str) -> dict:
        """
        Calculate raw metrics for the given code.
        """
        try:
            raw_metrics = analyze(code)
            return raw_metrics
        except Exception as e:
            print(f"Error : {e}")
            return {}

    def calculate_metrics(self, code: str) -> dict:
        """
        Calculate all static metrics for the given code.
        """
        try:
            raw_metrics = self.raw_metrics(code)
            metrics = {
                "cyclomatic_complexity": self.cyclomatic_complexity(code),
                "loc": raw_metrics.loc,
                "lloc": raw_metrics.lloc,
                "comments": raw_metrics.comments,
            }
            return metrics
        except Exception as e:
            print(f"Error : {e}")
            return {}