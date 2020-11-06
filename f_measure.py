import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

class PerformanceResult:

    def __init__(self, img, gt):
        # Note: the images are passed in the form of DIBCO data (fg = 0, bg = 1)
        # Invert the images for simplicity:
        img = (255 - img) > 0
        gt = (255 - gt) > 0

        tp_img = np.logical_and(img, gt)
        fp_img = np.logical_and(img, ~gt)
        fn_img = np.logical_and(~img, gt) 

        tp = np.sum(tp_img)
        fn = np.sum(fn_img)
        fp = np.sum(fp_img)

        recall = tp / (tp + fn)
        precision = tp / (tp + fp)
        fm = 2 * recall * precision / (recall + precision)
        
        self.recall = recall
        self.precision = precision
        self.fm = fm

class PerformanceMeasure:

    def __init__(self, img_path, gt_path):
        self.img_path = img_path
        self.gt_path = gt_path

    def calc(self, img_name: str, gt_name: str) -> PerformanceResult:

        img = cv2.imread(os.path.join(self.img_path, img_name), cv2.IMREAD_GRAYSCALE)
        gt = cv2.imread(os.path.join(self.gt_path, gt_name), cv2.IMREAD_GRAYSCALE)

        r = PerformanceResult(img, gt)
        return r


       