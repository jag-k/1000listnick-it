import hashlib
import binascii
import os

from json import load
from model import *

if os.getenv("LOCAL", "False").lower() == "true":
    db.bind(provider="sqlite", filename=":memory:")
else:
    db.bind(**load(open('database_settings.json')))
db.generate_mapping(create_tables=True)


def hash_user(email, pwd):
    dk = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=b'%s ---- %s' % (email, pwd),
        salt=b'lorem {email} ipsum!, please',
        iterations=100000
    )
    return str(binascii.hexlify(dk), encoding="utf-8")


def is_user(login, pwd):
    return is_hash_user(hash_user(login, pwd))


@db_session
def is_hash_user(user_hash):
    return user_hash and exists(user_hash == u.hash for u in User)


@db_session
def get_user_by_email(email: str) -> User:
    return get(u for u in User if u.email == email)


@db_session
def get_user_by_hash(user_hash: str) -> User:
    return get(u for u in User if u.hash == user_hash)


@db_session
def get_user(email_hash_id):
    return select(u for u in User if email_hash_id in (u.email, u.hash, u.id)).first()


@db_session
def create_user(email: str, password: str, name: str = "") -> User or None:
    if not password:
        return None
    h = hash_user(email, password)
    user = get_user_by_hash(h)

    if not user and not get(u.email == email for u in User):
        return User(email=email, hash=h, name=name or email.split("@")[0])
    else:
        return user


@db_session
def del_user(email_hash_id):
    u = get_user(email_hash_id)
    if u:
        u.delete()
        return True
    return False


@db_session
def edit_user_password(email_hash_id, password: str):
    u = get_user(email_hash_id)
    u.hash = hash_user(u.email, password)
    return u


@db_session
def edit_user_data(user: User, name: str = None, email: str = None, password: str = None, **kwargs) -> User:
    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.hash = hash_user(user.email, password)
    commit()
    return user


if __name__ == '__main__':
    with db_session:
        User.select().show()
