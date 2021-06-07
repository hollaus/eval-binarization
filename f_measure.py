import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import constants
import math

class PerformanceResult:

    def __init__(self, img, gt, fg_type: constants.FGType = constants.FGType.REGULAR, invert_img = False):

        # # check if this is the output of the FCN:
        # if np.shape(img)[2] == 3:
        #     if (fg_type == constants.FGType.MSBIN_FG_1):
        #         img = (img[:,:,1] > 0) * 255

        if fg_type == constants.FGType.REGULAR:
            # Note: the images are passed in the form of DIBCO data (fg = 0, bg = 1)
            if invert_img:
                img = (255 - img) > 0
            else:
                img = img > 0
            gt = (255 - gt) > 0
            # gt = gt > 0
        else:
            # Mask out blue regions in the input image and in the gt:
            img = np.where(np.logical_and(gt[:,:,2] == 0, gt[:,:,0] == 255), 0, img)
            if invert_img:
                img = (255 - img) > 0
            else:
                img = img > 0
            if fg_type == constants.FGType.MSBIN_FG_1:
                gt = gt[:,:,1] == 255
            elif fg_type == constants.FGType.MSBIN_FG_2:
                gt = gt[:,:,1] == 122

        #     # gt = np.where(gt == 255, 1, 0)
        # elif fg_type == constants.FGType.MSBIN_FG_2:
        #     # raise Exception('The foreground type is not supported!')
        #     # # Mask out blue regions in the input image and in the gt:
        #     # img = np.where(np.logical_and(gt[:,:,2] == 0, gt[:,:,0] == 255), 0, img)
        #     # # Just evaluate the red ink, mask out the other color:
        #     # img = (255 - img) > 0
        #     b = 0
        # else:
        #     raise Exception('The foreground type is not supported!')

        # Exclude images if they do not have any positive - this should only happen for constants.FGType.MSBIN_FG_2:
        if np.sum(gt) == 0:
            self.recall = -1
            self.precision = -1
            self.fm = -1
            return

        tp_img = np.logical_and(img, gt)
        fp_img = np.logical_and(img, ~gt)
        fn_img = np.logical_and(~img, gt) 
        tn_img = np.logical_and(~img, ~gt)

        tp = np.sum(tp_img)
        fn = np.sum(fn_img)
        fp = np.sum(fp_img)
        tn = np.sum(tn_img)

        recall = tp / (tp + fn)
        if math.isnan(recall):
            recall = 0
        precision = tp / (tp + fp)
        if math.isnan(precision):
            precision = 0
        fm = 2 * recall * precision / (recall + precision)
        if math.isnan(fm):
            fm = 0

        nrfn = fn / (fn + tp)
        nrfp = fp / (fp + tn)
        nrm = (nrfn + nrfp) / 2
        
        self.recall = recall
        self.precision = precision
        self.fm = fm
        self.nrm = nrm

class PerformanceMeasure:

    def __init__(self, img_path, gt_path, invert_imgs = False):
        self.img_path = img_path
        self.gt_path = gt_path
        self.invert_imgs = invert_imgs

    def calc(self, img_name: str, gt_name: str, fg_type: constants.FGType = constants.FGType.REGULAR) -> PerformanceResult:

        img = cv2.imread(os.path.join(self.img_path, img_name), cv2.IMREAD_ANYCOLOR)
        if len(np.shape(img)) == 3 and np.shape(img)[2] == 3:
            if fg_type == constants.FGType.MSBIN_FG_1:
                img = img[:,:,1]
            elif fg_type == constants.FGType.MSBIN_FG_2:
                img = img[:,:,2]
            else:
                raise Exception('Foreground type is not supported!')

        # img = cv2.imread(os.path.join(self.img_path, img_name), cv2.IMREAD_GRAYSCALE)
        if fg_type == constants.FGType.REGULAR:
            # In case of MSTEx or Dibco convert the image to grayscale:
            gt = cv2.imread(os.path.join(self.gt_path, gt_name), cv2.IMREAD_GRAYSCALE)
        else:
            # In case of MSBin, the color information is required:
            gt = cv2.imread(os.path.join(self.gt_path, gt_name), cv2.IMREAD_COLOR)

        r = PerformanceResult(img, gt, fg_type, self.invert_imgs)
        return r

if __name__ == "__main__":
    img_path = 'D:\\msi\\ace_v2\\dibco_measure\\msbin\\test\\0.25_0_0'
    img_path = 'D:\\msi\\gmm\\params\\msbin\\train\\5_0.01'
    img_name = 'EA5.png'
    gt_path = 'C:\\cvl\\msi\\data\\msbin\\MSBin\\train\\labels\\'
    gt_name = 'EA5.png'
    pm = PerformanceMeasure(img_path, gt_path, invert_imgs=True)
    pm.calc(img_name, gt_name, constants.FGType.MSBIN_FG_1)  



       