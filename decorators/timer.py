import time
import threading
from logger.packmanlogger import PackmanLogger


def timer(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.gmtime(time.time()-start)
        PackmanLogger.debug(msg="Function {func} ran for {time} minute(s) in {thread} thread"
                            .format(func=func.__name__, time=time.strftime('%H.%M.%S', end),
                                    thread=str(threading.current_thread().ident)))
        return result
    return wrapper
