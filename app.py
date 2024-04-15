import os
import json
import time

import concurrent.futures
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS
from grisa import Grisa

from src.scraper import Scraper
from src.format_parser import FormatParser
from src.pre_evaluation import PreEvaluation
from src.evaluator import Evaluator
from src.post_evaluation import PostEvaluation
from src.run_grisa import run_grisa
from src.image import PostedImage, FoundImage, SupportingImage
import src.utils as utils
import src.database as db

from src.timer import timeme

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
@timeme
def grisa():
    """
    Main server endpoint to run grisa
    
    Accepts url of file or file itself
    """

    if request.method == 'POST':
        LOCAL_DEV = False

        # start = time.time()
        if request.files.get('file'):
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'File has empty name'})
            img = PostedImage(file, filename=file.filename, url=False)
        elif request.json.get('selected_url'):
            url = request.json['selected_url']
            img = PostedImage(url, url=True)
            if img.get_status_code() != 200:
                return jsonify({'error': 'Image is not accesible by the host server'})

            # supporting_imgs_urls = request.json['urls']
            # supporting_imgs = [SupportingImage(url, url=True) for url in supporting_imgs_urls]
        else:
            return jsonify({'error': 'No file found'})
        output = run_grisa(img.get_absolute_path(), LOCAL_DEV)
        posted_img_list = [img]

        db_img_list = []

        if output is None:
            return jsonify({'error': 'No similar images found!'})
        elif 'error' in output:
            return jsonify(output)

        start = time.time()
        sim_img_list = [FoundImage(img) for img in output[0]]
        src_img_list = [FoundImage(img) for img in output[1]]

        def save_file_from_url(img):
            url = img.get_img_display_url()
            absolute_path = img.get_absolute_path()
            start = time.time()
            res = requests.get(url)
            end = time.time()
            print(f"Request for {url} took: {end - start}")
            img.set_status_code(res.status_code)
            if res.status_code == 200:
                with open(absolute_path, 'wb') as f:
                    f.write(res.content)

        # Save images using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(save_file_from_url, sim_img_list + src_img_list)

        for img in sim_img_list + src_img_list:
            img.find_img_extention()        

        end = time.time()

        # print(f"Creating image objects of similar and source took: {end - start} seconds")
        # exit(0)


        start = time.time()
        formated_output = FormatParser(posted_img_list=posted_img_list, 
                                       sim_img_list=sim_img_list, 
                                       src_img_list=src_img_list,
                                       db_img_list=db_img_list)        
        end = time.time()
        print(f"Formating output took: {end - start} seconds")
        
        pre_evaluation = PreEvaluation(formated_output.get_report())

        evaluator = Evaluator(pre_evaluation.get_report())
        evaluator.evaluate()

        post_evaluation = PostEvaluation(evaluator.get_report())

        utils.remove_images(posted_img_list + sim_img_list + src_img_list) 

        return jsonify(post_evaluation.get_report())


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
    # db.connect()
    # db.create_tables()
    app.run(debug=True)
    # db.close_connection()