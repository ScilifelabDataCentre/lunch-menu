import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from starlette_context import middleware, plugins
import fastapi

import utils


app = fastapi.FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

if os.environ.get("REVERSE_PROXY", False):
    app.add_middleware(
        middleware.ContextMiddleware,
        plugins=(plugins.ForwardedForPlugin(),),
    )


@app.get("/api")
@cache(expire=360000)
async def list_entities():
    return {
        "documentation_swagger": app.url_path_for("swagger_ui_html"),
        "documentation_redoc": app.url_path_for("redoc_html"),
        "openapi": app.url_path_for("openapi"),
    }


@app.get("/api/restaurant")
@cache(expire=360000)
async def list_restaurants():
    return {
        "restaurants": utils.list_restaurants(),
    }


@app.get("/api/restaurant/{name}")
@cache(expire=10800)
async def get_restaurant(name):
    data = dict(utils.get_restaurant(name))
    if not data:
        raise fastapi.HTTPException(status_code=404, detail="Restaurant not found")
    data["menu"] = [{"dish": entry} for entry in data["menu"]]
    return {
        "restaurant": data,
    }


@app.get("/api/version")
@cache(expire=360000)
async def get_backend_version():
    ver = os.environ.get("VERSION", "")
    return {
        "version": ver,
    }


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
