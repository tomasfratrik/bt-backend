from flask import Flask, jsonify, request
from flask_cors import CORS
from src.scraper import Scraper
from run_grisa import run_grisa
import os

from grisa import Grisa
from src.image import PostedImage

app = Flask(__name__)
CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    """
    Test if the server is running
    """
    return jsonify('pong!')

@app.route('/get_images_from_url', methods=['POST'])
def get_images_from_url():
    """
    Endpoint to get images from a given url, if the site is supported
    """
    if request.method == 'POST':
        url = request.json['url']
        result = Scraper.scrape_advertisement_images(url)
        if "error" in result:
            return jsonify(result)

        return_format = {
            'website_url': url,
            'image_urls': result
        }
        return jsonify(return_format)


@app.route('/grisa/upload', methods=['POST', 'GET'])
def grisa():
    """
    Main server endnpoint to run grisa
    
    Accepts url of file or file itself
    """
    if request.method == 'POST':
        LOCAL_DEV = False

        if 'url' in request.json:
            url = request.json['url']
            img = PostedImage(url, url=True)
            if img.get_status_code() != 200:
                return jsonify({'error': 'Image is not accesible by the host server'})
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'File has empty name'})
            img = PostedImage(file, filename=file.filename, url=False)
        else:
            return jsonify({'error': 'No file found'})

        output = run_grisa(img.get_absolute_path(), LOCAL_DEV)
        img.remove()

        if output is None:
            return jsonify({'error': 'No similar images found'})
        elif 'error' in output:
            return jsonify(output)
        
        similiar_img_json, source_img_json = output

        return jsonify({'similiar_img': similiar_img_json, 'source_img': source_img_json})


@app.route('/grisa_test', methods=['GET'])
def grisa_test():
    """
    Endpoint to test if grisa is working
    """

    LOCAL_DEV = False
    grisa = Grisa()
    grisa.options_add_argument('--headless')
    grisa.options_add_argument('--no-sandbox')
    grisa.options_add_argument('--disable-dev-shm-usage')
    grisa.options_add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    try:
        grisa.set_driver_path("CHROMEDRIVER_PATH")
        grisa.set_binary_path("GOOGLE_CHROME_BIN")
        LOCAL_DEV = False
    except Exception as e:
        CHROMEDRIVER_PATH="./driver/chromedriver/chromedriver"
        grisa.set_driver_path(CHROMEDRIVER_PATH)
        LOCAL_DEV = True

    grisa.init_driver()
    relative_path = "grisa_test_img/house.jpeg"
    absolute_path = os.path.join(os.getcwd(), relative_path)
    grisa.run(absolute_path, accept_cookies=True, local_dev=LOCAL_DEV)
    page_source = grisa.get_page_source()
    similiar_img_json = grisa.scrape_similiar(page_source)
    grisa.driver_quit()
    return jsonify(similiar_img_json)



if __name__ == '__main__':
    app.run(debug=True)