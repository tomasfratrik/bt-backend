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
        if img["from_url"] is False:
            break
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
    report = evaluate_based_on_tld_baseline(report, tld_baseline)
    report["baseline"]["tld"] = tld_baseline

    return report


def evaluate_based_on_tld_baseline(report, tld_baseline):
    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            if data["tld"] not in tld_baseline.keys() and data["tld"] in tld_countries:
                for img in data["images"]:
                    img["point_modules_detected"]["top_level_domain"] = points_map.get("top_level_domain")
                    img["points"] += points_map["top_level_domain"]["points"]
    
    if report["upload_type"] == "url":
        for img in report["images"]["posted_images"]:
            if img["tld"] not in tld_baseline.keys() and data["tld"] in tld_countries:
                img["point_modules_detected"]["top_level_domain"] = points_map.get("top_level_domain")
                img["points"] += points_map["top_level_domain"]["points"]

    return report


def change_country(report, country):
    if not report:
        return {"error": "No report given"}

    report = remove_current_evaluation(report)
    report = evaluate_based_on_tld_baseline(report, country)
    report["baseline"]["tld"] = country

    return report


def remove_current_evaluation(report):
    for img_type in FOUND_IMAGE_TYPES:
        for portal, data in report["images"][img_type].items():
            for img in data["images"]:
                if "top_level_domain" in img["point_modules_detected"]:
                    img["points"] -= points_map["top_level_domain"]["points"]
                    del img["point_modules_detected"]["top_level_domain"]

    for img in report["images"]["posted_images"]:
        if "top_level_domain" in img["point_modules_detected"]:
            img["points"] -= points_map["top_level_domain"]["points"]
            del img["point_modules_detected"]["top_level_domain"]

    return report