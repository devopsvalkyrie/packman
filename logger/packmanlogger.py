import logging
import os
import sys
from tabulate import tabulate
from enum import IntEnum
from logging import Logger
from time import sleep
from singleton_decorator import singleton


@singleton
class PackmanLogger(Logger):
    """
    PackmanLogger is a custom logging class which can be used to unify log format across different parts of automation.

    There are several log levels:
    CRITICAL: This log level should be used in cases there is a threat of inconsistent state after the issue occurred.
              Termination of execution is expected after this log.
    ERROR: This log level should be used in cases of controlled exceptions with termination of execution afterward.
           For error level you can attach knowledge base link with complete explanation of particular error and how it
           can be fixed.
    WARNING: This log level should be used in cases of suspicious behaviours when no termination of execution is experted.
             The list of warning logs (warning_list) could be sent to the email after the execution (because no one reads
             logs when automation execution was successful).
    INFO: This log level should be used for human readable logs.
    DEBUG: This log level should be used to print any useful information for debugging purposes.
    TRACE: This log level should be used to print api requests/responses for debugging. It has its ows log level because
           api requests tent to be long and you could want to separate them from short debug messages.
    """

    class LogLevel(IntEnum):
        CRITICAL = 50
        ERROR = 40
        WARNING = 30
        INFO = 20
        DEBUG = 10
        TRACE = 5

    def __init__(self, log_level=None):
        self.logger = logging.getLogger("PACKMAN")
        self.logger.setLevel(log_level if log_level else "INFO")
        self.stream_handler = logging.StreamHandler(stream=sys.stdout)
        self.stream_handler.setFormatter(logging.Formatter(u"%(levelname)-s: %(message)s"))
        self.logger.addHandler(self.stream_handler)
        self.warning_list = []
        self.separator_length = 196
        self._update_log_levels()

    def __call__(self, log_level=None):
        self.stream_handler.setLevel(log_level if log_level else "INFO")
        self.logger.setLevel(log_level if log_level else "INFO")
        self.log_level = log_level
        return self

    def _update_log_levels(self):
        """
        Private function to add custom log levels to Python logging.
        """
        custom_log_levels = self.LogLevel
        for log_level in custom_log_levels:
            logging.addLevelName(log_level, log_level.name)

    def log(self, level, msg):
        if os.linesep in msg:
            separator = "#"
            separator_before = separator * (self.separator_length - len(level.name) - 2)
            separator_after = separator * self.separator_length
            wrapped_msg = "{sep_b}{linesep}{msg}{linesep}{sep_a}{linesep}".format(linesep=os.linesep, msg=msg,
                                                                                  sep_b=separator_before,
                                                                                  sep_a=separator_after)
        self.logger.log(level=level, msg=wrapped_msg)

    def warning(self, msg):
        self.warning_list.append(msg)
        self.log(level=self.LogLevel.WARNING, msg=msg)

    def error(self, msg, kb_entry_link=None):
        if kb_entry_link:
            self.log(level=self.LogLevel.ERROR, msg="{message}{linesep}More info at {link}"
                     .format(message=msg, linesep=os.linesep, link=kb_entry_link))
        else:
            self.log(level=self.LogLevel.ERROR, msg=msg)

    def info(self, msg):
        self.log(level=self.LogLevel.INFO, msg=msg)

    def debug(self, msg):
        self.log(level=self.LogLevel.DEBUG, msg=msg)

    def trace(self, msg):
        self.log(level=self.LogLevel.TRACE, msg=msg)

    def thread_log(self, flag, timeout, msg):
        time_passed = 0
        while flag.qsize() == 0:
            sleep(timeout)
            time_passed += timeout
            message = "{msg}: passed {time_passed} seconds".format(msg=msg, time_passed=time_passed)
            self.info(msg=message)

    def log_table(self, data):
        headers = data[0].keys()
        table = tabulate([item.values() for item in data], headers=headers, tablefmt='grid')
        msg = "{linesep}{table}{linesep}".format(linesep=os.linesep, table=table)
        self.log(level=self.LogLevel.INFO, msg=msg)

