import tempfile

from config import Config

config = Config()
tempfile.tempdir = config.TEMPDIR


def dump_dataframe(df):
    fn = tempfile.mktemp()
    df.to_pickle(fn)
    return fn
