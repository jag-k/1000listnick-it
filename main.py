import sys
from os import system

STEPS = [
    {
        "name": 'Запустить "Задачу на алгоритмизацию"',
        # language=Bash
        "cmd": 'echo "\nДля просмотра справки запустите следующую команду:\n%s file_search.py --help\n" &&'
               ' %s file_search.py' % (sys.executable, sys.executable),
    },
    {
        "name": "Переключиться в мастер",
        # language=Bash
        "cmd": "git checkout master",
    }
]

EXIT_COMMAND = {
        "name": "Выйти",
        # language=Bash
        "cmd": "exit"
    }

answer = "-1"
while not (answer.isnumeric() and int(answer) in range(len(STEPS)+1)):
    print("Выберите команду:")
    for i in range(len(STEPS)):
        print("%s: %s" % (i+1, STEPS[i]['name']))

    print("0: %s" % EXIT_COMMAND['name'])
    try:
        answer = input()
    except KeyboardInterrupt:
        answer = "0"
        break


STEPS.insert(0, EXIT_COMMAND)

print("Выполняем действие...")
system(STEPS[int(answer)]["cmd"])
