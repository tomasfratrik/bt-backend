from src.image import IMAGE_TYPES, FOUND_IMAGE_TYPES
from src.timer import timeme

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
    
    @timeme
    def order_images(self):
        self.score_to_percent()
        self.order_images_by_points()
        self.setup_portal_points_and_photo()
        self.order_portals_by_points()
    

    def order_portals_by_points(self):
        for img_type in FOUND_IMAGE_TYPES:
            # sorted_dict = dict(sorted(self.report["images"][img_type].items(),
            #                           key=lambda x: x[1]["most_points"], reverse=True))
            # self.report["images"][img_type] = sorted_dict
            sorted_keys = sorted(self.report["images"][img_type],
                                 key=lambda x: self.report["images"][img_type][x]["most_points"],
                                 reverse=True)
            # print(f"SORTED KEYS: {sorted_keys}")
            sorted_dict = {key: self.report["images"][img_type][key] for key in sorted_keys}
            # print("SORTED DICT")
            # for k,v in sorted_dict.items():
            #     print(f"{k} : {v['most_points']}")
            self.report["images"][img_type] = sorted_dict
    
    def order_images_by_points(self):
        for img_type in FOUND_IMAGE_TYPES:
            for portal, data in self.report["images"][img_type].items():
                data["images"] = sorted(data["images"], key=lambda x: x["points"], reverse=True)

    def setup_portal_points_and_photo(self): 
        for img_type in FOUND_IMAGE_TYPES:
            for portal, data in self.report["images"][img_type].items():
                data["most_points"] = data["images"][0]["points"]
                data["most_points_photo"] = data["images"][0]["display_photo_url"]
    
    def score_to_percent(self):
        for img_type in FOUND_IMAGE_TYPES:
            for portal, data in self.report["images"][img_type].items():
                for img in data["images"]:
                    img["total_points_percentage"] = int((img["points"] / self.report["max_points"]) * 100)
        
        for img in self.report["images"]["posted_images"]:
            img["total_points_percentage"] = int((img["points"] / self.report["max_points"]) * 100)

    
    def get_report(self):
        return self.report