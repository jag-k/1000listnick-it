from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from extensions import *
from db import *

app = Sanic(__name__)

app.blueprint(calendar)


@app.route('/')
def main_r(req: Request):
    with db_session:
        return json(URL.select().first().to_dict())


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8080,
    )
