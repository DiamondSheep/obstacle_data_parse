import os
import numpy as np
import csv
import json
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.optimize import linear_sum_assignment
from prototxt_parser.prototxt import parse

def parse_prototxt_file(prototxt_file_name):
    items = []
    with open(prototxt_file_name, 'rb') as file_d:
        return parse(str(file_d.read()))
        
def parse_json_file(json_file_name):
    with open(json_file_name, 'rb') as file_d:
        return json.load(file_d)

def compute_distance(dt_pos, gt_pos):
    result = 0.0
    for key in dt_pos.keys():
        result += pow(dt_pos[key] - gt_pos[key], 2)
    return result

def compute_horizontal_distance(dt_pos, gt_pos):
    return pow(dt_pos['y'] - gt_pos['y'], 2)
        
def get_cost_matrix(dt_pos_list, gt_pos_list)->np.array:
    cost_matrix = []
    for dt_pos in dt_pos_list:
        distance_list = []
        for gt_pos in gt_pos_list:
            distance = compute_distance(dt_pos, gt_pos)
            distance_list.append(distance)
        cost_matrix.append(distance_list)
    return np.array(cost_matrix)

def save_csv(file_name, x, multi_row=False):
    with open(file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        if (multi_row):
            for i in x:
                writer.writerow(i)
        else:
            writer.writerow(x)

def visual(csv_data, x_label=None, y_label=None):
    sns.scatterplot(data, x_label, y_label)

def analysis(verbose = False, dt_dir_name = "./data/me_dt", gt_dir_name = "./data/me_gt", csv_file_name = "./results/dis_error.csv"):
    # Lists to save results 
    _distance = []
    _obs_error = []
    _obs_hor_error = []
    
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
            hor_error = compute_horizontal_distance(dt_pos_dict, gt_pos_dict)
            # load to results
            _distance.append(gt_pos_dict['x'])
            _obs_error.append(error)
            _obs_hor_error.append(hor_error)
            if verbose:
                print(f"dt id: {dt_id}, gt id: {gt_id}, {gt_pos_dict['x']}, error: {error}, distance: {compute_distance(dt_pos_dict, gt_pos_dict)} horizontal distance: {hor_error}")
    
    save_csv(csv_file_name, [_distance, _obs_error])