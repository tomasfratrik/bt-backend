# import point_modules as pm
from .point_modules import *

class Baseline:
    def __init__(self, img_list):
        self._img_list = img_list
        self.set_TLD_baseline()
    
    def get_img_list(self):
        return self._img_list
    
    def set_TLD_baseline(self):
        tlds = {}
        img_list = self.get_img_list()
        # TLD: count
        for img in img_list:
            tld = img.get_tld()
            if tld in tlds:
                tlds[tld] += 1
            else:
                tlds[tld] = 1
        print(tlds)


class Evaluator:

    def __init__(self, posted_img_list, sim_img_list, src_img_list):
        self._posted_img_list = posted_img_list
        self._sim_img_list = sim_img_list
        self._src_img_list = src_img_list
        self._baseline = Baseline(posted_img_list + sim_img_list + src_img_list)
        for key, val in pm.points.items():
            eval(f'pm.{key}()')
            