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
        self.parse_db_images()
    
    def parse_posted_images(self):
        for img in self._posted_img_list:
            self.report["images"]["posted_images"].append({
                "display_photo_url": img.get_origin_img_url_link(),
                "ssim": 0,
                "file_path": img.get_absolute_path(),
                "website_url": "sus",
                "website_name": img.get_website_name(),
                "domain": img.get_domain(),
                "tld": img.get_tld(),
                "display_position": 0,
                "points": 0,
                "point_modules_detected": {} 
            })

    def parse_found_images(self):
        # group ads by domain
        for img in self._sim_img_list:
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
            if img.get_domain() not in self.report["images"]["similar_images"]:
                self.report["images"]["similar_images"][img.get_domain()] = {}
                self.report["images"]["similar_images"][img.get_domain()]["tld"] = img.get_tld()
                self.report["images"]["similar_images"][img.get_domain()]["count"] = 1
                self.report["images"]["similar_images"][img.get_domain()]["domain"] = img.get_domain()
                self.report["images"]["similar_images"][img.get_domain()]["website_name"] = img.get_website_name() 
                self.report["images"]["similar_images"][img.get_domain()]["images"] = [img_data]
            else:
                self.report["images"]["similar_images"][img.get_domain()]["count"] += 1
                self.report["images"]["similar_images"][img.get_domain()]["images"].append(img_data)
            
        for img in self._src_img_list:
            img_data = {
                "display_photo_url": img.get_img_display_url(),
                "ssim": 0,
                "file_path": img.get_absolute_path(),
                "website_url": img.get_img_origin_website_url(),
                "website_name": img.get_website_name(),
                "position": img.get_img_position(),
                "resolution": img.get_img_resolution(),
                "img_extention": img.get_found_img_extention(),
                "domain": img.get_domain(),
                "tld": img.get_tld(),
                "display_position": 0,
                "points": 0,
                "point_modules_detected": {} 
            }
            if img.get_domain() not in self.report["images"]["source_images"]:
                self.report["images"]["source_images"][img.get_domain()] = {}
                self.report["images"]["source_images"][img.get_domain()]["tld"] = img.get_tld()
                self.report["images"]["source_images"][img.get_domain()]["count"] = 1
                self.report["images"]["source_images"][img.get_domain()]["domain"] = img.get_domain()
                self.report["images"]["source_images"][img.get_domain()]["website_name"] = img.get_website_name() 
                self.report["images"]["source_images"][img.get_domain()]["images"] = [img_data]
            else:
                self.report["images"]["source_images"][img.get_domain()]["count"] += 1
                self.report["images"]["source_images"][img.get_domain()]["images"].append(img_data)

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
            "point_modules_severity": {},
            "max_points": pm.max_points(),
            "baseline": {},
            "images": {
                "posted_images": [],
                "similar_images": {},
                "source_images": {},
                "database": []
            }
        }
    
    def get_report(self):
        return self.report
