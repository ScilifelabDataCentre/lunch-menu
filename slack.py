"""
Requests/functions used to interact with slack
"""
import os

import flask

import main


blueprint = flask.Blueprint('slack', __name__)  # pylint: disable=invalid-name


@blueprint.route('/', methods=['POST'])
def handle_slack_request():
    command_text = flask.request.form['text']
    identifiers = command_text.split()
    available = [entry['identifier'] for entry in main.list_restaurants()]
    regions = ('ki', 'bmc', 'uu', 'uppsala', 'solna')

    text = ''
    for identifier in identifiers:
        if identifier in available:
            restaurant_data = dict(main.get_restaurant(identifier))
            text += f'*{restaurant_data["title"]}*\n'
            for dish in restaurant_data['menu']:
                text += f'- {dish}\n'
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
            text = list_identifiers()
            break
    if not identifiers:
        text = list_identifiers()

    response = {"blocks": [{"type": "section",
			    "text": {
				"type": "mrkdwn",
				"text": text}}]}
    return flask.jsonify(response)


def get_token(token_name: str) -> str:
    try:
        return os.environ[token]
    except KeyError:
        return None


def list_identifiers() -> str:
    text = f'*Available restaurants:*\n'
    for entry in main.list_restaurants():
        text += f'- {entry["name"]}: `{entry["identifier"]}`\n'
    text += '- Solna: `solna`\n'
    text += '- Uppsala: `uppsala`\n'
    return text
