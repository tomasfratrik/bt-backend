import requests
from bs4 import BeautifulSoup


class Reality:

    @staticmethod
    def scrape(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img', class_='nahled')
        image_urls = [img['src'] for img in image_tags]

        # now we have low resolution images, so change url to get full resolution
        # this we have /thumb/numbers_1/numbers_2_id.jpg
        # this we want https://www.reality.cz/photo/numbers_1/numbers_2_id.jpg
        for i, url in enumerate(image_urls):
            image_urls[i] = f"https://www.reality.cz/photo/{image_urls[i].split('/')[2]}/{image_urls[i].split('/')[3]}"
        
        # remove duplicates
        image_urls = list(set(image_urls))

        return image_urls

        