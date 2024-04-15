import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize

from src.image import FOUND_IMAGE_TYPES

from src.timer import timeme


class PreEvaluation():

    def __init__(self, report, supporting_imgs=None):
        self.report = report
        self.supporting_imgs = supporting_imgs
        self.set_orgin_images()
        self.filter_images()
    
    def set_orgin_images(self):
        self.orig_img_paths = []
        self.orig_img_paths.append(self.report["images"]["posted_images"][0]["file_path"])
        if self.supporting_imgs:
            for img in self.supporting_imgs:
                # self.orig_img_paths.append(img["file_path"])
                self.orig_img_paths.append(img.get_absolute_path())


    def get_report(self):
        return self.report
    
    @timeme
    def filter_images(self):
        self.filter_unsimiliar_images()
    
    def filter_redundant(self):
        for img_type in FOUND_IMAGE_TYPES:
            unique_domains = []
            new_dict = []
            for img in self.report["images"][img_type]:
                if img["domain"] not in unique_domains:
                    unique_domains.append(img["domain"])
                    new_dict.append(img)
            self.report["images"][img_type] = new_dict
    
    @staticmethod
    def calculate_ssim(img1_path, img2_path):
        img1 = cv2.imread(img1_path, 0)
        img2 = cv2.imread(img2_path, 0)

        if img1.shape[0] * img1.shape[1] > img2.shape[0] * img2.shape[1]:
            img1, img2 = img2, img1

        resized_img1 = resize(img1, (img2.shape[0], img2.shape[1]), anti_aliasing=True, preserve_range=True)

        return ssim(resized_img1, img2, data_range=255)
    

    def filter_unsimiliar_images(self):

        img_orig_file_path = self.report["images"]["posted_images"][0]["file_path"]
        sim_images_paths = []
        sim_images_paths.append(img_orig_file_path)
        for portal, data in self.report["images"]["source_images"].items():
            for img in data["images"]:
                img_file_path = img["file_path"]
                ssim = self.calculate_ssim(img_orig_file_path, img_file_path)
                img["ssim"] = ssim
                if ssim < 0.5:
                    sim_images_paths.append(img_file_path)
        
        portals_to_delete = []
        for portal, data in self.report["images"]["similar_images"].items():
            new_list = []
            for img in reversed(data["images"]):
                delete = True
                img_file_path = img["file_path"]
                for sim_img_path in sim_images_paths:
                    ssim = self.calculate_ssim(sim_img_path, img_file_path)
                    if ssim > 0.35:
                        delete = False
                        break
                if not delete:
                    new_list.append(img)
            if not new_list:
                portals_to_delete.append(portal)
            else:
                data["images"] = new_list
                data["count"] = len(new_list)
        for portal in portals_to_delete:
            del self.report["images"]["similar_images"][portal]
