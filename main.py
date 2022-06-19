import os
import re
from argparse import ArgumentParser


def execute(args):
    os.makedirs(args.name, exist_ok=True)
    open(os.path.join(args.name, "__init__.py"), "w").close()
    open(os.path.join(args.name, "config.py"), "w").close()
    open(os.path.join(args.name, "logger.py"), "w").close()

    output_lines = []
    with open("pyproject.toml") as file:
        for line in file.readlines():
            if "name = " in line:
                line = re.sub(r"\"[\w-]+\"", f"\"{args.name}\"", line)
            output_lines.append(line)

    with open("pyproject.toml", "w") as file:
        for line in output_lines:
            file.write(line)

    if args.tests:
        os.makedirs("tests", exist_ok=True)


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "-n", "--name", default="app", help="name of the project"
    )
    parser.add_argument(
        "-t", "--tests", action="store_true", help="If the project will be tested"
    )

    args = parser.parse_args()
    print(args)
    execute(args)


if __name__ == "__main__":
    main()
