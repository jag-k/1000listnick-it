import os
from json import loads

import jinja2_sanic
import jinja2
from sanic.exceptions import NotFound, SanicException

from jinja2_sanic import render_template as temp, template

from sanic import Sanic
from sanic.request import Request
from sanic.response import json, text, redirect, HTTPResponse
from sanic.compat import Header

from db import *

app = Sanic(__name__)

jinja2_sanic.setup(
    app,
    loader=jinja2.FileSystemLoader("./view"),
    autoescape=jinja2.select_autoescape()
)


@app.route('/')
async def main_r(req: Request):
    with db_session:
        return json({
            "headers": {**dict(req.headers), "sec-ch-ua": None},
            "data": loads(User.select().to_json())
        })


def alert(message: str, _type: str = "warning"):
    return {
        "Set-Cookies": "alert=%s;alert_type=%s" % (message, _type)
    }


@app.route("/register")
@template("register.jinja2")
async def reg_user(req: Request):
    print(req.method)
    if req.method == "POST":
        form = req.form

        with db_session:
            create_user(form.get("email"), form.get("password"))
        return redirect("/", alert("User"))

    return {
        "users": ["user"]
    }


@app.exception(NotFound)
def handler(req: Request, exc: SanicException):
    return json({
        "message": {
            "error": "Not found",
            "path": req.url,
            "status": 404
        }
    }, 404)


app.static("/", "public")

if __name__ == '__main__':
    ssl_conn = None

    if os.getenv("LOCAL", "false").lower() == "true":
        import ssl
        ssl_conn = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        ssl_conn.load_cert_chain("./localhost.crt", keyfile="./localhost.key")

    port = os.getenv("SERVER_PORT", "null")
    if port.isdigit():
        port = int(port)
    elif ssl_conn is not None:
        port = 443
    else:
        port = 80

    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=port,
        auto_reload=True,
        ssl=ssl_conn,
    )
