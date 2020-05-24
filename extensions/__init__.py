import os
import sys

path = __file__.rsplit('/', 1)[0]

r, dirs, _ = next(os.walk(path))
for d in filter(lambda x: not x.startswith("__"), dirs):
    sys.path.append(os.path.join(r, d))

try:
    from extensions.calendar.main import app as calendar

finally:
    pass
