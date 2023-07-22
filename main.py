from flask import Flask, render_template, request, url_for, redirect, session, jsonify, after_this_request
import json
from nerdfilmes import createHTML, getLink
from peerflix_process import start_peerflix, kill_peerflix
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP


app = Flask(__name__)


magneticLink = """magnet:?xt=urn:btih:08ada5a7a6183aae1e09d831df6748d566095a10&dn=Sintel&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F"""


@app.route('/', methods=["POST", "GET"])
def home():
	if request.method == "GET":	
		return render_template('index.html', HOST=f'http://{get_ip()}:5000')


@app.route('/search', methods=["POST", "GET"])
def search():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    if request.method == "POST":
        title = request.get_data().decode()
        title = json.loads(title)['title']
        return  createHTML(title)       
    
    if request.method == "GET":
        return 'MERDA'


@app.route('/setlink', methods=["POST", "GET"])
def set():
    global magneticLink 

    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    if request.method == "POST":
        url = request.get_data().decode()
        url = json.loads(url)['url']
        start_peerflix(getLink(url))
        return  'ok'


@app.route('/magnetic', methods=["POST", "GET"])
def magnetic():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if request.method == "GET":
        return magneticLink


@app.route('/kill', methods=["POST", "GET"])
def kill():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if request.method == "GET":
        kill_peerflix()
        return 'kill'

        #return render_template('index.html')


@app.route('/video', methods=["POST", "GET"])
def video():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if request.method == "GET":
        return render_template('video.html', HOST=f'http://{get_ip()}:8888')



app.run(host='0.0.0.0', port=5000, debug=True)


# @app.route('/', methods=["POST", "GET"])
# def home():
# 	if request.method == "POST":
# 		manga_title = request.form["manga_title"]
# 		return redirect(url_for("results", manga_title=manga_title))
# 	return render_template('pesquisa.html')