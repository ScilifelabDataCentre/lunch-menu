from flask import Flask

import main

app = Flask(__name__)

@app.route('/ki')
def make_menu_ki():
    return main.gen_ki_menu()

@app.route('/uu')
def make_menu_uu():
    return main.gen_uu_menu()
