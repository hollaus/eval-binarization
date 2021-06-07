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
import math

def get_image_files(path):
    extensions = ('*.png', '*.tiff')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(path, ext)))
    
    # filter out pseudo images (these are just for probability visualization):
    files = [f for f in files if 'pseudo' not in f]
    return files

def convert_img(path_in, path_out):
    image = cv2.imread(path_in)
    fg = image[:,:,1]
    fg = 255 - fg
    path_name = os.path.join(path_out, os.path.basename(path_in))
    cv2.imwrite(path_name, fg)

    return path_name

class FolderMeasure:

    def __init__(self, path_img, path_gt, use_dibco_tool = False, path_dibco_bin = '', invert_imgs = False, save_single_results = True):
        self.path_img = path_img
        self.path_gt = path_gt
        self.use_dibco_tool = use_dibco_tool
        self.path_dibco_bin = os.path.join(path_dibco_bin, 'DIBCO_metrics.exe')
        self.invert_imgs = invert_imgs
        self.save_single_results = save_single_results

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
            fm = f_measure.PerformanceMeasure(self.path_img, self.path_gt, self.invert_imgs)


        # DIBCO computation tooks very long...
        # Therefore, show a progress button, to make it less boring :)
        if self.use_dibco_tool:
            for img_name in tqdm.tqdm(img_names):
                print(img_name)
                result = dw.calc(img_name, get_gt_file(TYPE_GT), get_gt_file(TYPE_PSEUDO_RECALL), get_gt_file(TYPE_PSEUDO_PRECISION))
                print(result)
                results.append(result)
                print("mean fm: " + str(np.mean([r.fm for r in results])))

            # Store the mean performance values:
            self.mean_fm = np.mean([r.fm for r in results])
            self.mean_recall = np.mean([r.recall for r in results])
            self.mean_precision = np.mean([r.precision for r in results])
            self.mean_psnr = np.mean([r.psnr for r in results])
            self.mean_pseudo_fm = np.mean([r.pseudo_fm for r in results])
            self.mean_drd = np.mean([r.drd for r in results])
            self.mean_pseudo_recall = np.mean([r.pseudo_recall for r in results])
            self.mean_pseudo_precision = np.mean([r.pseudo_precision for r in results])
            evaluated_img_names = img_names

        else:
            removed_img_names = ['BT44', 'BT50', 'EA0', 'EA1', 'EA47', 'EA59', 'EA60', 'EA62', 'EA63', 'EA64']
            evaluated_img_names = []
            for img_name in img_names:

                # TODO: remove this!
                img_base_name = os.path.splitext(os.path.basename(img_name))[0]
                if img_base_name in removed_img_names:
                    continue
                
                result = fm.calc(img_name, get_gt_file(TYPE_GT), fg_type)
                if result.fm == -1:
                    continue

                if math.isnan(result.fm):
                    print(img_name)

                results.append(result)
                evaluated_img_names.append(img_name)
            
            # Store the mean performance values:
            self.mean_fm = np.mean([r.fm for r in results])
            self.mean_recall = np.mean([r.recall for r in results])
            self.mean_precision = np.mean([r.precision for r in results])

        if self.save_single_results:
            if self.use_dibco_tool:
                self.img_names = evaluated_img_names
                self.fm = [r.fm for r in results]
                self.precision = [r.precision for r in results]
                self.recall = [r.recall for r in results]
                self.psnr = [r.psnr for r in results]
                self.drd = [r.drd for r in results]
                self.pseudo_recall = [r.pseudo_recall for r in results]
                self.pseudo_fm = [r.pseudo_fm for r in results]
                self.pseudo_precision = [r.pseudo_precision for r in results]
            else:
                self.img_names = evaluated_img_names
                self.fm = [r.fm for r in results]
                self.precision = [r.precision for r in results]
                self.recall = [r.recall for r in results]
                self.nrm = [r.nrm for r in results]

            
