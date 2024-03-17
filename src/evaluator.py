import src.point_modules as pm

class Evaluator:
    # expected data in report format from FormatParser
    def __init__(self, report):
        self.report = report
    
    def evaluate(self):
        for module in pm.points_map:
            func_string = f'pm.{module}(report=self.report)'
            self.report = eval(func_string)
        self.score_to_percent()
    
    def score_to_percent(self):
        for img_type in self.report["images"]:
            for img in self.report["images"][img_type]:
                 img["total_points_percentage"] = int((img["points"] / self.report["max_points"]) * 100)

    def get_report(self):
        return self.report 





