#! /usr/bin/python3
import argparse

from email import *

parser = argparse.ArgumentParser(
    description="Задание на реализацию очереди"
)
parser.add_argument(
    "-n", "--no-color", action="store_true", default=False,
    help="Убрать цветной вывод"
)

subparser = parser.add_subparsers(help="Возможные команды")

# === ADD COMMAND ===

add_queue = subparser.add_parser("add", help="Добавить в очередь на отправку")
add_queue.add_argument(
    "email", action="store", type=str,
    help="Message получателя"
)
add_queue.add_argument(
    "-t", "--title", action="store", type=str, nargs="*",
    help="Заголовок письма"
)
content_g = add_queue.add_mutually_exclusive_group()
content_g.add_argument(
    "-m", "--message", action="store", type=str, nargs="*",
    help="То, что будет отправлено пользователю"
)
content_g.add_argument(
    "-f", "--file", action="store", type=open,
    help="Взять контент для отправки из файла (требует путь к файлу)"
)
content_g.add_argument(
    "-H", "--html", action="store", type=open,
    help="Отправить HTML (требует путь к файлу)"
)

# === SEND COMMAND ===

send_queue = subparser.add_parser("send", help="Отправить из очереди")
send_queue.add_argument(
    "emails", action="store", type=str, nargs="*",
    help="Отправить сообщения на данные email адреса"
)
send_queue.add_argument(
    "-a", "--all", action="store_true", default=False,
    help="Отправить ВСЕ сообщения из очереди (игнорирует введённые адреса)"
)
send_queue.add_argument(
    "-r", "--real-send", action="store_true", default=False,
    help="Совершить РЕАЛЬНУЮ отправку на почты (пока не реализованно)"
)

# === CHECK COMMAND ===

check_queue = subparser.add_parser("check", help="Посмотреть сообщения")
check_queue.add_argument(
    "emails", action="store", type=str, nargs="*",
    help="Показывает историю сообщений на данные email адреса (по умолчанию все)"
)
check_queue.add_argument(
    "-s", "--status", action="store", type=str, choices=("all", "ok", "err", "wait"), default="all",
    help="Показывает сообщения в очереди (wait), отправленные (ok), с ошибкой (err) и все сообщения (all)"
)
check_queue.add_argument(
    "-c", "--count", action="store", type=int, default=-1,
    help="Количество сообщений, которые будут показаны (по умолчанию, все)"
)

argv = parser.parse_args()

# print(argv)
if argv.no_color:
    Color.DE_COLOR = True


def main():
    if "email" in argv:  # ADD
        as_html = False
        if argv.html:
            with argv.html as file:
                content = file.read()
                as_html = True
        elif argv.file:
            with argv.file as file:
                content = file.read()
        else:
            content = " ".join(argv.message)

        add_to_queue(
            email=argv.email,
            title=' '.join(argv.title),
            content=content,
            as_html=as_html,
        )
        print("Сообщение для %s добавлено в очередь!" % Color(argv.email, Color.THUMBNAIL, Color.UNDERLINE, Color.BLUE))

    elif "all" in argv:  # SEND
        send_count = send(*(argv.emails if not argv.all else []), real_send=argv.real_send)
        print("Отправлено %s сообщений" % Color(send_count, Color.THUMBNAIL, Color.GREEN))

    elif "status" in argv:  # CHECK
        check(*argv.emails, email_count=argv.count, status=argv.status)

    else:  # NO COMMAND
        parser.print_help()


if __name__ == '__main__':
    main()
