from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from grisa import Grisa

app = Flask(__name__)
CORS(app)
IMG_DIR = "images"

@app.route('/ping', methods=['GET'])
def index():
    return jsonify('pong!')

@app.route('/grisa_test', methods=['GET'])
def grisa_test():
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


@app.route('/grisa', methods=['GET', 'POST'])
def grisa():
    if request.method == 'POST':
        LOCAL_DEV = False
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # get image extension
        extention = file.filename.split('.')[-1]
        img_random_id = str(uuid.uuid4())
        img_new_name = f"{img_random_id}.{extention}"
        relative_path = os.path.join(IMG_DIR, img_new_name)
        absolute_path = os.path.join(os.getcwd(), relative_path)
        file.save(absolute_path)

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
        grisa.run(absolute_path, accept_cookies=True, local_dev=LOCAL_DEV)

        page_source = grisa.get_page_source()
        similiar_img_json = grisa.scrape_similiar(page_source)
        grisa.driver_quit()

        os.remove(absolute_path)
        print(f"similiar_img_json: {similiar_img_json}")
        return jsonify(similiar_img_json)

if __name__ == '__main__':
    app.run(debug=True)