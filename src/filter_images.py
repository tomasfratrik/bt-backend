from src.image import FOUND_IMAGE_TYPES


class FilterImages():

    def __init__(self, report):
        self.report = report
        self.filter_images()
    
    def get_report(self):
        return self.report
    
    def filter_images(self):
        self.filter_redundant()
    
    def filter_redundant(self):
        for img_type in FOUND_IMAGE_TYPES:
            unique_domains = []
            new_dict = []
            for img in self.report["images"][img_type]:
                if img["domain"] not in unique_domains:
                    unique_domains.append(img["domain"])
                    new_dict.append(img)
            self.report["images"][img_type] = new_dict
