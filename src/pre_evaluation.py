import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize

from src.image import FOUND_IMAGE_TYPES


class PreEvaluation():

    def __init__(self, report, supporting_imgs=None):
        self.report = report
        self.supporting_imgs = supporting_imgs
        self.filter_images()

    def get_report(self):
        return self.report
    
    def filter_images(self):
        self.set_similarity()
    
    @staticmethod
    def calculate_ssim(img1_path, img2_path):
        print(f"Calculating SSIM between {img1_path} and {img2_path}")
        img1 = cv2.imread(img1_path, 0)
        img2 = cv2.imread(img2_path, 0)

        if img1.shape[0] * img1.shape[1] > img2.shape[0] * img2.shape[1]:
            img1, img2 = img2, img1

        resized_img1 = resize(img1, (img2.shape[0], img2.shape[1]), anti_aliasing=True, preserve_range=True)

        return ssim(resized_img1, img2, data_range=255)
    

    def set_similarity(self):

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
        
        highest_ssim_overall = 0 
        for portal, data in self.report["images"]["similar_images"].items():
            for img in data["images"]:
                img_highest_ssim = 0
                img_file_path = img["file_path"]
                for sim_img_path in sim_images_paths:
                    ssim = self.calculate_ssim(sim_img_path, img_file_path)
                    if ssim > img_highest_ssim:
                        img_highest_ssim = ssim
                    if ssim > highest_ssim_overall :
                        highest_ssim_overall = ssim
                # img["ssim"] = img_highest_ssim
                img["ssim"] = int(round(img_highest_ssim * 100, 0)) / 100 

        # self.report["ssim_threshold"] = int(round(highest_ssim_overall * 100, 0)) 
        ssim_rounded = int(round(highest_ssim_overall * 100, 0)) / 100
        self.report["ssim_threshold"] = ssim_rounded
