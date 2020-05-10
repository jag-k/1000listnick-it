from email.db import *


def add_to_queue(email: str, title: str = "", content: str = "", as_html: bool = False):
    with db_session:
        n = Message(
            email=email,
            title=title,
            content=content,
            as_html=as_html,
        )
        print(n)
        commit()
        Message.select().show()


def send(*emails: str):
    if not emails:
        pass
