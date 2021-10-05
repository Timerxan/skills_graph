from pyvis.network import Network
import json


def gr_vis(filt_tags_path):
    with open(filt_tags_path, 'r', encoding="utf-8") as f:
        tags_json = json.load(f)

    net = Network(800, 800)

    net.add_nodes([node["id"] for node in tags_json["items"]["nodes"]])
    net.add_edges([(link["source"], link["target"]) for link in tags_json["items"]["links"]])

    net.show_buttons(filter_=['physics'])
    net.show('graph_vis.html')


if __name__ == '__main__':
    gr_vis('data/for_visualization/filt-tags_python.json')
