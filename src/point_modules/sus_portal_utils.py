"""
This module contains the list of suspicious portals and their top-level domains.

Author: Tomas Fratrik
"""

SPECIAL_TLDS =  ["com.au", "com.br", "com.mx", "com.ar", "com.co", "com.pe", "com.eg", 
            "com.sa", "com.tr", "com.ua", "com.vn", "com.sg", "com.my",
            "com.hk", "com.tw", "com.ph", "com.id", "com.jp", "com.kr",
            "com.th", "com.cn", "com.ru"]

sus_portals = [
    {
        "portal": "booking",
        "tld": ["com"]
    },
    {
        "portal": "airbnb",
        "tld": ["com", "be", "ie", "pl", "de", "fi", "ca", "it", "fr", "es", "co.uk", "ie", "nl"]
    },
    {
        "portal": "zillow",
        "tld": ["com"]
    },
    {
        "portal": "craigslist",
        "tld": ["org"]
    }
]
