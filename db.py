import os
from json import load

from pony.orm import *

if not os.path.exists("db.sqlite3"):
    with open("db.sqlite3", "w") as file_db:
        file_db.write("")

db = Database()
db.bind(**load(open('database_settings.json')))


class URL(db.Entity):
    original = PrimaryKey(str)
    short = Required(str, unique=True)


db.generate_mapping(create_tables=True)


if __name__ == '__main__':
    with db_session:
        URL.select().show()
        # URL(
        #     original="https://yandex.ru",
        #     short="ya"
        # )
