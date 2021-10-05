from pyvis.network import Network
import json


def gr_vis(filt_tags_path, node_cut_off_level = 20):
    with open(filt_tags_path, 'r', encoding="utf-8") as f:
        tags_json = json.load(f)

    node_max_popularity = max([node["popularity"] for node in tags_json["items"]["nodes"]])
    link_max_value = max([link["value"] for link in tags_json["items"]["links"]])
    node_nc = 100/node_max_popularity  # node normalization coefficient
    link_nc = 100/link_max_value  # link normalization coefficient

    nodes = [node["id"]
             for node in tags_json["items"]["nodes"]
             if int(node_nc * node["popularity"]) > node_cut_off_level]
    nodes_values = [int((node_nc * node["popularity"]) ** 0.5)
                    for node in tags_json["items"]["nodes"]
                    if int(node_nc * node["popularity"]) > node_cut_off_level]

    edges = [(link["source"], link["target"], int(link_nc * link["value"]/10))
             for link in tags_json["items"]["links"]
             if link["source"] in nodes and link["target"] in nodes]

    net = Network(800, 800)

    net.add_nodes(nodes, nodes_values)
    net.add_edges(edges)

    net.show_buttons(filter_=['physics'])
    net.show('graph_vis.html')


if __name__ == '__main__':
    gr_vis('data/for_visualization/filt-tags_python.json')
