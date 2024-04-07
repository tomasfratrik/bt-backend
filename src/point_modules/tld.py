from .tld_utils import tld_countries
from .points import points_map
from src.image import IMAGE_TYPES, FOUND_IMAGE_TYPES

def set_baseline(images):
    tld_dict = {}
    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in images[img_type].items():
            tld = data["tld"]
            if tld in tld_dict:
                tld_dict[tld] += 1
            else:
                tld_dict[tld] = 1
    for img in images["posted_images"]:
        tld = img["tld"]
        if tld in tld_dict:
            tld_dict[tld] += 1
        else:
            tld_dict[tld] = 1

    # filtrate tld dict to only have country tlds
    for tld in list(tld_dict.keys()):
        if tld not in tld_countries:
            del tld_dict[tld]

    tld_baseline = {}
    for tld, count in tld_dict.items():
        if count == max(tld_dict.values()):
            tld_baseline[tld] = tld_countries.get(tld)
    
    return tld_baseline


def top_level_domain(report=None):
    if not report:
        return {"error": "No report given"}

    tld_baseline = set_baseline(report["images"])
    report["baseline"]["tld"] = tld_baseline

    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            if data["tld"] not in tld_baseline.keys():
                for img in data["images"]:
                    img["point_modules_detected"]["top_level_domain"] = points_map.get("top_level_domain")
                    img["points"] += points_map["top_level_domain"]["points"]
    
    for img in report["images"]["posted_images"]:
        if img["tld"] not in tld_baseline.keys():
            img["point_modules_detected"]["top_level_domain"] = points_map.get("top_level_domain")
            img["points"] += points_map["top_level_domain"]["points"]

    return report