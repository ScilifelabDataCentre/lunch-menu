from flask import Flask
from flask_caching import Cache

import main

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def display_available():
    return main.page_start("Restaurant Menu Parser")[0] + """
    <p><a href="ki">KI (Solna)</a></p>
    <p><a href="uu">UU (BMC)</a></p>
  </body>
</html>
    """

@app.route('/ki')
@cache.cached(timeout=3600)
def make_menu_ki():
    return main.gen_ki_menu()

@app.route('/uu')
@cache.cached(timeout=3600)
def make_menu_uu():
    return main.gen_uu_menu()
