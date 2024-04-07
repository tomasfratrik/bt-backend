from .sus_web_utils import sus_websites
from .points import points_map
from src.image import IMAGE_TYPES, FOUND_IMAGE_TYPES

def suspicious_website(report=None):
    if not report:
        return {"error": "No report given"}
    
    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            if data["website_name"] in sus_websites:
                for img in data["images"]:
                    img["point_modules_detected"]["suspicious_website"] = points_map.get("suspicious_website")
                    img["points"] += points_map["suspicious_website"]["points"]

    for img in report["images"]["posted_images"]:
        if img["website_name"] in sus_websites:
            img["point_modules_detected"]["suspicious_website"] = points_map.get("suspicious_website")
            img["points"] += points_map["suspicious_website"]["points"]

    return report