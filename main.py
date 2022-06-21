import os
import re
from argparse import ArgumentParser

logger = """import logging


class Format(logging.Formatter):
    grey = "\\x1b[38;21m"
    yellow = "\\x1b[33;21m"
    red = "\\x1b[31;21m"
    bold_red = "\\x1b[31;1m"
    reset = "\\x1b[0m"
    green = "\\x1b[32m"
    asctime = "%(asctime)s"
    name = "[%(name)s]"
    levelname = "[%(levelname)-4s]"
    message = "%(message)s"

    FORMATS = {
        logging.DEBUG: f"{asctime} {grey} {name} {levelname} {reset} {message}",
        logging.INFO: f"{asctime} {green} {name} {levelname} {reset} {message}",
        logging.WARNING: f"{asctime} {yellow} {name} {levelname} {message} {reset}",
        logging.ERROR: f"{asctime} {red} {name} {levelname} {message} {reset}",
        logging.CRITICAL: f"{asctime} {bold_red} {name} {levelname} {message} {reset}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def create_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = Format()

    # file
    file = logging.FileHandler(f"{logger_name}.log")
    file.setLevel(level=logging.DEBUG)
    file.setFormatter(formatter)

    # console
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(file)
    logger.addHandler(console)

    return logger
"""


def execute(args):
    os.makedirs(args.name, exist_ok=True)
    open(os.path.join(args.name, "__init__.py"), "w").close()
    open(os.path.join(args.name, "config.py"), "w").close()

    with open(os.path.join(args.name, "logger.py"), "w") as file:
        file.write(logger)

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
