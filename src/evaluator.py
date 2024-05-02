import src.point_modules as pm


class Evaluator:
    # expected data in report format from FormatParser
    def __init__(self, report):
        self.report = report
    

    def evaluate(self):
        for module in pm.points_map:
            func_string = f'pm.{module}(report=self.report)'
            self.report = eval(func_string)
    

    def evaluate_new_countries(self, country):
        self.report = pm.change_country(self.report, country)


    def get_report(self):
        return self.report 





