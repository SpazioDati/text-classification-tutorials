# coding: utf-8
import sys, requests, json

import logging
logging.captureWarnings(True)

APPID='INSERT_YOUR_APP_ID'
APPKEY='INSERT_YOUR_APP_KEY'

test_model = {
    'lang': 'it',
    'description': 'test #1 model',
    'categories': [
        {
            "name": "Tennis",
            "topics": {
                "https://it.wikipedia.org/wiki/Tennis": 1.0,
            },
        },
        {
            "name": "Calcio",
            "topics": {
                "https://it.wikipedia.org/wiki/Calcio_(sport)": 1.0,
                "https://it.wikipedia.org/wiki/Calcio_in_Italia": 1.0,
            },
        },
        {
            "name": "Ciclismo",
            "topics": {
                "https://it.wikipedia.org/wiki/Ciclismo_(sport)": 1.0,
            },
        },
        {
            "name": "Rugby",
            "topics": {
                "https://it.wikipedia.org/wiki/Rugby": 1.0,
                "https://it.wikipedia.org/wiki/Rugby_a_15": 1.0,
                "https://it.wikipedia.org/wiki/Rugby_a_13": 1.0,
                "https://it.wikipedia.org/wiki/Rugby_a_13": 1.0,
            },
        },
    ],
}

all_models = requests.get('https://api.dandelion.eu/datatxt/cl/models/v1', {'$app_id':APPID, '$app_key':APPKEY}).json()
print 'looking for model with this description:', test_model['description']
test_models = filter(lambda m: m['data']['description'] == test_model['description'], all_models['items'])
if len(test_models) == 0:
    print 'creating test model...'
    custom_model = requests.post('https://api.dandelion.eu/datatxt/cl/models/v1', {'$app_id':APPID, '$app_key':APPKEY, 'data':json.dumps(test_model) }).json()
else:
    print 'test models:', map(lambda m: (m['data']['description'], m['id']), test_models)
    custom_model = test_models[0]
    custom_model = requests.put('https://api.dandelion.eu/datatxt/cl/models/v1', {'$app_id':APPID, '$app_key':APPKEY, 'id':custom_model['id'], 'data':json.dumps(test_model) }).json()
print custom_model

test_texts = [
    'colpisce la palla con la racchetta e vince',
    'con dribbling, supera il difensore e manda la palla in rete',
    'manda la palla in rete e segna il primo goal della partita',
]

for text in test_texts:
    print ''
    print text
    result = requests.get('https://api.dandelion.eu/datatxt/cl/v1', {'$app_id':APPID, '$app_key':APPKEY, 'model':custom_model['id'], 'text':text }).json()
    for category in result['categories']:
        print '  - [{}] {}'.format(category['score'],category['name'])
