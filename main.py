from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from extensions import *
# from db import *

app = Sanic(__name__)

app.blueprint(calendar, url_prefix="/calendar")


@app.route('/')
def main_r(req: Request):
    return json(
        list(map(lambda route: route.uri, calendar.routes))
    )


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8080,
    )
