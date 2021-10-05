from pyvis.network import Network
import json


def gr_vis(filt_tags_path, node_cut_off_level=1, edge_cut_off_level=1):
    with open(filt_tags_path, 'r', encoding="utf-8") as f:
        tags_json = json.load(f)

    node_max_popularity = max([node["popularity"] for node in tags_json["items"]["nodes"]])
    link_max_value = max([link["value"] for link in tags_json["items"]["links"]])
    node_nc = 100/node_max_popularity  # node normalization coefficient
    link_nc = 100/link_max_value  # link normalization coefficient

    nodes = [node["id"] for node in tags_json["items"]["nodes"]
             if int(node_nc * node["popularity"]) > node_cut_off_level]
    nodes_size = [2 + int((node_nc * node["popularity"])**0.5)
                  for node in tags_json["items"]["nodes"]
                  if int(node_nc * node["popularity"]) > node_cut_off_level]

    def color_from_popularity(popularity):  # popularity 0-100
        if popularity > 75 : return 'red'
        elif popularity > 50 : return 'yellow'
        elif popularity > 25 : return 'green'
        else : return 'blue'

    nodes_color = [color_from_popularity(node_nc*node["popularity"])
                   for node in tags_json["items"]["nodes"]
                   if int(node_nc * node["popularity"]) > node_cut_off_level]

    edges = [(link["source"], link["target"], int(link_nc * link["value"]/15))
             for link in tags_json["items"]["links"]
             if link["source"] in nodes
             and link["target"] in nodes
             and int(link_nc * link["value"]) > edge_cut_off_level]

    net = Network(800, 800)

    for node, node_size, color in zip(nodes, nodes_size, nodes_color):
        net.add_node(node, hidden=False, shape='dot', color=color, size=node_size, mass=node_size,
                     borderWidth=0, borderWidthSelected=2)

    net.add_edges(edges)
    net.inherit_edge_colors(False)
    net.set_edge_smooth('diagonalCross')
    net.set_options("""
                    var options = {
                      "nodes": {
                        "font": {
                          "strokeWidth": 3
                        }
                      },
                      "edges": {
                        "color": {
                          "color": "rgba(66,66,65,0.58)",
                          "highlight": "rgba(255,148,45,1)",
                          "inherit": false
                        },
                        "font": {
                          "strokeWidth": 42
                        },
                        "smooth": {
                          "type": "cubicBezier",
                          "forceDirection": "none"
                        }
                      },
                        "physics": {
                            "barnesHut": {
                              "gravitationalConstant": -1050,
                              "centralGravity": 4,
                              "springLength": 50,
                              "springConstant": 0.015,
                              "damping": 0.4,
                              "avoidOverlap": 0.2
                            },
                            "minVelocity": 0.75
                      }
                    }
                    """)
    net.write_html('graph_visualisation.html')
    # net.show('graph_vis.html')


if __name__ == '__main__':
    gr_vis('data/for_visualization/filt-tags_python.json', node_cut_off_level=5, edge_cut_off_level=5)
