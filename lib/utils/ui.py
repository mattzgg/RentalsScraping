import os, traceback

from termcolor import colored


def create_info(text):
    return colored(text, "green")


def create_warning(text):
    return colored(text, "yellow")


def create_error(text):
    return colored(text, "red")


def print_exception(message=""):
    module_path = os.path.dirname(__file__)
    package_path = "/{}".format(__package__.replace(".", "/"))
    project_path = module_path[0 : len(module_path) - len(package_path)]

    new_traceback_lines = []
    traceback_lines = traceback.format_exc().splitlines()
    for traceback_line in traceback_lines:
        new_traceback_lines.append(traceback_line.replace(project_path, ""))

    print(create_error("\nAN ERROR OCCURRED: {}".format(message)))
    for new_traceback_line in new_traceback_lines:
        print(create_error(new_traceback_line))
