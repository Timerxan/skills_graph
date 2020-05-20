""" Preprocessing module

Filters out small nodes and weak links not to overload graph visualization

Usage example:
    preprocess.py "./data/raw/raw-tags_machine learning.json" "./data/filtered_5/filt-tags_machine-learning.json"
"""

import sys
import itertools
import json


def process(raw_tags_path, out_path, del_nodes_count=0, lower=True):

    with open(raw_tags_path, 'rb') as f:
        in_json = json.load(f)

    tags_list = in_json['items']
    if lower:
        tags_list = [[i.lower() for i in line] for line in tags_list]

    print(len(tags_list))

    # processing tags
    flattened_list = [i for line in tags_list for i in line]

    # counting words occurrences
    nodes_dict_all = {i: flattened_list.count(i) for i in set(flattened_list)}
    # filtering by occurrences count
    nodes_dict = {k:v for k, v in nodes_dict_all.items() if v > del_nodes_count}

    print('Len nodes dict:', len(nodes_dict_all))
    print(f'Len nodes dict > {del_nodes_count}: {len(nodes_dict)}')

    # tags connection dict initialization
    formatted_tags = {(tag1, tag2): 0 for tag1, tag2 in itertools.permutations(set(nodes_dict.keys()), 2)}

    # count tags connection
    for line in tags_list:
        for tag1, tag2 in itertools.permutations(line, 2):
            if (tag1, tag2) in formatted_tags.keys():
                formatted_tags[(tag1, tag2)] += 1

    # filtering pairs with zero count
    for k, v in formatted_tags.copy().items():
        if v == 0:
            del formatted_tags[k]

    #for k, v in formatted_tags.items():
    #    print(k, v)

    nodes = []
    links = []
    for pair, count in formatted_tags.items():
        links.append({"source": pair[0], "target": pair[1], "value": count})

    max_count = max(list(nodes_dict.values()))
    count_step = max_count // 7
    for node, count in nodes_dict.items():
        nodes.append({"id": node, "group": count // count_step, "popularity": count})

    data_to_dump = in_json.copy()
    data_to_dump['items'] = {"nodes": nodes, "links": links}

    print('phrase:', data_to_dump['phrase'])
    print('vacancies parced:', data_to_dump['items_number'])

    with open(out_path, 'w') as f:
        json.dump(data_to_dump, f, ensure_ascii=False)

    return formatted_tags


if __name__ == '__main__':
    raw_tags_path = sys.argv[1]
    out_path = sys.argv[2]
    process(raw_tags_path, out_path, del_nodes_count=5)
