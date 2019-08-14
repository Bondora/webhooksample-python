import os
import json

from flask import Flask, request
from signature import validate_signature

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

@app.route('/')
def ping():
    return 'OK'

@app.route('/hook', methods=['POST'])
def hook():
    validate_signature(request, app.config.get('KEYS'), app.config.get('HOST'))

    event = json.loads(request.data)
    eventid = event["EventId"]
    eventtype = event["EventType"]
    payload = event['Payload']

    print("event: {}, id: {}".format(eventtype, eventid))

    datadir = app.config.get('DATADIR')
    os.makedirs(datadir, exist_ok=True)

    filepath = '{}/{}_{}.json'.format(datadir, eventid, eventtype)
    with open(filepath, mode='w', encoding='utf8') as f:
        json.dump(payload, f, indent='  ')

    return 'POST'

if __name__ == '__main__':
    app.run()