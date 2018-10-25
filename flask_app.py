from flask import Flask

import main

app = Flask(__name__)

@app.route('/')
def display_available():
    content = ('<html>' +
               '<head>' +
               '<title>Restaurant Menu Parser</title>' +
               '</head>' +
               '<body>' +
               '<p><a href="ki">KI (Solna)</a></p>' + 
               '<p><a href="uu">UU (BMC)</a></p>' +
               '</body>' +
               '</html>')
    return content

@app.route('/ki')
def make_menu_ki():
    return main.gen_ki_menu()

@app.route('/uu')
def make_menu_uu():
    return main.gen_uu_menu()
