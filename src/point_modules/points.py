"""
This module contains the points that can be awarded to a website.
 * Names have to correlate with module names

Author: Tomas Fratrik
"""

points_map = {
    "top_level_domain": {
        "name": "Top Level Domain",
        "points": 3,
        "needs_url": True,
        "description": "Top level domain of the website is probably "
                       "from a different country than expected"
    },
    "suspicious_portal": {
        "name": "Suspicious portal",
        "points": 2,
        "needs_url": True,
        "description": "Portal is known for having many fraudalent advertisements"
    },
    "resolution": {
        "name": "Resolution",
        "points": 1,
        "needs_url": False,
        "description": "Resolution of image found on website is lower than expected"
    },
    "extention": {
        "name": "Extention",
        "points": 1,
        "needs_url": False,
        "description": "Image extention is not common"
    },
}
