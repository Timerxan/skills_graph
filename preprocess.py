""" Preprocessing module

Filters out small nodes and weak links not to overload graph visualization
"""

import sys
import itertools
import pickle
import json


def process(raw_tags_path, del_nodes_count=10, del_links_count=5, lower=True):

    with open(raw_tags_path, 'rb') as f:
        tags_list = pickle.load(f)

    print(len(tags_list))
    # processing tags
    flattened_list = [i for line in tags_list for i in line]

    # filtering by occurrences count and counting words occurrences
    nodes_dict = {i: flattened_list.count(i) for i in set(flattened_list) if flattened_list.count(i) >= del_nodes_count}
    print(nodes_dict)

    # tags connection dict initialization
    formatted_tags = {(tag1, tag2): 0 for tag1, tag2 in itertools.permutations(set(nodes_dict.keys()), 2)}

    # count tags connection
    for line in tags_list:
        for tag1, tag2 in itertools.permutations(line, 2):
            if (tag1, tag2) in formatted_tags.keys():
                #print('------------------------------')
                formatted_tags[(tag1, tag2)] += 1

    #for k, v in formatted_tags.items():
    #    print(k, v)

    # filtering data with small number of links
    for k, v in formatted_tags.copy().items():
        if v <= del_links_count:
            del formatted_tags[k]

    for k, v in formatted_tags.items():
        print(k, v)

    nodes = []
    links = []

    for pair, count in formatted_tags.items():
        #print(pair)
        links.append({"source": pair[0].lower(), "target": pair[1].lower(), "value": count})

    for node, count in nodes_dict.items():
        nodes.append({"id": node, "group": int(count / 500), "popularity": count})

    data_to_dump = {"nodes": nodes, "links": links}

    print(data_to_dump)

    # rename file to use it
    phrase = raw_tags_path.split('_')[-1][:-4]
    with open(f'./data/proc-tags_{phrase}.json', 'w') as f:
        json.dump(data_to_dump, f)

    return formatted_tags


if __name__ == '__main__':
    raw_tags_path = sys.argv[1]
    process(raw_tags_path)
