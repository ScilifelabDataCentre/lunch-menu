from flask import Flask, abort, jsonify
import flask
from flask_caching import Cache
from flask_cors import CORS

import main

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/')
@cache.cached(timeout=10800)
def list_entities():
    return jsonify({'entities': ['restaurant']})


@app.route('/api/restaurant/')
@cache.cached(timeout=10800)
def list_restaurants():
    return jsonify({'restaurants': main.list_restaurants()})


@app.route('/api/restaurant/<name>/')
@cache.cached(timeout=10800)
def get_restaurant(name):
    data = dict(main.get_restaurant(name))
    if not data:
        abort(status=404)
    data['menu'] = [{'dish': entry} for entry in data['menu']]
    return jsonify({'restaurant': data})

@app.route('/api/slack/', methods=['POST'])
def handle_slack_request():
    command_text = flask.request.form['text']
    identifiers = command_text.split()
    available = [entry['identifier'] for entry in main.list_restaurants()]
    regions = ('ki', 'bmc', 'uu', 'uppsala', 'solna')

    text = ''
    for identifier in identifiers:
        if identifier not in available and identifier.lower() not in regions:
            text = f'Usage: `/lunch-menu <identifier>`. Available restaurants:\n\n'
            for entry in main.list_restaurants():
                text += f'- {entry["name"]}: `{entry["identifier"]}`\n'
            break
        elif identifier.lower() in regions:
            if identifier.lower() in ('solna', 'ki'):
                new_ids = [entry['identifier'] for entry in main.list_restaurants() if entry['campus'] == 'Solna']
            else:
                new_ids = [entry['identifier'] for entry in main.list_restaurants() if entry['campus'] == 'Uppsala']
            for ident in new_ids:
                restaurant_data = dict(main.get_restaurant(ident))
                text += f'*{restaurant_data["title"]}*\n'
                for dish in restaurant_data['menu']:
                    text += f'- {dish}\n'
        else:
            restaurant_data = dict(main.get_restaurant(identifier))
            text += f'*{restaurant_data["title"]}*\n'
            for dish in restaurant_data['menu']:
                text += f'- {dish}\n'

    response = {"blocks": [{"type": "section",
			    "text": {
				"type": "mrkdwn",
				"text": text}}]}
    return flask.jsonify(response)
