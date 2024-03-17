
from src.image import IMAGE_TYPES

class Adjust():
    """
    Final touches to report

    * Order images in report, depending on points
    """

    def __init__(self, report):
        self.report = report
        self.adjust_report()
    
    def adjust_report(self):
        self.order_images()
    
    def order_images(self):
        self.order_images_by_points()
    
    def order_images_by_points(self):
        for img_type in IMAGE_TYPES:
            self.report["images"][img_type] = sorted(self.report["images"][img_type], key=lambda x: x["points"], reverse=True)
    
    
    def get_report(self):
        return self.report