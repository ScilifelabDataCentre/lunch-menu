import os

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from starlette_context import middleware, plugins

import utils

app = FastAPI()

if os.environ.get("REVERSE_PROXY", False):
    app.add_middleware(
        middleware.ContextMiddleware,
        plugins=(
            plugins.ForwardedForPlugin(),
        ),
    )


@app.get("/api")
@cache(expires=360000)
async def list_entities():
    return {"entities": ["restaurant"]}


@app.get("/api/restaurant")
@cache(expires=360000)
async def list_restaurants():
    print("asd")
    return {
        "restaurants": utils.list_restaurants(),
    }


@app.get("/api/restaurant/{name}")
@cache(expire=10800)
async def get_restaurant(name):
    data = dict(utils.get_restaurant(name))
    if not data:
        flask.abort(status=404)
    data["menu"] = [{"dish": entry} for entry in data["menu"]]
    return {"restaurant": data,}


@app.get("/api/version")
@cache(expires=360000)
async def get_backend_version():
    ver = os.environ.get("VERSION", "")
    return {"version": ver,}


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
