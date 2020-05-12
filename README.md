# 1000-LIST-NICK (IT)
🎉 Вы открыли первый этап! 🎉

[📄 Ссылка на само задание ⬀](https://docs.google.com/document/d/1wYLULwmx8y3N35BXD0Nx3g_r2SZH2eyxUFXkvFM4S8E)

 - [1 этап ⬀](https://github.com/jag-k/1000listnick-it/tree/first-stage)
 - [2 этап ⬀](https://github.com/jag-k/1000listnick-it/tree/second-stage)


<h3 align="center"> ⚠️ ВАЖНО Для работы программы необходимо установить зависимости! Как это сделать написано ниже! ⚠️ </h3>

## Как запустить проект? 
1. Для начала, должен быть установлен [`python`⬀](https://www.python.org/downloads/) версии не ниже `3.7` и [`git`⬀](https://git-scm.com/downloads)
1. После установки нужно склонировать проект в удобное для Вас место командой `git clone https://github.com/jag-k/1000listnick-it.git`
1. Затем перейти в папку проекта `cd 1000listnick-it` и выбрать 1-й этап: `git checkout first-stage`
1. Установите зависимости командой `pip install -r reqirements.txt` или `python -m pip install -r reqirements.txt` 
1. Для запуска проекта используйте команду  `python main.py` ИЛИ запустите конкретное задание:
    - 1-е задание (Поиск файла): `python file_search.py`
    - 2-e задание (Рассылка почты): `python email`. **ОБРАТИТЕ ВНИМАНИЕ НА ОТСВУТСВИЕ ПОСТВИКСА `.py`**

## Настройки проекта
Для получения справки добавьте флаг `-h` или `--help` во время запуска задания.
Например: `python file_search.py --help`

<img align="left" width="46%" src="https://github.com/jag-k/1000listnick-it/raw/first-stage/.github/help_page2.png"/>

<img align="right" width="49%" src="https://github.com/jag-k/1000listnick-it/raw/first-stage/.github/help_page.png"/>

Справа страница помощи 1-го задания: `python file_search.py --help`

Слева страницы помощи 2-го задания: `python email --help`, `python email add --help`, `python email send --help` и `python email check --help`


## Примеры запуска заданий
Пример запуска 1-го задания: 
```bash
python file_search.py .*\.py -o res.txt --regexp -r ./ -i venv .venv --ignore __pycache__
```
> Ищет все `.py` файлы в текущей директории, игнорируя питоновские временные и "системные" файлы, а так же записывает результат в `res.txt` файл


Примеры запуска 2-го задания:
```bash
python email add me@jagk.ru --title Отчёт о поиске -f res.txt
```
> Добавляет в очередь сообщение для _me@jagk.ru_ с заголовком `Отчёт о поиске`. Телом сообщения являются данные из файла `res.txt`, в которых записан отчёт выполнения предыдущей команды запуска 1-го задания

```bash
python email check -s wait
```
> Показывает все сообщения в очереди
 
```bash
python email send -a
```
> Отправляет все сообщения из очереди


#### Настройки подключения к базе данных для 2-го задания
Файл для конфигурации: `database_config.json`.
Используется база данных [PostgreSQL](https://www.postgresql.org)

Ключ     | Значение по умолчанию | Тип   | Описание
-------- | --------------------- | ----- | ---------------------------
user     | `""`                  | `str` | Логин от базы данных
password | `""`                  | `str` | Пароль от базы данных
host     | `"localhost"`         | `str` | Хост/путь к базе данных
port     | `5432`                | `int` | Порт подключения
database | `"postgres"`          | `str` | Название самой базы данных


## Какие зависимости есть, и зачем они нужны?
Все эти зависимости относятся к 2-му заданию `./email/`
> То есть `file_search.py` можно использовать и без установки этих зависимостей

Библиотека                                    | Её предназначение
--------------------------------------------- | -----------------
[pony](https://pypi.org/pony)                 | [PonyORM](https://ponyorm.org) - Это [ORM](https://ru.wikipedia.org/wiki/ORM) Для работы с базами данных
[psycopg2cffi](https://pypi.org/psycopg2cffi) | Позволяет работать [PonyORM](https://ponyorm.org) с БД [PostgreSQL](https://www.postgresql.org)

## Мои контакты
Если будут вопросы по проекту, то вот как со мной связаться: 
- [👥 VK](https://vk.com/jag_konon)
- [:octocat: GitHub](https://github.com/jag-k)
- [🌐 Мой вебсайт (да, там ничего нет)](https://jagk.ru)
- [📧 jagk58@ya.ru](mailto:jagk58@ya.ru)
