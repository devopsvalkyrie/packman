import threading
from logger.packmanlogger import PackmanLogger


def thread_session(func):
    sessions = threading.local()

    def wrapper(*args, **kwargs):
        if 'session' not in sessions.__dict__:
            PackmanLogger.info(msg='Current thread: {id}'.format(id=threading.current_thread().ident))
            sessions.session = func(*args, **kwargs)
        session = sessions.session
        return session
    return wrapper
