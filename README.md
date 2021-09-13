Lunch Menu Aggregator
=====================

This is the code for a webpage listing the menus of the restaurants near SciLifeLab Solna (KI) and Uppsala (BMC).

The first code was written in 2010 by [@talavis](https://github.com/talavis), who is still the main developer. There are also multiple contributors of e.g. bugfixes and new parsers.

There are three parts:

* A parser that can be accessed via CLI or be imported in Python. It uses Requests and BeatifulSoup to download and parse the restaurant web pages.
* A backend that makes the menus available via via an API built on top of Flask.
* A frontend that presents the menus in a more readable format (by making requests to the backend. It is written in Quasar (Vue).

## Using the python backend in CLI

Usage: `python3 main.py restaurant_name > index.html`

The supported restaurants are also listed when you run main.py without any arguments.


## Development

### Backend

Start the backend with `FLASK_APP=flask_app.py flask run`.

### Frontend

Update `proxy.target` in `frontend/quasar.conf.js` to match your backend.

Make sure you have installed `yarn` and `quasar` (using e.g. `yarn global add @quasar/cli`).

Start the frontend by running `quasar dev` in the `frontend` folder.

### Add a new restaurant

To add a new restaurant:
1. Add the parser function to `parser.py`
2. Add the relevant keyword and function name to `MAPPER` in `main.py`
3. Add URLs etc to `restaurants.json`


## Supported endpoints in the flask application:

- `/restaurant/` (json): List all supported restaurants
- `/restaurant/<identifier>/` (json): Retrieve menu for a restaurant (identifier can be obtained from the above request).


## Hosted versions:

- [Backend](https://menu.dckube.scilifelab.se/api/)
- [Frontend](https://menu.dckube.scilifelab.se/)


## Containers:

Dockerfiles are available in the `k8s` folder.

- [Backend](https://hub.docker.com/repository/docker/scilifelabdatacentre/menu-backend)
- [Frontend hosted in nginx](https://hub.docker.com/repository/docker/scilifelabdatacentre/menu-frontend)


## Feedback
Bugs and requests for new restaurants or features should be submitted as issues to Github.
