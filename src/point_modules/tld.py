from .tld_utils import tld_countries
from .points import points
from src.image import IMAGE_TYPES

def set_baseline(images):
    tld_dict = {}
    for img_type in IMAGE_TYPES:
        for img in images[img_type]:
            tld = img["tld"]
            if tld in tld_dict:
                tld_dict[tld] += 1
            else:
                tld_dict[tld] = 1

    # filtrate tld dict to only have country tlds
    for tld in list(tld_dict.keys()):
        if tld not in tld_countries:
            del tld_dict[tld]

    # put tu baseline list of all tlds with the highest same count
    tld_baseline = []
    for tld, count in tld_dict.items():
        if count == max(tld_dict.values()):
            formated_tld = { f"{tld}": tld_countries.get(tld) }
            tld_baseline.append(formated_tld)
    
    return tld_baseline


def top_level_domain(report=None):
    if not report:
        return {"error": "No report given"}

    tld_baseline = set_baseline(report["images"])
    report["baseline"]["tld"] = tld_baseline

    for img_type in IMAGE_TYPES:
        for img in report["images"][img_type]:
            if img["tld"] in tld_countries:
                continue
            if img["tld"] not in report["baseline"]["tld"]:
                img["point_modules_detected"].append("top_level_domain")
                img["score"] += points["top_level_domain"]

    return report