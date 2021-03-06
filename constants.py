from enum import Enum

def map_fg_type(fg_type: int):
    if fg_type == 0:
        return FGType.REGULAR
    elif fg_type == 1:
        return FGType.MSBIN_FG_1
    elif fg_type == 2:
        return FGType.MSBIN_FG_2
    else:
        raise Exception('The input number given cannot be mapped to an FGType.')

class FGType(Enum):
    """
    FGType defines the foreground types in ground truth images.

    This class gives us the capability to deal with the special foreground classes in the MSBin dataset, which contains two foreground classes.
    """
    # This foreground is the default for regular ground truth images - as in Dibco or MSTEx
    REGULAR = 0
    # This is the dominant foreground class in MSBin:
    MSBIN_FG_1 = 1
    # This is the second foreground class in MSBin:
    MSBIN_FG_2 = 2
    # This is the foreground class in MSTEx colored green
    MSTEX_FG_GREEN = 3

HEADER_PATH_IMG = 'path_img'
HEADER_PRECISION = 'precision'
HEADER_FM = 'fm'
HEADER_RECALL = 'recall'
HEADER_DRD = 'drd'
HEADER_PSEUDO_FM = 'pseudo_fm'
HEADER_PSEUDO_RECALL = 'pseudo_recall'
HEADER_PSEUDO_PRECISION = 'pseudo_precision'
HEADER_PSNR = 'psnr'
HEADER_NRM = 'nrm'