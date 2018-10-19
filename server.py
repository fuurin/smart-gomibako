from flask import Flask, request, jsonify
from amount import get_amount
from config import init_config, set_config
from collection_day_crawler import init_collection
from collection_searcher import search_collection
from collection_day_checker import nowIsCollectionDay, tomorrowIsCollectionDay
from notification import notify_for_today, notify_for_tomorrow
import json

DEBUG = True
CONFIG_FILE = 'config.json'
COLLECTION_FILE = 'collection.json'
GOMIBAKO_THRESHOLD = 3

app = Flask(__name__)

@app.route('/')
def index():
    response = jsonify({'Health Check': 'Hello! This is smart-gomibako API!'})
    response.status_code = 200
    return response

@app.route('/amount')
def amount():
    response = jsonify({'amount': get_amount()})

    response.status_code = 200
    return response

@app.route('/config', methods=['GET', 'POST'])
def config(): 
    with open(CONFIG_FILE, 'r') as config_json:
        config = json.load(config_json)
    
    if request.method == 'GET':
        response = jsonify(config)
    elif request.method == 'POST':
        with open(CONFIG_FILE, 'w') as config_file:
            new_config, response = set_config(config, request.form)
            json.dump(new_config, config_file)
        response = jsonify(response)

    response.status_code = 200
    return response

@app.route('/collection')
def collection(): 
    with open(COLLECTION_FILE) as collection_json:
        collection = json.load(collection_json)
    with open(CONFIG_FILE) as config_json:
        config = json.load(config_json)
    
    id = request.args.get('id')
    ku = request.args.get('ku')
    kana1 = request.args.get('kana1')
    kana2 = request.args.get('kana2')
    juusho = request.args.get('juusho')

    result = search_collection(collection, config, id, ku, kana1, kana2, juusho)
    response = jsonify(result)

    response.status_code = 200
    return response

@app.route('/today')
def today_is_collection_day():
    with open(COLLECTION_FILE) as collection_json:
        collection = json.load(collection_json)
    with open(CONFIG_FILE) as config_json:
        config = json.load(config_json)
    
    response = jsonify({'result': nowIsCollectionDay(collection, config), 'config': config})

    response.status_code = 200
    return response

@app.route('/tomorrow')
def tomorrow_is_collection_day():
    with open(COLLECTION_FILE) as collection_json:
        collection = json.load(collection_json)
    with open(CONFIG_FILE) as config_json:
        config = json.load(config_json)
    
    response = jsonify({'result': tomorrowIsCollectionDay(collection, config), 'config': config})

    response.status_code = 200
    return response

@app.route('/notify')
def notify():
    if get_amount() >= GOMIBAKO_THRESHOLD:
        if today_is_collection_day():
            notify_for_today()
        if tomorrow_is_collection_day():
            notify_for_tomorrow()

if __name__ == '__main__':
    app.debug = DEBUG
    init_config(CONFIG_FILE)
    init_collection(COLLECTION_FILE)
    app.run()