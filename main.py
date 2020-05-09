from os import system

STEPS = [
    {
        "answer": "1",
        "name": "Переключиться на первый этап",
        "cmd":
        # language=Bash
            "git checkout first-step",
    },
    {
        "answer": "2",
        "name": "Переключиться на второй этап",
        "cmd":
        # language=Bash
            "git checkout second-step",
    },
    {
        "answer": "0",
        "name": "Выйти",
        "cmd":
        # language=Bash
            "exit",
    }
]

answer = "-1"
while answer not in map(lambda x: x["answer"], STEPS):
    print("Выберите команду:")
    for n in STEPS:
        print("%(answer)s: %(name)s" % n)
    try:
        answer = input()
    except KeyboardInterrupt:
        answer = "0"

print("Выполняем действие...")
system(list(filter(lambda x: x["answer"] == answer, STEPS))[0]["cmd"])
