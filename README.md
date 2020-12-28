# eval-binarization
Evaluate the performance of document image binarization methods.

Measures the performance on a folder basis, given an input and a ground truth folder.
The performance measure is saved in the form of CSV file.

## Main function:

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