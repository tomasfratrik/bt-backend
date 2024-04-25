import src.point_modules as pm


class Evaluator:
    # expected data in report format from FormatParser
    def __init__(self, report):
        self.report = report
    
    def evaluate(self):
        for module in pm.points_map:
            posted_img = self.report["images"]["posted_images"][0]
            # if image is not from url and module needs url, skip
            needs_url = pm.points_map[module]["needs_url"]
            if posted_img["from_url"] is False and needs_url is True:
                continue
            func_string = f'pm.{module}(report=self.report)'
            self.report = eval(func_string)

    def get_report(self):
        return self.report 





