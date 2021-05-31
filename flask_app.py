import flask
import flask_caching
import flask_cors

import main
import slack

app = flask.Flask(__name__)
cache = flask_caching.Cache(app, config={"CACHE_TYPE": "simple"})
cors = flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(slack.blueprint, url_prefix="/api/slack")


@app.route("/api")
@cache.cached(timeout=10800)
def list_entities():
    return flask.jsonify({"entities": ["restaurant"],
                    "url": flask.url_for("list_entities", _external=True)})


@app.route("/api/restaurant")
@cache.cached(timeout=10800)
def list_restaurants():
    return flask.jsonify({"restaurants": main.list_restaurants(),
                    "url": flask.url_for("list_restaurants", _external=True)})


@app.route("/api/restaurant/<name>")
@cache.cached(timeout=10800)
def get_restaurant(name):
    data = dict(main.get_restaurant(name))
    if not data:
        abort(status=404)
    data["menu"] = [{"dish": entry} for entry in data["menu"]]
    return flask.jsonify({"restaurant": data,
                    "url": flask.url_for("get_restaurant", name=name, _external=True)})
