from flask import Flask
from flask_caching import Cache

import main


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

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

@app.route('/ki')
@cache.cached(timeout=3600)
def make_menu_ki():
    return main.gen_ki_menu()

@app.route('/uu')
@cache.cached(timeout=3600)
def make_menu_uu():
    return main.gen_uu_menu()
