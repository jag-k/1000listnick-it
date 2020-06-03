import os
from json import load
from model import *

db.bind(**load(open('database_settings.json')))
db.generate_mapping(create_tables=True)


if __name__ == '__main__':
    with db_session:
        User.select().show()
