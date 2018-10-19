from flask import Flask, request, jsonify
from amount import get_amount
import json
import os

DEBUG = True
CONFIG_FILE = 'config.json'
COLLECTION_FILE = 'collection.json'
INITIAL_CONFIG = {
    'name': '',
    'collection': {}
}

app = Flask(__name__)

def init_config(): 
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as conf:
            json.dump(INITIAL_CONFIG, conf)

def init_data():
    if not os.path.exists(COLLECTION_FILE):
        from collection_day_crawler import crawl
        crawl()

@app.route('/amount')
def amount():
    response = jsonify({'amount': get_amount()})
    response.status_code = 200
    return response

@app.route('/config', methods=['GET', 'POST'])
def config(): 
    with open(CONFIG_FILE, 'r') as conf:
        data = json.load(conf)
    
    if request.method == 'GET':
        response = jsonify(data)
    elif request.method == 'POST':
        with open(CONFIG_FILE, 'w') as conf:
            result = {'name': 'keep', 'collection': 'keep'}
            if 'name' in request.form: 
                result['name'] = 'changed'
                data['name'] = request.form['name']
            if 'collection' in request.form: 
                result['collection'] = 'changed'
                data['collection'] = request.form['collection']
            json.dump(data, conf)
        response = jsonify(result)

    response.status_code = 200
    return response

def search_id(collection, id):
    for k in collection.values():
        for c in k:
            if str(c['id']) == id: 
                return c
    return {}

def search_ku(collection, ku):
    for k in collection:
        if k == ku:
            return collection[ku]
    return {}

def search_juusho(collection, juusho):
    for k in collection.values():
        for c in k:
            if c['juusho'] == juusho: 
                return c
    return {}

@app.route('/collection')
def collection_day(): 
    with open(COLLECTION_FILE) as collection_json:
        collection = json.load(collection_json)
    
    result = collection
    id = request.args.get('id')
    ku = request.args.get('ku')
    kana1 = request.args.get('kana1')
    kana2 = request.args.get('kana2')
    juusho = request.args.get('juusho')
    if id:
        result = search_id(collection, id)
    elif ku:
        result = search_ku(collection, ku)
        if kana1:
            result = [c for c in result if c['kana1'] == kana1]
            if kana2:
                result = [c for c in result if c ['kana2'] == kana2]
    elif juusho:
        result = search_juusho(collection, juusho)
    
    response = jsonify(result)
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.debug = DEBUG
    init_config()
    init_data()
    app.run()