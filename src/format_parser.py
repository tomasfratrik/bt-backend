from src.image import Image
import src.point_modules as pm


class FormatParser():

    def __init__(self, posted_img_list=[], sim_img_list=[], src_img_list=[], db_img_list=[]):
        self._posted_img_list = posted_img_list
        self._sim_img_list = sim_img_list
        self._src_img_list = src_img_list
        self._db_img_list = db_img_list
        self.report = {}
        self.init_report()
        self.parse_posted_images()
        self.parse_found_images()
        # self.parse_db_images()
    
    def parse_posted_images(self):
        for img in self._posted_img_list:
            img_obj = {
                "ssim": 0,
                "file_path": img.get_absolute_path(),
                "display_position": 0,
                "points": 0,
                "point_modules_detected": {} 
            }
            if img.from_url():
                img_obj["display_photo_url"] = img.get_origin_img_url_link()
                img_obj["website_name"] = img.get_website_name()
                img_obj["website_url"] = "empty"
                img_obj["tld"] = img.get_tld()
                img_obj["domain"] = img.get_domain()
                img_obj["from_url"] = True
            else:
                img_obj["from_url"] = False
            self.report["images"]["posted_images"].append(img_obj)

    def parse_found_images(self):
        img_lists = ["self._sim_img_list", "self._src_img_list"]
        for img_list in img_lists:
            for img in eval(img_list):
                img_data = {
                    "display_photo_url": img.get_img_display_url(),
                    "ssim": 0,
                    "file_path": img.get_absolute_path(),
                    "website_url": img.get_img_origin_website_url(),
                    "website_name": img.get_website_name(),
                    "position": img.get_img_position(),
                    "img_extention": img.get_found_img_extention(),
                    "domain": img.get_domain(),
                    "tld": img.get_tld(),
                    "display_position": 0,
                    "points": 0,
                    "point_modules_detected": {} 
                }
                if img_list == "self._src_img_list":
                    img_type = "source_images"
                    img_data["resolution"] = img.get_img_resolution()
                else:
                    img_type = "similar_images"
                
                # portal is seen for the first time
                if img.get_domain() not in self.report["images"][img_type]:
                    self.report["images"][img_type][img.get_domain()] = {}
                    self.report["images"][img_type][img.get_domain()]["tld"] = img.get_tld()
                    self.report["images"][img_type][img.get_domain()]["count"] = 1
                    self.report["images"][img_type][img.get_domain()]["domain"] = img.get_domain()
                    self.report["images"][img_type][img.get_domain()]["website_name"] = img.get_website_name() 
                    self.report["images"][img_type][img.get_domain()]["images"] = [img_data]
                else:  
                    self.report["images"][img_type][img.get_domain()]["count"] += 1
                    self.report["images"][img_type][img.get_domain()]["images"].append(img_data)

    def parse_db_images(self):
        for img in self._db_img_list:
            self.report["images"]["database"].append({
                "display_photo_url": img.get_img_origin_website_url(),
                "website_url": img.get_img_origin_website_url(),
                "website_name": img.get_website_name(),
            })
       

    def init_report(self):
        self.report = {
            "status": "ok",
            "error_msg": "",
            "max_points": pm.max_points(),
            "baseline": {},
            "images": {
                "posted_images": [],
                "similar_images": {},
                "source_images": {},
                # "database": []
            }
        }
    
    def get_report(self):
        return self.report
