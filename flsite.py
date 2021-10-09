from flask import Flask, render_template, url_for, request
from graph_vis import gr_vis
from os import remove
import json

app = Flask(__name__)

def get_tag_list():
    with open('data/for_visualization/index.json', 'r', encoding="utf-8") as f:
        return json.load(f).keys()

@app.route('/', methods=['POST', 'GET'])
def index():
    style = url_for('static', filename='style.css')
    tags = get_tag_list()
    visualisation = url_for('user_graph', key_word='Hello', node_level=0, edge_level=0)
    return render_template('index.html', style=style, vis=visualisation, tags=tags, chosen_tag='Choose interested tag')


@app.route('/<tag>', methods=['POST', 'GET'])
def send(tag):
    style = url_for('static', filename='style.css')
    tags = get_tag_list()
    if request.method == 'POST':
        key_word = request.values['button']
        key_word, node_level, edge_level = key_word.split(',')
        visualisation = url_for('user_graph', key_word=key_word,
                                node_level=int(node_level), edge_level=int(edge_level))
        return render_template('index.html', style=style, vis=visualisation, tags=tags, chosen_tag=tag)


@app.route('/user_graph_<key_word>_<node_level>_<edge_level>', methods=['POST', 'GET'])
def user_graph(key_word, node_level, edge_level):
    path = gr_vis(key_word, int(node_level), int(edge_level))
    with open(path, 'r', encoding="utf-8") as f:
        graph_html = f.read()
    remove(path)
    return graph_html


if __name__ == "__main__":
    app.run(debug=True)