
"""
Scraper class to scrape images from advertisement websites

Author: Tomas Fratrik
"""

from urllib.parse import urlsplit 
import src.supported_websites as suppw

class Scraper():
    """
    Find corresponding advertisement website for url and scrape images
    from it and return them
    """

    @staticmethod
    def scrape_advertisement_images(url):
        parsed_url = urlsplit(url)
        netloc = parsed_url.netloc
        domain_split = netloc.split('.')
        # domain = domain_split[0]
        domain = '.'.join(domain_split[-2:])
        corresponding_class = suppw.portals_map.get(domain)
        if corresponding_class:
            return corresponding_class.scrape(url)
        else:
            return {"error": "Website not supported"}
        