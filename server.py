from flask import Flask, request, jsonify
from amount import get_amount
import json

DEBUG = True
CONFIG_FILE = 'config.json'
INITIAL_CONFIG = {
    'name': '',
    'collection': {}
}

app = Flask(__name__)

def init_config(): 
    with open(CONFIG_FILE, 'w') as conf:
        json.dump(INITIAL_CONFIG, conf)

@app.route('/amount')
def amount():
    response = jsonify({'amount': get_amount()})
    response.status_code = 200
    return response

@app.route('/config')
def config():
    with open(CONFIG_FILE, 'r') as conf:
        response = jsonify(json.load(conf))
    response.status_code = 200
    return response

@app.route('/config/name', methods=['GET', 'POST'])
def set_name(): 
    with open(CONFIG_FILE, 'r') as conf:
        data = json.load(conf)
    
    if request.method == 'GET':
        response = jsonify({'name': data['name']})
    else:
        with open(CONFIG_FILE, 'w') as conf:
            data['name'] = request.form['name']
            json.dump(data, conf)
        response = jsonify({'response': 'name changed'})

    response.status_code = 200
    return response

@app.route('/config/collection', methods=['GET', 'POST'])
def set_collection(): 
    with open(CONFIG_FILE, 'r') as conf:
        data = json.load(conf)
    
    if request.method == 'GET':
        response = jsonify({'collection': data['collection']})
    else:
        with open(CONFIG_FILE, 'w') as conf:
            data['collection'] = json.loads(request.form['collection'])
            json.dump(data, conf)
        response = jsonify({'response': 'collection changed'})

    response.status_code = 200
    return response

if __name__ == '__main__':
    app.debug = DEBUG
    init_config()
    app.run()