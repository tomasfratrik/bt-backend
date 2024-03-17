from .points import points_map
from .tld import top_level_domain
from .sus_web import suspicious_website
from .resolution import resolution


def max_points():
    max_points = 0
    for module in points_map:
        max_points += points_map[module]["points"]
    return max_points