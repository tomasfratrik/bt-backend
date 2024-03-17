# Names have to correlate with module names

# points = {
#     "top_level_domain": 3,
#     "suspicious_website": 2,
#     "resolution": 1,
# }

points_map = {
    "top_level_domain": {
        "name": "Top Level Domain",
        "points": 3,
        "description": "Top level domain of the website is probably from different country than expected"
    },
    "suspicious_website": {
        "name": "Suspicious website",
        "points": 2,
        "description": "Website is known for having many fraudalent advertisements"
    },
    "resolution": {
        "name": "Resolution",
        "points": 1,
        "description": "Resolution of image found on website is lower than expected"
    },

}
