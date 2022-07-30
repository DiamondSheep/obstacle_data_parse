import os
import numpy as np
from utils import *
from scipy.optimize import linear_sum_assignment

if __name__ == "__main__":
    """
    prototxt_itmes = []
    dir_name = "data/images"
    for file_name in os.listdir(dir_name):
        prototxt_file_name = os.path.join(dir_name, file_name)
        prototxt_itmes = parse_prototxt_file(prototxt_file_name)
    """
    verbose = True
    dt_dir_name = "./data/me_dt"
    gt_dir_name = "./data/me_gt"
    
    for dt_file_name, gt_file_name in zip(os.listdir(dt_dir_name), os.listdir(gt_dir_name)):
        if verbose:
            print(dt_file_name)
        dt_json_file_name = os.path.join(dt_dir_name, dt_file_name)
        gt_json_file_name = os.path.join(gt_dir_name, gt_file_name)
        dt_items = parse_json_file(dt_json_file_name)
        gt_items = parse_json_file(gt_json_file_name)
        
        if "obstacles" not in dt_items.keys() or "objects" not in gt_items.keys():
            continue
        
        dt_pos_list = []
        dt_id_list = []
        gt_pos_list = []
        gt_id_list = []

        # get information by parsing json
        for dt_item, gt_item in zip(dt_items["obstacles"], gt_items["objects"]):
            # check item
            if type(dt_item) is not dict or type(gt_item) is not dict:
                continue
            if "obstacle_id" not in dt_item.keys() or "id" not in gt_item.keys():
                continue
            # get information
            dt_id = dt_item["obstacle_id"]
            dt_id_list.append(dt_id)
            dt_pos = dt_item["obstacle_pos"]
            dt_pos_list.append(dt_pos)

            gt_id = int(gt_item["id"])
            gt_id_list.append(gt_id)
            gt_pos = gt_item["position"]
            gt_pos_list.append(gt_pos)
            """
            if verbose:
                print(f"dt id: {dt_id}, gt id: {gt_id}")
                print(f"dt pos: {dt_pos}, gt pos: {gt_pos}")
            """
        
        if len(dt_pos_list) < 1:
            continue
        if len(dt_pos_list) == 1:
            error = compute_distance(dt_pos_list[0], gt_pos_list[0])
            if verbose:
                print(f"dt id: {dt_id_list[0]}, gt id: {gt_id_list[0]}, {gt_pos_list[0]}, error: {error}")
        cost_matrix = get_cost_matrix(dt_pos_list, gt_pos_list)
        dt_index, gt_index = linear_sum_assignment(cost_matrix)
        for di, gi in zip(dt_index, gt_index):
            error = cost_matrix[di][gi]
            dt_id = dt_id_list[di]
            gt_id = gt_id_list[gi]
            dt_pos_dict = dt_pos_list[di]
            gt_pos_dict = gt_pos_list[gi]
            if verbose:
                print(f"dt id: {dt_id}, gt id: {gt_id}, {gt_pos_dict['x']}, error: {error}, distance: {compute_distance(dt_pos_dict, gt_pos_dict)} horizontal distance: {compute_horizontal_distance(dt_pos_dict, gt_pos_dict)}")
                
