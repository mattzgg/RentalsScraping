import configparser
from pathlib import Path

DB_CONFIG_FILE_NAME_PATTERN = "db_config.*.ini"
db_config_dir_path = Path(Path(__file__), "../../../config").resolve()


def get_db_config_file_name_help():
    more_info = (
        "There are no usable database config files under the 'config' directory. "
        + "The name of a database config file should follow the '{}' pattern."
    ).format(DB_CONFIG_FILE_NAME_PATTERN)
    file_names = get_available_db_config_file_names()
    if file_names:
        more_info = "The available names is/are: {}".format(", ".join(file_names))
    return "The database configuration file name. " + more_info


def get_db_connection_parameters(db_config_file_name):
    file_path = Path(db_config_dir_path, "./", db_config_file_name).resolve()
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)
    connection_parameters_section = config_parser["ConnectionParameters"]

    return {
        "host": connection_parameters_section.get("host"),
        "database": connection_parameters_section.get("database"),
        "user": connection_parameters_section.get("user"),
        "password": connection_parameters_section.get("password"),
        "time_zone": connection_parameters_section.get("time_zone"),
    }


def get_available_db_config_file_names():
    file_paths = sorted(db_config_dir_path.glob(DB_CONFIG_FILE_NAME_PATTERN))
    names = []
    for file_path in file_paths:
        names.append(file_path.name)
    return names