def main():  

    parser = argparse.ArgumentParser()
    parser.add_argument("path_gt", help="path to the ground truth images")
    parser.add_argument("path_img", help="path to the result images")
    parser.add_argument("path_csv", help="path to the csv output file")
    parser.add_argument("-dt", "--dibco_tool", help="use dibco tool", action="store_true")
    parser.add_argument('--path_dibco_bin', nargs='?', const='', default='')
    parser.add_argument('-fg_type', nargs='?', const=0, default=0, type=int)
    parser.add_argument("-s", "--subfolders", help="evaluate subfolders", action="store_true")
    parser.add_argument("-f", "--file_results", help="save results for each file", action="store_true")
    parser.add_argument("-i", "--invert_imgs", help="invert input images", action="store_true")
    args = parser.parse_args()

    measures = []
    if args.subfolders:
        folders = glob.glob(os.path.join(args.path_img, '*\\'))
    else:
        folders = [args.path_img]

    for folder in tqdm.tqdm(folders):
        measure = FolderMeasure(folder, args.path_gt, args.dibco_tool, args.path_dibco_bin, args.invert_imgs, True)
        measure.batch_measure(constants.map_fg_type(args.fg_type))    
        measures.append(measure)
        # This is a safety message to see if we got many wrong results...
        print(folder)
        tqdm.tqdm.write("Mean FM: %f" % measure.mean_fm)
        

    with open(args.path_csv, 'w', newline='') as csvfile:
        if args.dibco_tool:
            headers = [ constants.HEADER_PATH_IMG, constants.HEADER_FM, constants.HEADER_PRECISION, constants.HEADER_RECALL,
                        constants.HEADER_PSEUDO_FM, constants.HEADER_PSEUDO_PRECISION, constants.HEADER_PSEUDO_RECALL,
                        constants.HEADER_DRD, constants.HEADER_PSNR
                        ]            
        else:
            headers = [constants.HEADER_PATH_IMG, constants.HEADER_FM, constants.HEADER_PRECISION, constants.HEADER_RECALL, constants.HEADER_NRM]

        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for measure in measures:
            if args.dibco_tool:
                writer.writerow({   constants.HEADER_PATH_IMG: measure.path_img, 
                                    constants.HEADER_FM: measure.mean_fm,
                                    constants.HEADER_PRECISION: measure.mean_precision,
                                    constants.HEADER_RECALL: measure.mean_recall,
                                    constants.HEADER_PSEUDO_FM: measure.mean_pseudo_fm,
                                    constants.HEADER_PSEUDO_PRECISION: measure.mean_pseudo_precision,
                                    constants.HEADER_PSEUDO_RECALL: measure.mean_pseudo_recall,
                                    constants.HEADER_DRD: measure.mean_drd,
                                    constants.HEADER_PSNR: measure.mean_psnr
                                    })
            else:
                writer.writerow({   constants.HEADER_PATH_IMG: measure.path_img, 
                                    constants.HEADER_FM: measure.mean_fm,
                                    constants.HEADER_PRECISION: measure.mean_precision,
                                    constants.HEADER_RECALL: measure.mean_recall, 
                                    constants.HEADER_NRM: -1
                    })

            if args.file_results:
                # Add an empty row to distinguish between mean values and single values:
                writer.writerow({})

                if args.dibco_tool:
                    for (img_name, fm, precision, recall, pseudo_fm, pseudo_precision, pseudo_recall, drd, psnr) in zip(
                        measure.img_names, 
                        measure.fm, measure.precision, measure.recall, 
                        measure.pseudo_fm, measure.pseudo_precision, measure.pseudo_recall,
                        measure.drd, measure.psnr):
                        writer.writerow({   constants.HEADER_PATH_IMG: img_name, 
                                            constants.HEADER_FM: fm,
                                            constants.HEADER_PRECISION: precision,
                                            constants.HEADER_RECALL: recall,
                                            constants.HEADER_PSEUDO_FM: pseudo_fm,
                                            constants.HEADER_PSEUDO_PRECISION: pseudo_precision,
                                            constants.HEADER_PSEUDO_RECALL: pseudo_recall,
                                            constants.HEADER_DRD: drd,
                                            constants.HEADER_PSNR: psnr
                        })
                else:
                    for (img_name, fm, precision, recall, nrm) in zip(
                        measure.img_names, measure.fm, measure.precision, measure.recall, measure.nrm):
                        writer.writerow({   constants.HEADER_PATH_IMG: img_name, 
                                            constants.HEADER_FM: fm,
                                            constants.HEADER_PRECISION: precision,
                                            constants.HEADER_RECALL: recall,
                                            constants.HEADER_NRM: nrm
                        })
if __name__ == "__main__":
    main()     
