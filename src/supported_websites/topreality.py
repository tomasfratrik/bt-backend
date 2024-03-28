import requests
from bs4 import BeautifulSoup


class CeskeReality:
    @staticmethod
    def scrape(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # image_tags = soup.find_all('img')
        #print htnml page
        print(soup.prettify())
        image_tags = soup.find_all('img', class_='slide-image')
        print(f"image_tags: {image_tags}")
        image_urls = [img['src'] for img in image_tags]
        print(f"image_urls: {image_urls}")

        # for i, url in enumerate(image_urls):
        #     image_urls[i] = f"https://www.reality.cz/photo/{image_urls[i].split('/')[2]}/{image_urls[i].split('/')[3]}"
        
        # image_urls = list(set(image_urls))

        return image_urls

        