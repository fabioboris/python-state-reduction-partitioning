import sys
from os.path import exists

from state import State
from type_aliases import InputMatrix


def get_input_from_file(file_name: str) -> InputMatrix:
    output: InputMatrix = []

    file = open(file_name, encoding="utf8")
    content = file.read()
    file.close()

    rows = content.split("\n")
    for row in rows:
        values = list(map(lambda x: int(x), row.split(",")))
        output.append(values)

    return output


def save_states_to_file(file_name: str, input: list[State]):
    rows: list[str] = []

    for _, state in input.items():
        rows.append(f"{state.x0.index},{state.y0},{state.x1.index},{state.y1}")

    content = "\n".join(rows)

    file = open(file_name, mode="w", encoding="utf8")
    file.write(content)
    file.close()


def get_file_name() -> str:
    attempts = 0
    while(attempts < 3):
        attempts += 1
        file_name = input("Please, type the input file name: ")

        if exists(file_name):
            return file_name

    print("Canceled.")
    sys.exit()
