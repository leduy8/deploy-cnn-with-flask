# * Remember to: set FLASK_APP=hello_app.py then type: flask run to run
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/hello', methods=['POST'])
def hello():
    message = request.get_json(force=True)
    name = message['name']
    response = {
        'greeting': 'Hello, ' + name + '!'
    }
    return jsonify(response)
