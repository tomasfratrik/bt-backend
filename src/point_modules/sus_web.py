from .sus_web_utils import sus_websites
from .points import points
from src.image import IMAGE_TYPES

def suspicious_website(report=None):
    if not report:
        return {"error": "No report given"}
    
    for img_type in IMAGE_TYPES:
        for img in report["images"][img_type]:
            if img["website_name"] in sus_websites:
                img["point_modules_detected"].append("suspicious_website")
                img["score"] += points["suspicious_website"]

    return report