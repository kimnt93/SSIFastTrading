import logging
import time
import random
from datetime import datetime, timedelta
from dateutil import parser

DEFAULT_DATE_FORMAT = "%d/%m/%Y"


def run_forever(t=600):
    while True:
        logging.info('Running forever...')
        time.sleep(t)


def generate_request_id():
    return str(random.randint(0, 99999999))


def ensure_default_ssi_day_format(start_date, end_date):
    """
    Always convert to %d/%m/%Y format
    :param start_date:
    :param end_date:
    :return:
    """
    # If start_date and end_date are None, set default values
    if start_date is None:
        start_date = datetime.now().strftime(DEFAULT_DATE_FORMAT)
        end_date = (datetime.now() + timedelta(days=1)).strftime(DEFAULT_DATE_FORMAT)
    else:
        if isinstance(start_date, str):
            start_date = parser.parse(start_date)

        if isinstance(end_date, str):
            end_date = parser.parse(end_date)

        start_date = start_date.strftime(DEFAULT_DATE_FORMAT)
        end_date = end_date.strftime(DEFAULT_DATE_FORMAT)

    return start_date, end_date
