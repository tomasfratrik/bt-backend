
from src.image import IMAGE_TYPES, FOUND_IMAGE_TYPES

class PostEvaluation():
    """
    Final touches to report

    * Order images in report, depending on points
    * Final score to percentage
    """

    def __init__(self, report):
        self.report = report
        self.adjust_report()
    
    def adjust_report(self):
        self.order_images()
    
    def order_images(self):
        self.score_to_percent()
        self.order_images_by_points()
    
    def order_images_by_points(self):
        for img_type in FOUND_IMAGE_TYPES:
            for portal, data in self.report["images"][img_type].items():
                data["images"] = sorted(data["images"], key=lambda x: x["points"], reverse=True)
    
    def score_to_percent(self):
        for img_type in FOUND_IMAGE_TYPES:
            for portal, data in self.report["images"][img_type].items():
                for img in data["images"]:
                    img["total_points_percentage"] = int((img["points"] / self.report["max_points"]) * 100)
        
        for img in self.report["images"]["posted_images"]:
            img["total_points_percentage"] = int((img["points"] / self.report["max_points"]) * 100)

    
    def get_report(self):
        return self.report