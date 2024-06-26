"""
This module contains the Image class and its subclasses.

Author: Tomas Fratrik
"""

import os
import uuid
import requests
from urllib.parse import urlsplit
import imghdr


IMG_DIR = "images"
IMAGE_TYPES = ["posted_images", "similar_images", "source_images"]
FOUND_IMAGE_TYPES = ["similar_images", "source_images"] 
SOURCE_IMAGE_TYPES = ["source_images"]

class Image:
    
    def _parse_filename(self):
        self.set_original_img_extention(self.get_full_original_img_filename().split('.')[-1])
        self.set_img_filename_no_extention(self.get_full_original_img_filename().split('.')[0])
    
    def set_img_filename_no_extention(self):
        return self._name
    def set_img_filename_no_extention(self, name):
        self._name = name

    def get_original_img_extention(self):
        return self._extention
    def set_original_img_extention(self, extention):
        self._extention = extention
    
    def get_img_random_id(self):
        return self._img_random_id
    def set_img_random_id(self, img_random_id):
        self._img_random_id = img_random_id
    
    def set_relative_path(self):
        self._relative_path = os.path.join(IMG_DIR, self.get_generated_filename())
    def get_relative_path(self):
        return self._relative_path

    def set_absolute_path(self):
        self._absolute_path = os.path.join(os.getcwd(), self.get_relative_path())
    def get_absolute_path(self):
        return self._absolute_path

    def set_full_original_img_filename(self, name):
        self.original_filename = name
    def get_full_original_img_filename(self):
        return self.original_filename
    
    def set_img_description(self, description):
        self._description = description
    def get_img_description(self):
        return self._description
    
    def set_img_resolution(self, resolution):
        self._resolution = resolution
    def get_img_resolution(self):
        return self._resolution

    def parse_domain(self, url):
        parsed_url = urlsplit(url)
        netloc = parsed_url.netloc
        self._domain = netloc
        domain_split = self._domain.split('.')
        self._tld = domain_split[-1]
        self._website_name = domain_split[-2]

    def get_domain(self):
        return self._domain
    
    def get_website_name(self):
        return self._website_name
    def get_tld(self):
        return self._tld

    def set_img_file(self, file):
        self._file = file
    def get_img_file(self):
        return self._file

    def _generate_random_name(self):
        self.set_img_random_id(str(uuid.uuid4()))
        if self.from_url():
            self.set_original_img_extention(self._url_get_img_extention_from_link())
        self.set_generated_filename(f"{self.get_img_random_id()}.jpg")

    def set_generated_filename(self, name):
        self._generated_filename = name
    def get_generated_filename(self):
        return self._generated_filename
    
    def get_status_code(self):
        return self._status_code
    def set_status_code(self, status_code):
        self._status_code = status_code

    def from_url(self):
        return self._from_url

    def set_origin_img_url_link(self, url):
        self._url_link = url
    
    def get_origin_img_url_link(self):
        return self._url_link 

    def _url_get_img_extention_from_link(self):
        return self.get_origin_img_url_link().split('.')[-1]
    
    def get_image_data(self):
        return self._image_data

    def save_file(self):
        if self.from_url():
            url = self.get_origin_img_url_link()
            res = requests.get(url)
            self.set_status_code(res.status_code)
            if self.get_status_code() == 200:
                with open(self.get_absolute_path(), 'wb') as f:
                    f.write(res.content)
                    self._image_data = res.content
        else:
            self.get_img_file().save(self.get_absolute_path())

    def remove(self):
        os.remove(self.get_absolute_path())

    @staticmethod
    def save_file_from_url(img):
        url = img.get_img_display_url()
        absolute_path = img.get_absolute_path()
        res = requests.get(url)
        img.set_status_code(res.status_code)
        if res.status_code == 200:
            with open(absolute_path, 'wb') as f:
                f.write(res.content)
        img.find_img_extention()        
    


class PostedImage(Image):

    def __init__(self, img, filename=None, url=True):
        self._from_url = url
        if not url:
            self.set_img_file(img)
            self.set_full_original_img_filename(filename)
            self._parse_filename()
        else:
            self.set_origin_img_url_link(img)
            self.parse_domain(img)

        self._generate_random_name()
        self.set_relative_path()
        self.set_absolute_path()
        self.save_file()

class SupportingImage(PostedImage):
    pass

class FoundImage(Image):
    def __init__(self, img_obj={}):
        self._from_url = True
        self.set_img_description(img_obj.get('description'))
        self.set_img_display_url(img_obj.get('imageurl'))
        self.set_img_origin_website_url(img_obj.get('link'))
        # self.set_img_origin_website_name(img_obj.get('website'))
        self.set_img_position(img_obj.get('position'))
        self.set_img_resolution(img_obj.get('resolution'))
        self.parse_domain(self.get_img_origin_website_url())

        self.set_origin_img_url_link(self.get_img_display_url())

        self._generate_random_name()
        self.set_relative_path()
        self.set_absolute_path()
    
    def get_img_position(self):
        return self._position
    def set_img_position(self, position):
        self._position = position

    def set_img_origin_website_url(self, url):
        self._origin_website_url = url
    def get_img_origin_website_url(self):
        return self._origin_website_url

    def set_img_origin_website_name(self, website_name):
        self._origin_website_name = website_name
    def get_img_origin_website_name(self):
        return self._origin_website_name
    
    def set_img_display_url(self, url):
        self._display_url = url
    def get_img_display_url(self):
        return self._display_url
    
    def find_img_extention(self):
        image_format = imghdr.what(self.get_absolute_path()) 
        self.set_found_img_extention(image_format)
    def get_found_img_extention(self):
        return self._found_img_extention
    def set_found_img_extention(self, extention):
        self._found_img_extention = extention
    
    # this is just for saving the image
    def get_original_img_extention(self):
        return 'jpg'

    def _generate_random_name(self):
        self.set_img_random_id(str(uuid.uuid4()))
        self.set_generated_filename(f"{self.get_img_random_id()}.{self.get_original_img_extention()}")


class DatabaseImage(Image):
    def __init__(self, website_name, url_link, db_display_url, image_data):
        self._website_name = website_name
        self._url_link = url_link
        self._display_url = db_display_url
        self._image_data = image_data
        
    def get_website_name(self):
        return self._website_name
    def get_img_origin_website_url(self):
        return self._url_link
    def get_img_display_url(self):
        return self._display_url
    def get_image_data(self):
        return self._image_data
