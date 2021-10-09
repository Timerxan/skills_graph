from pyvis.network import Network
import json


def gr_vis(key_word="Hello!", node_level=5, edge_level=5):

    with open('data/for_visualization/index.json', 'r', encoding="utf-8") as f:
        key_words_json = json.load(f)

    with open(f"data/for_visualization/{key_words_json[key_word]}", 'r', encoding="utf-8") as f:
        tags_json = json.load(f)

    node_max_popularity = max([node["popularity"] for node in tags_json["items"]["nodes"]])
    link_max_value = max([link["value"] for link in tags_json["items"]["links"]])
    node_nc = 100/node_max_popularity  # node normalization coefficient
    link_nc = 100/link_max_value  # link normalization coefficient

    nodes = [node["id"] for node in tags_json["items"]["nodes"]
             if int(node_nc * node["popularity"]) > node_level]
    nodes_size = [1 + int((node_nc * node["popularity"])**0.5)
                  for node in tags_json["items"]["nodes"]
                  if int(node_nc * node["popularity"]) > node_level]

    def color_from_popularity(popularity):  # popularity 0-100
        if popularity > 50:
            return '#%02x%02x%02x' % (int((popularity-50)/50*255), int((100-popularity)/50*255), 0)
        else:
            return '#%02x%02x%02x' % (0, int(popularity/50*255), int((100-popularity)/100*255))

    nodes_color = [color_from_popularity(node_nc*node["popularity"])
                   for node in tags_json["items"]["nodes"]
                   if int(node_nc * node["popularity"]) > node_level]

    edges = [(link["source"], link["target"], int(link_nc * link["value"]/10))
             for link in tags_json["items"]["links"]
             if link["source"] in nodes
             and link["target"] in nodes
             and int(link_nc * link["value"]) > edge_level]

    net = Network(800, 800)

    for node, node_size, color in zip(nodes, nodes_size, nodes_color):
        net.add_node(node, hidden=False, shape='dot', color=color, size=2*node_size, mass=12-node_size,
                     borderWidth=0, borderWidthSelected=2)

    net.add_edges(edges)
    net.inherit_edge_colors(False)
    with open('static/var_options.json', 'r', encoding="utf-8") as f:
        var_options = f.read()
    net.set_options(f'{var_options}')
    # net.show_buttons()
    path = f'tmp/graph_visualisation_{key_word}_{node_level}_{edge_level}.html'
    net.save_graph(path)
    return path

if __name__ == '__main__':
    gr_vis(key_word='python', node_level=5, edge_level=5)
