from flask import Flask, render_template, url_for, request
from graph_vis import gr_vis
import json


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    style = url_for('static', filename='style.css')
    visualisation = url_for('user_graph', ip=ip, key_word='python', node_level=5, edge_level=5)
    return render_template('index.html', style=style, vis=visualisation)


@app.route('/send', methods=['POST', 'GET'])
def send():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    style = url_for('static', filename='style.css')
    if request.method == 'POST':
        key_word = request.form['key_word']
        key_word, node_level, edge_level = key_word.split(':')
        visualisation = url_for('user_graph', ip=ip, key_word=key_word,
                                node_level=int(node_level), edge_level=int(edge_level))
        return render_template('index.html', style=style, vis=visualisation)


@app.route('/user_graph_<ip>_<key_word>_<node_level>_<edge_level>', methods=['POST', 'GET'])
def user_graph(ip, key_word, node_level, edge_level):
    path = gr_vis(ip, key_word, int(node_level), int(edge_level))
    with open(path, 'r', encoding="utf-8") as f:
        graph_html = f.read()

    return graph_html


if __name__ == "__main__":
    app.run(debug=False)