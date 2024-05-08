#!/usr/bin/env python3
"""
The main server endpoints

Author: Tomas Fratrik
"""

import os
import json
import concurrent.futures
from flask import Flask, jsonify, request
from flask_cors import CORS

from src.scraper import Scraper
from src.format_parser import FormatParser
from src.pre_evaluation import PreEvaluation
from src.evaluator import Evaluator
from src.post_evaluation import PostEvaluation
from src.run_grisa import run_grisa
from src.image import Image, PostedImage, FoundImage
import src.utils as utils


app = Flask(__name__)
CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
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
    Main server endpoint to run grisa
    
    Accepts url of file or file itself
    """

    if request.method == 'POST':
        LOCAL_DEV = False

        # parse the request
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
        else:
            return jsonify({'error': 'No file found'})
        
        output = run_grisa(img.get_absolute_path())

        posted_img_list = [img]
        sim_img_list = [FoundImage(img) for img in output[0]]
        src_img_list = [FoundImage(img) for img in output[1]]

        # Save images using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(Image.save_file_from_url, sim_img_list + src_img_list)

        # Format the outputs
        formated_output = FormatParser(posted_img_list=posted_img_list, 
                                       sim_img_list=sim_img_list, 
                                       src_img_list=src_img_list)        
        
        # Pre-evaluate the report
        pre_evaluation = PreEvaluation(formated_output.get_report())

        # Evaluate the report
        evaluator = Evaluator(pre_evaluation.get_report())
        evaluator.evaluate()

        # Post-evaluate the report
        post_evaluation = PostEvaluation(evaluator.get_report())

        # Remove stored iamges
        utils.remove_images(posted_img_list + sim_img_list + src_img_list) 

        report = post_evaluation.get_report()

        return report


@app.route('/grisa/set/country', methods=['POST'])
def report_change_country():
    """
    Endpoint to change the baseline countries of the report
    and make evaluation
    """

    country = request.json['country']
    report = request.json['report']

    evaluator = Evaluator(report)
    evaluator.evaluate_new_countries(country)

    post_evaluation = PostEvaluation(evaluator.get_report())
    report = post_evaluation.get_report()

    return report


if __name__ == '__main__':
    app.run(debug=True)
