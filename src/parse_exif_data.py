import os
import uuid
import requests
from PIL import Image
from io import BytesIO

from src.image import IMAGE_TYPES

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(CUR_DIR, 'tmp_exif')


class ParseExifData():

    def __init__(self, report):
        self.report = report
    
    def parse_exif_data(self):
        for img_type in IMAGE_TYPES:
            for img in self.report["images"][img_type]:
                exif_data = self.get_exif_data(img)
                img["exif_data"] = exif_data
        
        return self.report
    
    def get_exif_data(self, img):
        # img = Image.open(img["display_photo_url"])
        res = requests.get(img["display_photo_url"])
        if res.status_code != 200:
            return
        
        # exif_data = Image.open(BytesIO(res.content))._getexif()
        img = Image.open(BytesIO(res.content))
        exif_data = img._getexif()
        return exif_data
