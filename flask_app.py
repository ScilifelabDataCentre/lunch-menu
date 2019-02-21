from flask import Flask
from flask_caching import Cache

import main

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def display_available():

    return """
<!DOCTYPE html>
<html lang="en">
<head>

  <!-- Basic Page Needs
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta charset="utf-8">
  <title>Restaurant Menu Parser</title>
  <meta name="description" content="">
  <meta name="author" content="">

  <!-- Mobile Specific Metas
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- FONT
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link href='//fonts.googleapis.com/css?family=Raleway:400,300,600' rel='stylesheet' type='text/css'>

  <!-- CSS
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="stylesheet" href="static/normalize.css">
  <link rel="stylesheet" href="static/skeleton.css">
  <link rel="stylesheet" href="static/custom.css">

  <!-- Scripts
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

  <!-- Favicon
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="icon" type="image/png" href="../../dist/images/favicon.png">

</head>
<body>
  <div class="gradient">
    <!-- Primary Page Layout
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->

    <h5><a href="ki">KI (Solna)</a><br><a href="uu">UU (BMC)</a></h5>


    <!-- End Document
    –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  </div>
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
