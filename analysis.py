from utils import *

if __name__ == "__main__":
    """
    prototxt_itmes = []
    dir_name = "data/images"
    for file_name in os.listdir(dir_name):
        prototxt_file_name = os.path.join(dir_name, file_name)
        prototxt_itmes = parse_prototxt_file(prototxt_file_name)
    """
    ### Settings
    verbose = False
    dt_dir_name = "./data/me_dt"
    gt_dir_name = "./data/me_gt"
    csv_file_name = "./results/dis_error.csv"

    analysis(verbose, dt_dir_name, gt_dir_name, csv_file_name)
