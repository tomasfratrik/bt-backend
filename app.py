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

@app.route('/grisa_test', methods=['GET', 'POST'])
def grisa_test():
    # PATH="./driver/chromedriver/chromedriver"
    grisa = Grisa()
    # grisa.set_driver_path(PATH)
    grisa.set_driver_path("CHROMEDRIVER_PATH")
    grisa.set_binary_path("GOOGLE_CHROME_BIN")
    grisa.init_driver()
    # relative_path = "audia6.png"
    relative_path = "house.jpeg"
    full_path = os.path.join(os.getcwd(), relative_path)
    # grisa.run(full_path, accept_cookies=True, local=True)
    grisa.run(full_path, accept_cookies=True)
    # grisa.run("https://im9.cz/sk/iR/importprodukt-orig/808/808fd902a98bc47d11d06a91f2af9424--mm2000x2000.jpg")
    # sleep(2)
    page_source = grisa.get_page_source()
    similiar_img_json = grisa.scrape_similiar(page_source)
    # grisa.go_to_source()
    # page_source = grisa.get_page_source()
    # source_img_json = grisa.scrape_source(page_source)
    # print(f"similiar_img_json: {similiar_img_json}")
    # print(100*"*")
    # print(f"source_img_json: {source_img_json}")
    grisa.driver_quit()
    # return similiar_img_json, source_img_json
    # print(f"similiar_img_json: {similiar_img_json}")
    return jsonify(similiar_img_json)


@app.route('/grisa', methods=['GET', 'POST'])
def grisa():
    if request.method == 'POST':
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
        grisa.set_driver_path("CHROMEDRIVER_PATH")
        grisa.set_binary_path("GOOGLE_CHROME_BIN")
        grisa.init_driver()
        grisa.run(absolute_path, accept_cookies=True, local=False)

        page_source = grisa.get_page_source()
        similiar_img_json = grisa.scrape_similiar(page_source)
        grisa.driver_quit()

        os.remove(absolute_path)
        print(f"similiar_img_json: {similiar_img_json}")
        return jsonify(similiar_img_json)

if __name__ == '__main__':
    app.run(debug=True)