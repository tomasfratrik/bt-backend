import src.point_modules as pm

class Evaluator:
    # expected data in report format
    report = {}

    def __init__(self, report):
        self.report = report
    
    def evaluate(self):
        print(pm.points)
        


