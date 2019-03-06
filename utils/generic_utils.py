import logging
import os
from configparser import ConfigParser
from datetime import date, datetime
from os.path import join, dirname, abspath

CUR_DATE = str(date.today())
BASE_DIR = dirname(dirname(abspath(__file__)))


def get_logs_directory():
    try:
        log_dir_loc = os.path.normpath(BASE_DIR + os.sep + os.pardir)
        os.makedirs(join(log_dir_loc, 'logs'), exist_ok=True)
        log_dir = join(log_dir_loc, 'logs')
        return log_dir
    except Exception as e:
        print("CRITICAL : Unable to create logs directory %s" % str(e))


def get_logger(name):
    log_format = '%(asctime)s  %(levelname)5s %(name)5s %(message)s'
    log_fname = join(get_logs_directory(), 'logfile_%s.log' % CUR_DATE)
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename=log_fname,
                        filemode='a+')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def get_app_config():
    config = ConfigParser()
    config.optionxform = str
    app_config = join(BASE_DIR, "app_config.ini")
    logger = get_logger(__name__)
    logger.info("Reading config for app")
    config.read(app_config)
    d = _read_config(config)
    return d


def _read_config(config):
    d = {}
    for section in config.sections():
        d[section] = {}
        for option in config.options(section):
            d[section][option] = config.get(section, option)
    return d


def diff_dates(latest, previous):
    latest = datetime.strptime(latest, "%Y-%m-%d %H:%M:%S")
    previous = datetime.strptime(previous, "%Y-%m-%d %H:%M:%S")
    return latest > previous


def epoch_to_timestamp(epoch):
    logger = get_logger(__name__)
    logger.info("Converting epoch(%s) to datetime" % (epoch))
    s, ms = divmod(int(epoch), 1000)
    timestamp = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


def increment_id(str_id, digits=4):
    s = str_id.split("_")
    s[-1] = str(int(s[-1]) + 1).zfill(digits)
    s = '_'.join(s)
    return s
