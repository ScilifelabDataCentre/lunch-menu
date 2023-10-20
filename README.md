Lunch Menu Aggregator
=====================

This is the code for a web page listing the menus of the restaurants near SciLifeLab Solna (KI) and Uppsala (BMC).

The first code was written in 2010 by [@talavis](https://github.com/talavis), who is still the main developer. There are also multiple contributors of e.g. bugfixes and new parsers.

There are three parts:

* A parser that can be imported in Python. It uses Requests and BeautifulSoup to download and parse the restaurant web pages.
* A backend that makes the menus available via an API built on top of Flask.
* A frontend that presents the menus in a more readable format (by making requests to the backend). It is written in Quasar (Vue).


## Development

Run `docker-compose up`.


### Add a new restaurant

To add a new restaurant:
1. Add the parser function to `parser.py`
2. Add the relevant keyword and function name to `MAPPER` in `main.py`
3. Add information about the restaurant to `restaurants.json`


## Supported endpoints in the flask application:

- `/restaurant` (json): List all supported restaurants
- `/restaurant/<identifier>` (json): Retrieve menu for a restaurant (identifier can be obtained from the above request).


## Hosted versions:

- [Backend](https://menu.dckube.scilifelab.se/api)
- [Frontend](https://menu.dckube.scilifelab.se/)


## Feedback
Bugs and requests for new restaurants or features should be submitted as issues to Github.
