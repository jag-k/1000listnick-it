import os

from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from db import *

app = Sanic(__name__)


@app.route('/')
def main_r(req: Request):
    with db_session:
        return json(URL.select().first().to_dict())


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
        host="0.0.0.0",
        port=port,
        auto_reload=True,
        ssl=ssl_conn,
    )


# for i in range(200):
#     print(i, "\033[%sm Hello_!\033[0m" % i)
