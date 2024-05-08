"""
This module is used to detect if the image is from a suspicious portal.

Author: Tomas Fratrik
"""

from .sus_portal_utils import sus_portals, SPECIAL_TLDS
from .points import points_map
from src.image import FOUND_IMAGE_TYPES

def suspicious_portal(report=None):
    if not report:
        return {"error": "No report given"}
    
    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            # if f"{data['website_name']}.{data["tld"]}" in sus_portals:
            # if data["website_name"] in sus_portals:
            found = False
            for portal in sus_portals:
                group_domain = data['domain']
                if portal['portal'] not in group_domain:
                    continue 
                
                list_of_domains = [f"{portal['portal']}.{tld}" for tld in portal['tld']]

                for domain in list_of_domains:
                    if domain in group_domain:
                        found = True
                        break
                
                list_of_special_domains = [f"{portal['portal']}.{tld}"for tld in SPECIAL_TLDS]
                for domain in list_of_special_domains:
                    if domain in group_domain:
                        found = True
                        break
            if found:
                for img in data["images"]:
                    img["point_modules_detected"]["suspicious_portal"] = points_map.get("suspicious_portal")
                    img["points"] += points_map["suspicious_portal"]["points"]

    if report["upload_type"] == "url":
        for img in report["images"]["posted_images"]:
            if img["website_name"] in sus_portals:
                img["point_modules_detected"]["suspicious_portal"] = points_map.get("suspicious_portal")
                img["points"] += points_map["suspicious_portal"]["points"]

    return report