import src.point_modules as pm

class Evaluator:
    # expected data in report format from FormatParser
    def __init__(self, report):
        self.report = report
    
    def evaluate(self):
        for module, points in pm.points.items():
            call = f'pm.{module}(report=self.report)'
            self.report = eval(call)
        return self.report



