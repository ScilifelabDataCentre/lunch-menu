import json

from flask import abort
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

import main


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def display_available():
    content = ('<html>' +
               '<head>' +
               '<title>Restaurant Menu Parser</title>' +
               '</head>' +
               '<body>' +
               '<p><a href="ki">Campus Solna (KI)</a></p>' +
               '<p><a href="uu">Campus Uppsala (BMC)</a></p>' +
               '</body>' +
               '</html>')
    return content


@app.route('/api/restaurants')
@cache.cached(timeout=3600)
def api_list_restaurants():
    return json.dumps(main.list_restaurants())


@app.route('/api/restaurant/<name>')
@cache.cached(timeout=3600)
def api_get_restaurant(name):
    data = main.get_restaurant(name)
    if not data:
        abort(404)
    return json.dumps(data)


@app.route('/ki')
@cache.cached(timeout=3600)
def make_menu_ki():
    return main.gen_ki_menu()


@app.route('/uu')
@cache.cached(timeout=3600)
def make_menu_uu():
    return main.gen_uu_menu()
