"""
Create baseline for the extention of the images and add points

Author: Tomas Fratrik
"""

from .points import points_map
from src.image import IMAGE_TYPES, FOUND_IMAGE_TYPES
from .extention_utils import ext_list


def baseline(report=None):
    if not report:
        return {"error": "No report given"}
    
    ext_dict= {}

    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            for img in data["images"]:
                ext = img["img_extention"]
                if ext in ext_dict:
                    ext_dict[ext] += 1
                else:
                    ext_dict[ext] = 1
    
    ext_baseline = {}
    for ext, count in ext_dict.items():
        if count == max(ext_dict.values()):
            ext_baseline[ext] = count

    return ext_baseline


def extention(report=None):
    if not report:
        return {"error": "No report given"}
    
    ext_baseline = baseline(report)

    baseline_exts = []
    for b_ext in ext_baseline.keys():
        for ext_group in ext_list:
            if b_ext in ext_group:
                baseline_exts += ext_group
    
    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            for img in data["images"]:
                if img["img_extention"] not in baseline_exts:
                    img["point_modules_detected"]["extention"] = points_map.get("extention")
                    img["points"] += points_map["extention"]["points"]
        
    return report