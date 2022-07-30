import numpy as np
import json
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