import subprocess
import re
import os

class DibcoResult:

    def __init__(self):
        self.fm = -1
        self.precision = -1
        self.recall = -1
        self.pseudo_fm = -1
        self.pseudo_recall = -1
        self.pseudo_precision = -1
        self.drd = -1
        self.psnr = -1
        self.file_name = []
    
    def __str__(self):
        return self.file_name + ":\nFM: %f\np-FM: %f\nDRD: %f\nPSNR: %f\nR: %f\nP: %f\np-R: %f\np-P: %f" % (
            self.fm, self.pseudo_fm, self.drd, self.psnr, self.recall, self.precision, self.pseudo_recall, self.pseudo_precision)

class DibcoWrapper:

    IDX_FM = 0
    IDX_PSEUDO_FM = 1
    IDX_PSNR = 2
    IDX_DRD = 3
    IDX_RECALL = 4
    IDX_PRECISION = 5
    IDX_PSEUDO_RECALL = 6
    IDX_PSEUDO_PRECISION = 7

    # parameterized constructor 
    def __init__(self, path_binary: str): 
        self.path_binary = path_binary
        # self.weight_path = weight_path

    def calc(self, img_path: str, gt_path: str, recall_weight_path: str, precision_weight_path: str) -> DibcoResult:

        args = [self.path_binary, gt_path, img_path, recall_weight_path, precision_weight_path]
        p = subprocess.Popen(args, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.read().decode("utf8")
        # Replace the special characters:
        clean_output = re.sub("\t|\r", "", output)
        # Get a string list containing solely the values:
        values = re.findall(":(.*?)\n", clean_output)

        m = DibcoResult()
        m.fm = float(values[self.IDX_FM])
        m.pseudo_fm = float(values[self.IDX_PSEUDO_FM])
        m.psnr = float(values[self.IDX_PSNR])
        m.drd = float(values[self.IDX_DRD])
        m.recall = float(values[self.IDX_RECALL])
        m.precision = float(values[self.IDX_PRECISION])
        m.pseudo_recall = float(values[self.IDX_PSEUDO_RECALL])
        m.pseudo_precision = float(values[self.IDX_PSEUDO_PRECISION])

        # set the file name:
        m.file_name = os.path.basename(img_path)

        return m

def main():    
    
    metric_path = "C:\\cvl\\msi\\code\\eval\\dibco\\dibco_metrics\\DIBCO_metrics.exe"
    # weight_path = "C:\cvl\msi\code\eval\dibco\BinEvalWeights\\BinEvalWeights.exe"
    dibco = DibcoWrapper(metric_path)
    
    m = dibco.calc('PR_bin.bmp', 'PR_GT.tiff', 'PR_RWeights.dat', 'PR_PWeights.dat')
    print(m)

if __name__ == "__main__":
    main()