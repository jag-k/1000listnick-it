from color_class import Color
from email.db import *


def add_to_queue(email: str, title: str = "", content: str = "", as_html: bool = False):
    with db_session:
        n = Message(
            email=email,
            title=title,
            content=content,
            as_html=as_html,
        )
        commit()
        # Message.select().show()


def send(*emails: str, real_send: bool = False):
    if not emails:
        filter_email = lambda x: x.status == "wait"
    else:
        filter_email = lambda x: x.status == "wait" and x.email in emails

    n = 0
    with db_session:
        for m in Message.select(filter_email):
            if real_send:
                m.status = "ok"  # TODO: Сделать реальную отправку по EMAIL.
            else:
                m.status = "ok"
            n += 1
    return n


def check(*emails, email_count: int = -1, status: str = None):
    if status == "all":
        if not emails:
            filter_email = lambda x: True
        else:
            filter_email = lambda x: x.email in emails
    elif status is not None:
        if not emails:
            filter_email = lambda x: x.status == status
        else:
            filter_email = lambda x: x.status == status and x.email in emails

    with db_session:
        s = Message.select(filter_email)
        if email_count > 0:
            s = s[:email_count]
        s = list(s)
        if not s:
            print("Сообщений в очереди не найдено...")
        else:
            print("Найдено %s сообщений:" % Color(str(len(s)), Color.THUMBNAIL, Color.GREEN), end="")
        for m in s:  # type: Message
            print("""
Почта: %s
Статус отправки: %s
Заголовок: %s
Это HTML?: %s
Контент: %s""" % (
                Color(m.email, Color.THUMBNAIL, Color.UNDERLINE, Color.BLUE),
                Color(m.status.upper(), {
                    "ok": Color.GREEN,
                    "err": Color.RED,
                    "wait": Color.BLUE
                }.get(m.status, 0), Color.THUMBNAIL),
                Color(m.title, Color.THUMBNAIL),
                Color("Да", Color.GREEN) if m.as_html else Color("Нет", Color.RED),
                Color(m.content, Color.THUMBNAIL),
            ))

