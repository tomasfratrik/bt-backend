import cv2
import PIL 
from PIL import Image 
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize

from src.image import FOUND_IMAGE_TYPES




class PreEvaluation():

    def __init__(self, report):
        self.report = report
        self.filter_images()
    
    def get_report(self):
        return self.report
    
    def filter_images(self):
        # self.filter_redundant()
        # self.filter_unsimiliar_images()
        pass
    
    def filter_redundant(self):
        for img_type in FOUND_IMAGE_TYPES:
            unique_domains = []
            new_dict = []
            for img in self.report["images"][img_type]:
                if img["domain"] not in unique_domains:
                    unique_domains.append(img["domain"])
                    new_dict.append(img)
            self.report["images"][img_type] = new_dict
    
    def filter_unsimiliar_images(self):
        img_model = self.report["images"]["posted_images"][0]
        img_model_obj = cv2.imread(img_model["file_path"], 0)
        for img_type in FOUND_IMAGE_TYPES:
            for img_found in self.report["images"][img_type]:
                img_found_obj = cv2.imread(img_found["file_path"],0)
                resized_img_model = resize(img_model_obj, (img_found_obj.shape[0], img_found_obj.shape[1]), anti_aliasing=True, preserve_range=True)
                img_found["ssim"] = ssim(resized_img_model, img_found_obj, data_range=255)

        # set baseline on the worst 'ssim' in the sources
        worst_ssim = 1
        for img in self.report["images"]["source_images"]:
            if img["ssim"] < worst_ssim:
                worst_ssim = img["ssim"]
        self.report["baseline"]["ssim"] = worst_ssim
