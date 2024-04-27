from .sus_portal_utils import sus_portals
from .points import points_map
from src.image import FOUND_IMAGE_TYPES

def suspicious_portal(report=None):
    if not report:
        return {"error": "No report given"}
    
    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            # if data["website_name"] in sus_portals:
            if f"{data['website_name']}.{data["tld"]}" in sus_portals:
                for img in data["images"]:
                    img["point_modules_detected"]["suspicious_portal"] = points_map.get("suspicious_portal")
                    img["points"] += points_map["suspicious_portal"]["points"]

    for img in report["images"]["posted_images"]:
        if img["website_name"] in sus_portals:
            img["point_modules_detected"]["suspicious_portal"] = points_map.get("suspicious_portal")
            img["points"] += points_map["suspicious_portal"]["points"]

    return report