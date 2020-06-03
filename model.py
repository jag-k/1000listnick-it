from datetime import timedelta
from pony.orm import *


db = Database()


class User(db.Entity):
    email = PrimaryKey(str, auto=True)
    hash = Required(str, hidden=True)
    vk = Optional(int, unique=True)
    timetables = Set('Timetable', reverse='user')
    contribution = Set('Timetable', reverse='contributors')


class Timetable(db.Entity):
    """permission types:
        hide: Only "admin" user can read/write Timetable
        read: Contributes and "admin" user only"""
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    permission = Optional(str, default='hide')
    start_lesson = Required(timedelta)
    lesson_duration = Required(timedelta)
    break_duration = Required(timedelta)
    user = Required(User, reverse='timetables')
    contributors = Set(User, reverse='contribution')
    days = Set('Day')
    repeatable = Optional(str)


class Day(db.Entity):
    id = PrimaryKey(int, auto=True)
    week_day = Required(int, size=8, default=1)  # from range 0 (sun) to 6 (sat)
    timetable = Required(Timetable)
    lessons = Set('Lesson')


class Lesson(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    location = Optional(str)
    days = Set(Day)



db.generate_mapping()