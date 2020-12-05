import signal
import logging
import logging.handlers
import logging.config
from pathlib import Path
from time import sleep


class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        new_args = list(args)
        filename = args[0]
        new_args[0] = str(Path(Path(__file__), "../../../logs/", filename).resolve())
        args = tuple(new_args)
        super().__init__(*args, **kwargs)


def logging_listener_worker(log_config_file_path, log_queue, sigint_event):
    """Whether this configuration can come from a configuration file?"""
    # Ignore the KeyboardInterrupt event in the first place.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    logging.config.fileConfig(log_config_file_path)

    while True:
        while not log_queue.empty():
            record = log_queue.get()
            logger = logging.getLogger(record.name)
            logger.handle(record)
        if sigint_event.is_set():
            break
        else:
            sleep(1)


def configure_log_dispatcher(log_queue):
    handler = logging.handlers.QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)