from urllib.parse import urlsplit 
from .supported_websites import *

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
        if domain_split[0] == 'www':
            domain = domain_split[1]
        else:
            domain = domain_split[0]
        corresponding_class = websites_map.get(domain)
        if corresponding_class:
            return corresponding_class.scrape(url)
        else:
            return {"error": "Website not supported"}
        