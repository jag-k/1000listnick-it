import json

from pony.orm import *


db = Database()
db.bind(
    provider='postgres',
    **json.load(open('database_config.json'))
)


class Message(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str)
    title = Optional(str, default="")
    content = Optional(str, default="")
    as_html = Optional(bool, default=False)
    status = Optional(str, default="wait")  # ok or err


db.generate_mapping(create_tables=True)
