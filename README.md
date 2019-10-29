lunch-parser
============

Parser for the menus of the restaurants near Campus Solna of Karolinska Institutet and BMC of Uppsala University.

## Using the python backend

Usage: `python3 main.py restaurant_name > index.html`

The supported restaurants are also listed when you run main.py without any arguments.

If new restaurants are added, add the parser function to `parser.py`, the relevant keyword and function name to `MAPPER` in `main.py`, and URLs etc to `restaurants.txt`.

It can be run via flask (`FLASK_APP=flask_app.py flask run`).

## Supported endpoints in the flask application:

- `/api/restaurants` (json): List all supported restaurants
- `/api/restaurant/<identifier>` (json): Retrieve menu for a restaurant (identifier can be obtained from the above request).
- `/ki` (html): Menu page for restaurants in Solna (KI)
- `/uu` (html): Menu page for restaurants in Uppsala (BMC)

## Hosted versions:

- [Flask app](http://scilifelab-lunches.herokuapp.com/)
- [Vue frontend](http://talavis.eu/menu/)

## Feedback
Bugs and requests for new restaurants or features should be submitted as issues.