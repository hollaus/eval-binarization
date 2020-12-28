"""Evaluate the performance of document image binarization methods.

Measures the performance on a folder basis, given an input and a ground truth folder.
The performance measure is saved in the form of CSV file.
"""  

import subprocess
import re
import os
import glob
import cv2
import numpy as np
import tqdm
import errno
import dibco_measure
import f_measure
import argparse
import csv
import constants

def get_image_files(path):
    extensions = ('*.png', '*.tiff')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(path, ext)))
        
    return files

def convert_img(path_in, path_out):
    image = cv2.imread(path_in)
    fg = image[:,:,1]
    fg = 255 - fg
    path_name = os.path.join(path_out, os.path.basename(path_in))
    cv2.imwrite(path_name, fg)

    return path_name

class FolderMeasure:

    def __init__(self, path_img, path_gt, use_dibco_tool = False, path_dibco_bin = ''):
        self.path_img = path_img
        self.path_gt = path_gt
        self.use_dibco_tool = use_dibco_tool
        self.path_dibco_bin = os.path.join(path_dibco_bin, 'DIBCO_metrics.exe')

        # Assure that the binary file is existing:
        if (not os.path.exists(self.path_dibco_bin)):
            print('The DIBCO binary path is wrong. This path must contain a file named: DIBCO_metrics.exe')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path_dibco_bin)
            
        self.mean_fm = -1
        self.mean_precision = -1
        self.mean_recall = -1


    def batch_measure(self, fg_type: constants.FGType = constants.FGType.REGULAR):

        TYPE_GT = 0
        TYPE_PSEUDO_RECALL = 1
        TYPE_PSEUDO_PRECISION = 2
        PSEUDO_RECALL_POSTFIX = '_RWeights.dat'
        PSEUDO_PRECISION_POSTFIX = '_PWeights.dat'  

        def get_gt_file(gt_file_type):

            img_file_name = os.path.basename(img_name)
            
            if gt_file_type == TYPE_GT:
                path = os.path.join(self.path_gt, img_file_name)
            elif gt_file_type == TYPE_PSEUDO_RECALL:
                img_base_name = os.path.splitext(img_file_name)[0]
                path = os.path.join(self.path_gt, img_base_name + PSEUDO_RECALL_POSTFIX)
            elif gt_file_type == TYPE_PSEUDO_PRECISION:
                img_base_name = os.path.splitext(img_file_name)[0]
                path = os.path.join(self.path_gt, img_base_name + PSEUDO_PRECISION_POSTFIX)
            else:
                raise Exception('Unknown type')

            # Check if the file is existing:
            if (os.path.exists(path)):
                return path
            else:
                if (gt_file_type == TYPE_PSEUDO_PRECISION or gt_file_type == TYPE_PSEUDO_RECALL):
                    print('Missing a dibco weight file, please create it first with the GTConverter class.')
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        img_names = get_image_files(self.path_img)
        if not img_names:
            raise Exception('No image found.')

        img_name = ''
        results = []

        if (self.use_dibco_tool):
            dw = dibco_measure.DibcoWrapper(self.path_dibco_bin)
        else:
            fm = f_measure.PerformanceMeasure(self.path_img, self.path_gt)

        for img_name in img_names:
            if (self.use_dibco_tool):
                result = dw.calc(img_name, get_gt_file(TYPE_GT), get_gt_file(TYPE_PSEUDO_RECALL), get_gt_file(TYPE_PSEUDO_PRECISION))
            else:
                result = fm.calc(img_name, get_gt_file(TYPE_GT), fg_type)
            
            results.append(result)

        # Store the mean performance values:
        self.mean_fm = np.mean([r.fm for r in results])
        self.mean_recall = np.mean([r.recall for r in results])
        self.mean_precision = np.mean([r.precision for r in results])

class ImgConverter:

    def __init__(self, path_in, path_out, path_gt=''):
        """Initialize the converter. 
        In case of MSBin path_gt is required for encoding unknown regions."""
        self.path_in = path_in

        self.path_out = path_out
        self.path_gt = path_gt

    def batch_convert(self):
        files = get_image_files(self.path_in)
        if not files:
            print('No suitable file found.')
            return -1

        for f in files:
            convert_img(f, self.path_out)

class GTConverter:

    def __init__(self, path_in, path_out, path_dibco_bin):
        self.path_in = path_in
        self.path_out = path_out
        self.path_dibco_bin = os.path.join(path_dibco_bin, "BinEvalWeights.exe")

    def batch_convert(self):

        def save_weights():
            args = [self.path_dibco_bin, file_out_name]
            p = subprocess.Popen(args, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p.stdout.read().decode("utf8")
            done_msg = '\r\nStarting 7 stages procedure:\r\n1. Loading GT and CC Detection\r\n2. Skeleton and Contour\r\n3. Distance Weights for Recall\r\n4. Loading Inverted GT and CC Detection\r\n5. Skeleton\r\n6. Distance Weights for Precision\r\n7. Releasing Mem and Terminating\r\n'
            if (output != done_msg):
                print(output)

        files = get_image_files(self.path_in)
        if not files:
            print('No suitable file found.')
            return -1

        print('Calculating dibco weights...')
        for f in tqdm.tqdm(files):
            file_out_name = convert_img(f, self.path_out)
            save_weights()
            
def main():  

    parser = argparse.ArgumentParser()
    parser.add_argument("path_gt", help="path to the ground truth images")
    parser.add_argument("path_img", help="path to the result images")
    parser.add_argument("path_csv", help="path to the csv output file")
    parser.add_argument("-dt", "--dibco_tool", help="use dibco tool", action="store_true")
    parser.add_argument('--path_dibco_bin', nargs='?', const='', default='')
    parser.add_argument('--fg_type', nargs='?', const=0, default=0, type=int)
    parser.add_argument("-s", "--subfolders", help="evaluate subfolders", action="store_true")
    args = parser.parse_args()

    measures = []
    if args.subfolders:
        folders = glob.glob(os.path.join(args.path_img, '*\\'))
    else:
        folders = [args.path_img]

    for folder in tqdm.tqdm(folders):
        measure = FolderMeasure(folder, args.path_gt, args.dibco_tool, args.path_dibco_bin)
        measure.batch_measure(constants.map_fg_type(args.fg_type))    
        measures.append(measure)

    with open(args.path_csv, 'w', newline='') as csvfile:
        headers = [constants.HEADER_PATH_IMG, constants.HEADER_MEAN_FM, constants.HEADER_MEAN_PRECISION, constants.HEADER_MEAN_RECALL]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for measure in measures:
            writer.writerow({   constants.HEADER_PATH_IMG: measure.path_img, 
                                constants.HEADER_MEAN_PRECISION: measure.mean_precision,
                                constants.HEADER_MEAN_RECALL: measure.mean_recall,
                                constants.HEADER_MEAN_FM: measure.mean_fm})

if __name__ == "__main__":
    main()     
