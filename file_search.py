# /usr/bin/python3
import argparse
import os
import re
import sys
import threading
from queue import Queue, Empty
from functools import wraps
from time import time
from types import FunctionType
from typing import List, Union

TIMEOUT = True
DEFAULT_TIMEOUT = 60
PRINT_STRING = "\rНайден файл: %s"

search_q = Queue()
kill_thread = Queue()

parser = argparse.ArgumentParser(
    description="Задание на алгоритмизацию"
)

parser.add_argument(
    "file", action="store", type=str, default=False, nargs='?',
    help="Полное имя файла"
)

parser.add_argument(
    "-r", "--root", action="store", default="/", type=str,
    help="Корневая директория, откуда будет производится поиск"
)

parser.add_argument(
    "-o", "--output", action="store", type=str, default=False,
    help="Имя файла, в которое запишутся пути файлов"
)

parser.add_argument(
    "-q", "--quiet", action="store_true", default=False,
    help='Включает "тихий" режим, то есть ничего не выводится в консоль (предназначено в основном для вывода в файл)'
)

parser.add_argument(
    "--regexp", action="store_true", default=False,
    help='Вместо имени файла принимает н̶а̶р̶к̶о̶т̶и̶к̶и̶ Regular Expression (Регулярное выражение)'
)

parser.add_argument(
    "-t", "--timeout", action="store", default=DEFAULT_TIMEOUT, type=int,
    help="Таймаут поиска (по умолчанию %d секунд). Для выключения введите -1" % DEFAULT_TIMEOUT
)

parser.add_argument(
    "-i", "--ignore", action="append", default=[], nargs="*",
    help="Игнорирование директорий"
)

argv = parser.parse_args()
argv.ignore = [i for j in argv.ignore for i in j]

results = []
filename = argv.file if argv.file else input("Введите имя файла: ")


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    groups = {}

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        StoppableThread.groups.setdefault(name, [])
        StoppableThread.groups[name].append(self)
        super(StoppableThread, self).__init__(group, target, name,
                                              args, kwargs, daemon=daemon)
        self.stop_event = threading.Event()

    def stop(self):
        for th in StoppableThread.groups.get(self.name, []):
            kill_thread.put(self.name)
            th.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


def thread(func: FunctionType = None, daemon: bool = False) -> Union[StoppableThread, FunctionType]:
    def w(f: FunctionType):
        @wraps(f)
        def decorate(*args, NO_THREAD=False, **kwargs):
            if NO_THREAD:
                return f(*args, **kwargs)
            th = StoppableThread(target=f, name=f.__name__, args=args, kwargs=kwargs, daemon=daemon)
            th.start()
            return th

        return decorate

    if func is None:
        return w
    return w(func)


@thread(daemon=True)
def pol(*value, sep=" "):
    """
    Print On Line

    :param value: Some values
    :type value: Any
    :param sep: Separator
    :type sep: str
    :return: None
    :rtype: None
    """
    return print('\r' + sep.join(map(str, value)), end='', flush=True)


try:
    if not argv.output:
        raise PermissionError
    with open(argv.output, "w") as file:
        file.write("")
    if argv.quiet:
        @thread(daemon=True)
        def print_res(p, *a):
            with open(argv.output, "a") as f:
                f.write(os.path.join(p, *a) + '\n')
    else:
        @thread(daemon=True)
        def print_res(p, *a):
            path = os.path.join(p, *a)
            with open(argv.output, "a") as f:
                f.write(path + '\n')
            print(PRINT_STRING % path)

except PermissionError:
    if argv.quiet:
        def print_res(p, *a):
            pass
    else:
        @thread(daemon=True)
        def print_res(p, *a):
            print(PRINT_STRING % os.path.join(p, *a))

if argv.regexp:
    try:
        f_re = re.compile(filename, re.MULTILINE)
    except re.error as err:
        print("Ошибка во время компиляции регулярного выражения!: %s" % err, file=sys.stderr)

    def find_file(files: List[str]) -> List[str]:
        return f_re.findall("\n".join(files))

else:
    def find_file(files: List[str]) -> List[str]:
        return list(filter(filename.__eq__, files))


def is_killed(func_name: str) -> bool:
    try:
        kill = kill_thread.get_nowait()
        if kill == func_name:
            return True
        kill_thread.put(kill)
        return False
    except Empty:
        return False


@thread
def search(root: str = argv.root):
    global TIMEOUT
    try:
        for r, directories, files in os.walk(root):
            if is_killed("search"):
                break
            if any(map(lambda x: x in r, argv.ignore)):
                continue
            pol(r)
            for i in find_file(files):
                search_q.put_nowait(os.path.join(r, i))
        search_q.put(None)
        TIMEOUT = False
    except KeyboardInterrupt:
        return


@thread(daemon=True)
def watcher(queue: Queue):
    while True:
        r = queue.get()
        if is_killed("watcher") or r is None:
            break
        print_res(r)
        results.append(r)


def stop(*threads: StoppableThread):
    for th in threads:
        if th.is_alive():
            th.stop()
            th.join()


def main():
    root = os.path.abspath(argv.root)
    print('Выполняется поиск по директории "%s"...' % root)
    print('Для прерывания программы нажмите ⌃C\n')
    t1 = time()
    s = search(root)
    w = watcher(search_q)
    try:
        if argv.timeout > 0:
            s.join(argv.timeout)
            stop(s, w)
            t2 = time()
            pol(
                " \nТаймаут!\n"
                if TIMEOUT else
                " \nПоиск завершён!\n"
            )
        else:
            s.join()
    except KeyboardInterrupt:
        stop(s, w)
        t2 = time()
        pol("Завершение поиска пользователем\n")

    res = sorted(set(results))

    pol('Нашлось %d за %d сек.\n' % (len(res), int(t2 - t1)))
    print(*res, sep="\n")


if __name__ == '__main__':
    main()
