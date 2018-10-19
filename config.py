import json, os

INITIAL_CONFIG = {
    'name': '',
    'category': '',
    'collection': ''
}

def set_config(config, form):
    result = {'name': 'keep', 'category': 'keep', 'collection': 'keep'}
    for item in result:
        if item in form: 
            result[item] = 'changed'
            config[item] = form[item]
    return config, result

def init_config(config_file): 
    if not os.path.exists(config_file):
        with open(config_file, 'w') as config:
            json.dump(INITIAL_CONFIG, config)