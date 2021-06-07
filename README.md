# MSBin Dataset

This dataset is named _MSBin_ which stands for MultiSpectral Document Binarization. The dataset is dedicated to the (document image) binarization of multispectral images. The dataset is introduced in [[Hollaus et al. 2019]](#[Hollaus-et-al.-2019]).

## Download
The dataset is on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3257366.svg)](https://doi.org/10.5281/zenodo.3257366)

Note that this is the second version of the dataset, where 10 images are removed from the test set, because they were too varying from the training set. The results obtained on the first version can be found in  [[Hollaus et al. 2019]](#[Hollaus-et-al.-2019]).

## Folder structure

    ├── train                   # Training set
    │   ├── images              # Input images
    │   ├── labels              # Ground-truth encoding three classes
    │   └── dibco_labels        # Ground-truth according to DIBCO scheme
    │       ├── fg_1            # Foreground 1 (main foreground) 
    │       └── fg_2            # Foreground 2 (red ink)
    ├── test                   # Training set
    │   ├── images              # Test images
    │   ├── labels              # Ground-truth encoding three classes
    │   └── dibco_labels        # Ground-truth according to DIBCO scheme
    │       ├── fg_1            # Foreground 1 (main foreground) 
    │       └── fg_2            # Foreground 2 (red ink)    

The encoding for the ground-truth images in the _labels_ folders is detailed below.
The encoding in the _dibco_labels_ folders follows the _DIBCO_ convention: Black is foreground and white is background. Additionally, the weights for Pseudo-Recall and Pseudo-Precision [[XXX]](XXX) are included in these folders.

## Usage

<!-- TODO: requirements -->

File:
```binar_eval.py```


```bash
usage: binar_eval.py [-h] [-dt] [--path_dibco_bin [PATH_DIBCO_BIN]]
                     [--fg_type [FG_TYPE]] [-s]
                     path_gt path_img path_csv

positional arguments:
  path_gt               path to the ground truth images
  path_img              path to the result images
  path_csv              path to the csv output file

optional arguments:
  -h, --help            show this help message and exit
  -dt, --dibco_tool     use dibco tool
  --path_dibco_bin [PATH_DIBCO_BIN]
  --fg_type [FG_TYPE]
  -s, --subfolders      evaluate subfolders
```

<!-- TODO: Examples -->


## Naming Convention
The folders containing the training and test data contain subdirectories named _images_ and _labels_. The multispectral images contained in the _images_ folder are named with the following naming convention, whereby an underscore separates the different elements:

``
BookId_PageId_WavelengthId.png
``

whereby ``BookId`` describes the type of manuscript and is either _EA_ or _BT_. ``PageId`` is a digit, which can be mapped to a certain page in the corresponding book. ``WavelengthId`` is also a number that depicts the spectral range at which the image was acquired.

The mapping is provided in the following table, together with the exposure time that was used for the certain spectral ranges.


| ``WavelengthId``        | Illumination / Spectral Range           | Exposure time (in sec.)  |
| -------------: |:-------------:| -----|
| 0  | White light (broadband)           | 0.0666 |
| 1  | 365 nm (UV flurorescence)   | 10 |
| 2  | 450 nm (narrowband)               | 0.125 |
| 3  | 465 nm (narrowband)               | 0.1 |
| 4  | 505 nm (narrowband)               | 0.05 |
| 5  | 535 nm (narrowband)               | 0.0666 |
| 6  | 570 nm (narrowband)               | 0.1666 |
| 7  | 625 nm (narrowband)               | 0.0333 |
| 8  | 700 nm (narrowband)               | 0.1666 |
| 9  | 780 nm (narrowband)               | 0.2 |
| 10 | 780 nm (narrowband)               | 0.2 |
| 11 | 870 nm (narrowband)               | 0.5 |

For the ground truth images contained in the _labels_ folder, the following naming convention is used:

``
BookId_PageId.png
``

## Imaged Books
The dataset is comprised of 120 image portions, whereby the training and test sets contain 80 and 40 multispectral images, respectively. 
The portions are taken from two medieval manuscripts, named _Bitola-Triodion ABAN 38_ (hereafter named _BT_) and _Enina-Apostolus NBMK 1144_ (hereafter named _EA_). 
The latter one is in a worse condition than the first one, since it contains partially damaged folios and faded-out ink. 
Each multispectral image in the dataset has been taken from a different manuscript folio.

## Classes
Both manuscripts contain cyrillic text written in iron gall ink.
The corresponding foreground regions are colored black or brown.
This class is hereafter denoted as _FG_.
The document background class is abbreviated with _BG_.
Additionally, a subset of the images contain characters that are written in red ink, denoted as _FGR_.
The test set contains certain regions that are labeled as uncertain regions _UR_ in the ground truth images. 
_UR_ denote regions, that could not be clearly identified as belonging to _FG_, _FGR_ or _BG_.
These regions are excluded from the evaluation:
Therefore, in the evaluation they are marked as belonging to the background - both in the ground truth images as well as in the resulting images.
The training set does not contain uncertain regions, in order to allow for a training on entire image patches.

## Groundtruth
The ground truth contains a color-coded image for each multispectral image, whereby the colors encode different classes - as listed in the following table.

| Label        | Description           | RGB color code  |
| ------------- |:-------------:| -----:|
| _FG_  | Main text         | (255, 255, 255) |
| _FGR_ | Red ink           | (122, 122, 122) |
| _BG_  | Background        | (0, 0, 0)       |
| _UR_  | Uncertain region  | (0, 0, 255)     |

## Image Acquisition

The image acquisition was fulfilled in the course of the [CIMA (Centre of Image and Material Analysis in Cultural Heritage)](https://cima.or.at) project.

The images contained in the _MSBin_ dataset have been captured with a Phase One IQ260 achromatic camera with a resolution of 60 megapixels. 
A multispectral LED panel provides 11 different narrow-band spectral ranges from 365 nm until 940 nm. 
An UltraViolet (UV) long pass filter has been used in combination with UV light (365 nm) to acquire UV fluorescence images.
For the acquisition of the remaining 10 spectral ranges no optical filter has been used.
Additionally, a broadband LED illumination has been used to acquire white light images.
Therefore, each multispectral image consists of 12 channels.

For each spectral range an individual exposure time has been determined in order to maximize the spectral range. 
These individual exposure times for the spectral ranges remained unchanged during the acquisition, because otherwise the spectral variability of the target classes would have been increased.
The images have been registered onto each other with a multimodal image registration algorithm
[[Heinrich et al. 2012]](#[heinrich-et-al.-2012]), in order to correct optical distortions.



## References
### [Hollaus et al. 2019]
F. Hollaus, S. Brenner and R. Sablatnig: "CNN based Binarization of MultiSpectral Document Images". To appear in: International Conference on Document Analysis and Recognition (ICDAR), 2019.
### [Heinrich et al. 2012]
M. P. Heinrich, M. Jenkinson, M. Bhushan, T. Matin, F. V. Gleeson, S. M. Brady, and J. A. Schnabel, “MIND: Modality independent neighbourhood descriptor for multi-modal deformable
registration”. Medical Image Analysis, vol. 16, no. 7, pp. 1423–1435, 2012

## eval-binarization
Evaluate the performance of document image binarization methods.

Measures the performance on a folder basis, given an input and a ground truth folder.
The performance measure is saved in the form of CSV file.

### Main function:

```binar_eval.py```


```bash
usage: binar_eval.py [-h] [-dt] [--path_dibco_bin [PATH_DIBCO_BIN]]
                     [--fg_type [FG_TYPE]] [-s]
                     path_gt path_img path_csv

positional arguments:
  path_gt               path to the ground truth images
  path_img              path to the result images
  path_csv              path to the csv output file

optional arguments:
  -h, --help            show this help message and exit
  -dt, --dibco_tool     use dibco tool
  --path_dibco_bin [PATH_DIBCO_BIN]
  --fg_type [FG_TYPE]
  -s, --subfolders      evaluate subfolders
```