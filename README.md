lunch-parser
============

Scripts useful for parsing the menus of the restaurants near Campus Solna of Karolinska Institutet and BMC of Uppsala University and generating a simple html page.

Usage:
python3 main.py restaurant_name > index.html

The supported restaurants are also listed when you run main.py without any arguments.

If new restaurants are added, add the parser function to `parser.py`, the relevant keyword and function name to `MAPPER` in `main.py`, and URLs etc to `restaurants.txt`.

An experimental version can be run via flask `FLASK_APP=flask_app.py flask run`, with the ki menus listed under /ki and uu under /uu.