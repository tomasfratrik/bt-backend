import flask
import flask_cors
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from grisa import Grisa

app = flask.Flask(__name__)
flask_cors.CORS(app)

@app.route('/ping', methods=['GET'])
def index():
    return flask.jsonify('pong!')

if __name__ == '__main__':
    app.run(debug=True)