from os import system

STEPS = [
    {
        "name": "Переключиться на первый этап",
        # language=Bash
        "cmd": "git checkout first-stage",
    },
    {
        "name": "Переключиться на второй этап",
        # language=Bash
        "cmd": "git checkout second-stage",
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
