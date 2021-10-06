from flask import Flask, render_template, url_for, request
from graph_vis import gr_vis


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    style = url_for('static', filename='style.css')
    visualisation = url_for('user_graph', ip=ip)
    if request.method == 'POST':
        print(request.form)
    print(visualisation)
    return render_template('index.html', style=style, vis=visualisation)


@app.route('/send', methods=['POST', 'GET'])
def send():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    style = url_for('static', filename='style.css')
    visualisation = url_for('user_graph', ip=ip)
    if request.method == 'POST':
        print(request.form)
    print(visualisation)
    return render_template('index.html', style=style, vis=visualisation)


@app.route('/user_graph<ip>', methods=['GET'])
def user_graph(ip):
    path = gr_vis(ip)
    with open(path, 'r', encoding="utf-8") as f:
        graph_html = f.read()
    return graph_html


if __name__ == "__main__":
    app.run(debug=True)