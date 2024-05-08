""" 
This module is responsible for detecting resolution points in the images.
    
Author: Tomas Fratrik
"""

from .points import points_map

def set_baseline(images):
    cnt = 1
    sum_pixel = 0
    sumx = 0
    sumy = 0

    for portal, data in images["source_images"].items():
        for img in data["images"]:
            sumx += img["resolution"][0]
            sumy += img["resolution"][1]
            sum_pixel +=  img["resolution"][0] * img["resolution"][1]
            cnt += 1
    
    avgx = sumx / cnt
    avgy = sumy / cnt
    avg_pixel_cnt = sum_pixel / cnt
    return avg_pixel_cnt, avgx, avgy

def resolution(report=None):
    if not report:
        return {"error": "No report given"}

    avg_pixel_cnt, res_x, res_y = set_baseline(report["images"])
    
    report["baseline"]["resolution"] = {
        "average_pixel_count": avg_pixel_cnt,
        "resolution_x": res_x,
        "resolution_y": res_y
    }

    for portal, data in report["images"]["source_images"].items():
        for img in data["images"]:
            if img["resolution"][0] * img["resolution"][1] < avg_pixel_cnt:
                img["point_modules_detected"]["resolution"] = points_map.get("resolution")
                img["points"] += points_map["resolution"]["points"]

    return report