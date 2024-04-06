import requests
from bs4 import BeautifulSoup
import json


class Nehnutelnosti_SK:

    @staticmethod
    def scrape(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Don't scrape directly from html,
        # scrape from JSON response data
        script_tag = soup.find('script', type='application/ld+json')

        json_data = json.loads(script_tag.string)

        json_data = json_data['@graph']
        for data in json_data:
            if data['@type'] == 'Product':
                product_data = data
                break
        
        images = product_data['image']

        return [img['url'] for img in images]



        