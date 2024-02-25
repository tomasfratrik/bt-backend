import os
import uuid
import requests
IMG_DIR = "images"


class Image:
    def __init__(self, img, filename=None, url=True):
        self._from_url = url
        if not url:
            self.set_file(img)
            self.set_original_filename(filename)
            self._parse_filename()
        else:
            self.set_url_link(img)

        self._generate_random_name()
        self.set_relative_path()
        self.set_absolute_path()
        self.save_file()

    def set_url_link(self, url):
        self._url_link = url
    
    def get_url_link(self):
        return self._url_link 
    
    def from_url(self):
        return self._from_url
        
    
    def set_file(self, file):
        self._file = file
    def get_file(self):
        return self._file
    
    def _parse_filename(self):
        self.set_extention(self.get_original_filename().split('.')[-1])
        self.set_name(self.get_original_filename().split('.')[0])
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
    
    def get_img_random_id(self):
        return self._img_random_id
    
    def set_img_random_id(self, img_random_id):
        self._img_random_id = img_random_id
    
    def _url_get_extention_from_link(self):
        return self.get_url_link().split('.')[-1]
    
    def _generate_random_name(self):
        self.set_img_random_id(str(uuid.uuid4()))
        if self.from_url():
            self.set_extention(self._url_get_extention_from_link())
        self.set_generated_filename(f"{self.get_img_random_id()}.{self.get_extention()}")
    
    def set_generated_filename(self, name):
        self._generated_filename = name
    
    def get_generated_filename(self):
        return self._generated_filename
    
    def set_relative_path(self):
        self._relative_path = os.path.join(IMG_DIR, self.get_generated_filename())
    
    def get_relative_path(self):
        return self._relative_path

    def set_absolute_path(self):
        self._absolute_path = os.path.join(os.getcwd(), self.get_relative_path())
    
    def get_absolute_path(self):
        return self._absolute_path

    def get_extention(self):
        return self._extention

    def set_extention(self, extention):
        self._extention = extention

    def set_original_filename(self, name):
        self.original_filename = name

    def get_original_filename(self):
        return self.original_filename
    
    def set_website_url(self, url):
        self._website_url = url
    
    def get_website_url(self):
        return self._website_url

    def set_website_name(self, name):
        self._website_name = name
    
    def get_website_name(self):
        return self._website_name

    def set_resolution(self, resolution):
        self._resolution = resolution
    
    def get_resolution(self):
        return self._resolution
    
    def set_img_url(self, url):
        self._img_url = url
    
    def get_img_url(self):
        return self._img_url
    
    def set_status_code(self, code):
        self._status_code = code
    
    def get_status_code(self):
        return self._status_code
    
    def save_file(self):
        if self.from_url():
            url = self.get_url_link()
            res = requests.get(url)
            self.set_status_code(res.status_code)
            if self.get_status_code() == 200:
                with open(self.get_absolute_path(), 'wb') as f:
                    f.write(res.content)
        else:
            self.get_file().save(self.get_absolute_path())

    def remove(self):
        os.remove(self.get_absolute_path())
    


class PostedImage(Image):
    pass


class FoundImage(Image):
    pass


class DatabaseImage(Image):
    pass
