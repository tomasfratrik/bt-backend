from .points import points_map
from .extention import extention
from .tld import top_level_domain
from .resolution import resolution
from .sus_portal import suspicious_portal


def max_points():
    max_points = 0
    for module in points_map:
        max_points += points_map[module]["points"]
    return max_points