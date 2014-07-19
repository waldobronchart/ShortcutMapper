import sys
import logging


class LogData(object):
    log_instance = logging.Logger('default')


def getlog():
    """Get the global log setup by the __main__ script"""

    if LogData.log_instance is None:
        setuplog()

    return LogData.log_instance


def setuplog(output_file=None):
    """Setup the global log. Add more specific settings as you please."""

    log = LogData.log_instance
    if LogData.log_instance is None:
        log = logging.Logger()
    log.name = 'main'

    # Format
    formatter = logging.Formatter('%(asctime)s %(levelname)8s %(module)10s.py@%(lineno)-3d   %(message)s')

    # Output to std out
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.formatter = formatter
    log.addHandler(stdout_handler)

    # Output to file
    if output_file is not None:
        file_handler = logging.FileHandler(output_file, 'w')
        file_handler.formatter = formatter
        log.addHandler(file_handler)

    LogData.log_instance = log
    return LogData.log_instance


