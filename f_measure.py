import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import constants

class PerformanceResult:

    def __init__(self, img, gt, fg_type: constants.FGType = constants.FGType.REGULAR):
        if fg_type == constants.FGType.REGULAR:
            # Note: the images are passed in the form of DIBCO data (fg = 0, bg = 1)
            # Invert the images for simplicity:
            img = (255 - img) > 0
            gt = (255 - gt) > 0
        elif fg_type == constants.FGType.MSBIN_FG_1:
            # Mask out blue regions in the input image and in the gt:
            img = np.where(np.logical_and(gt[:,:,2] == 0, gt[:,:,0] == 255), 0, img)
            img = (255 - img) > 0
            img = img > 0
            gt = gt[:,:,1] == 255
            # gt = np.where(gt == 255, 1, 0)
        elif fg_type == constants.FGType.MSBIN_FG_2:
            raise Exception('The foreground type is not supported!')
            # # Mask out blue regions in the input image and in the gt:
            # img = np.where(np.logical_and(gt[:,:,2] == 0, gt[:,:,0] == 255), 0, img)
            # # Just evaluate the red ink, mask out the other color:
            # img = (255 - img) > 0

        else:
            raise Exception('The foreground type is not supported!')

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

    def calc(self, img_name: str, gt_name: str, fg_type: constants.FGType = constants.FGType.REGULAR) -> PerformanceResult:

        img = cv2.imread(os.path.join(self.img_path, img_name), cv2.IMREAD_GRAYSCALE)
        if fg_type == constants.FGType.REGULAR:
            # In case of MSTEx or Dibco convert the image to grayscale:
            gt = cv2.imread(os.path.join(self.gt_path, gt_name), cv2.IMREAD_GRAYSCALE)
        else:
            # In case of MSBin, the color information is required:
            gt = cv2.imread(os.path.join(self.gt_path, gt_name), cv2.IMREAD_COLOR)

        r = PerformanceResult(img, gt, fg_type)
        return r

if __name__ == "__main__":
    img_path = 'D:\\msi\\ace_v1\\stages_eval\\msbin\\stage_1\\'
    img_name = 'BT3.png'
    gt_path = 'C:\\cvl\\msi\\data\\msbin\\MSBin\\train\\labels\\'
    gt_name = 'BT3.png'
    pm = PerformanceMeasure(img_path, gt_path)
    pm.calc(img_name, gt_name, constants.FGType.MSBIN_FG_1)  



       