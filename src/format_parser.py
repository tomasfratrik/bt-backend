from src.image import Image

class FormatParser():

    report = {}
    _posted_img_list = []
    _sim_img_list = []
    _src_img_list = []

    @classmethod
    def __init__(cls, posted_img_list=[], sim_img_list=[], src_img_list=[]):
        cls._posted_img_list = posted_img_list
        cls._sim_img_list = sim_img_list
        cls._src_img_list = src_img_list
        cls.init_report()
        cls.parse_posted_images()
        cls.parse_found_images()
    
    @classmethod
    def parse_posted_images(cls):
        print(f"POSTED LIST: {cls._posted_img_list}")
        print(f"POSTED LIST TYPE: {type(cls._posted_img_list)} ")
        for img in cls._posted_img_list:
            cls.report["images"]["posted_images"].append({
                "display_photo_url": img.get_origin_img_url_link(),
                "origin_website_url": img.get_origin_img_url_link(),
                "tld": img.get_tld(),
                "display_position": 0,
                "score": 0,
                "point_modules_detected": []
            })
    @classmethod
    def parse_found_images(cls):
        for img in cls._sim_img_list:
            cls.report["images"]["similar_images"].append({
                "display_photo_url": img.get_img_display_url(),
                "origin_website_url": img.get_img_origin_website_url(),
                "origin_website_name": img.get_img_origin_website_name(),
                "position": img.get_img_position(),
                "tld": img.get_tld(),
                "display_position": 0,
                "score": 0,
                "point_modules_detected": []
            })
        for img in cls._src_img_list:
            cls.report["images"]["source_images"].append({
                "display_photo_url": img.get_img_display_url(),
                "origin_website_url": img.get_img_origin_website_url(),
                "origin_website_name": img.get_img_origin_website_name(),
                "position": img.get_img_position(),
                "tld": img.get_tld(),
                "display_position": 0,
                "score": 0,
                "point_modules_detected": []
            })

    @classmethod
    def init_report(cls):
        cls.report = {
            "status": "ok",
            "error_msg": "",
            "point_modules_severity": {},
            "images": {
                "posted_images": [],
                "similar_images": [],
                "source_images": [],
                "database": []
            }
        }
