import os
import time
from logger.packmanlogger import PackmanLogger


def retry(func, retry_count=3):

    def retry_query(*args, **kwargs):
        for attempt in range(retry_count):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as ex:
                PackmanLogger.error(msg="""Attempt {attempt_no} of {total_attempts} failed with exception:
                                        {linesep}{exception}"""
                                        .format(attempt_no=attempt+1, total_attempts=retry_count, linesep=os.linesep,
                                                exception=str(ex)))
                if attempt == retry_count-1:
                    raise ex
                time.sleep(1)
                continue
    return retry_query
