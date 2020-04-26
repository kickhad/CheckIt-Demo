import logging
import os

class MyFileHandler(object):

    def __init__(self, dir, logger, handlerFactory, **kw):
        kw['filename'] = os.path.join(dir, logger.name)
        self._handler = handlerFactory(**kw)

    def __getattr__(self, n):
        if hasattr(self._handler, n):
            return getattr(self._handler, n)
        raise AttributeError(n)


formatter = logging.Formatter(
        '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        '%m-%d %H:%M:%S')


def log_factory(logname):
    log_dir = os.path.join('c:\\prod\\prod01\\app1\\logs\\')
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # fh = MyFileHandler(log_dir, logger, logging.FileHandler)
    fh = logging.FileHandler(logname + '1' + '.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # ch.setStream(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


'[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s,%m-%d %H:%M:%S'
