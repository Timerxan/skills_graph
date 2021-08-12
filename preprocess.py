""" Preprocessing module

Filters out small nodes and weak edges not to overload graph visualization

Usage example:
    preprocess.py "./data/raw/raw-tags_machine learning.json" "./data/filtered_5/filt-tags_machine-learning.json"
"""

import sys
import itertools
import json
from collections import Counter


def preprocess(raw_tags_path, out_path, node_size_thresh=0, lower=True):
    
    # load tags
    with open(raw_tags_path, 'r', encoding="utf-8") as f:
        tags_json = json.load(f)
        
    print(tags_json['parse_date'], tags_json['phrase'], tags_json['items_number'])

    tags_list = tags_json['items']
    if lower:
        tags_list = [[i.lower() for i in line] for line in tags_list]

    # counting words occurrences
    nodes_size = Counter([i for line in tags_list for i in line])
    print('Number of unique nodes:', len(nodes_size))
    
    # filtering by occurrences count
    nodes_size = {k: v for k, v in nodes_size.items() if v >= node_size_thresh}

    print(f'Len nodes dict >= {node_size_thresh}: {len(nodes_size)}')

    # count tags edges
    formatted_tags = dict()
    for line in tags_list:
        for tag1, tag2 in itertools.permutations([tag for tag in line if tag in nodes_size], 2):
            if (tag1, tag2) not in formatted_tags.keys():
                formatted_tags[(tag1, tag2)] = 0
            formatted_tags[(tag1, tag2)] += 1     

    #for k, v in formatted_tags.items():
    #    print(k, v)

    # prepairing for visualization
    count_color_step = (max(list(nodes_size.values())) - node_size_thresh) // min(7, len(nodes_size) - node_size_thresh)  # 7 colors
    nodes = [{"id": node, "group": (count - node_size_thresh) // count_color_step, "popularity": count} \
             for node, count in nodes_size.items()]

    links = [{"source": pair[0], "target": pair[1], "value": count} \
             for pair, count in formatted_tags.items()]         

    
    data_to_dump = {'parse_date': tags_json['parse_date'], 
                    'phrase': tags_json['phrase'], 
                    'items_number': tags_json['items_number'],
                    'items': {"nodes": nodes, "links": links}}

    print('phrase:', data_to_dump['phrase'])
    print('vacancies parced:', data_to_dump['items_number'])

    with open(out_path, 'w') as f:
        json.dump(data_to_dump, f, ensure_ascii=False)

    return formatted_tags


if __name__ == '__main__':
    raw_tags_path = sys.argv[1]
    out_path = sys.argv[2]
    preprocess(raw_tags_path, out_path, node_size_thresh=5)
