"""Helpers to manipulate times"""

import logging
import re
from datetime import datetime, timedelta

import arrow
from dateutil import tz

LOG = logging.getLogger(__name__)


####################################################################
### Datetime primitives
###


def get_unix_ts_unit(unix_ts):
    """Check if linux timestamp units are in seconds or ms."""
    if len(unix_ts) == 13:
        unit = "ms"
    elif len(unix_ts) == 10:
        unit = "s"
    else:
        raise ValueError("Unix timestamp is not in seconds or milliseconds")
    return unit


def convert_unix_time(unix_time):
    """Convert unix timestamp to date-time object."""
    return datetime.fromtimestamp(unix_time / 1000, tz=tz.tzutc())


def unixtime_to_datestring(unix_time, fmt_str="%Y-%m-%d %H:%M:%S"):
    """Convert unix timestamp into a string."""
    return datetime.fromtimestamp(unix_time).strftime(fmt_str)


def unixtime_to_datetime(unix_time):
    """Convert unix timestamp into a string."""
    return datetime.utcfromtimestamp(unix_time)


# TODO: unify redundant time functions
def time_from_string(mytime_str, tformat="%H:%M"):
    """Converts a string into a time object."""
    return datetime.strptime(mytime_str, tformat).time()


def date_from_string(mydate_str):
    """Converts a string into a date object."""
    return datetime.strptime(mydate_str, "%Y-%m-%d").date()


def format_dt_object(dt_obj, fmt_str):
    """return date time object in format specified."""
    return datetime.strftime(dt_obj, fmt_str)


def string_to_datetime(date_str, time_format):
    """Convert pre-checked string into datetime object."""
    datet_obj = datetime.strptime(date_str, time_format)

    return datet_obj


def get_relative_ndays_from_date(date_str):
    """
    Converts a given date string to a string representing the relative time from that date.

    Parameters:
    - date_str (str): A string representing a date in any valid format.

    Returns:
    - str: A string representing the relative time from the given date string.

    Example:
    >>> format_datetime_to_relative('2022-01-01')
    '2 years ago'
    """
    parsed_date_time = arrow.get(date_str)
    return parsed_date_time.humanize()


####################################################################
### Datetime checks
###


def check_date_fmt(date_string=None):
    """Check that date matches format "YYYY-MM-DD"."""
    if re.match(REGEX_PATTERN, date_string):
        LOG.debug("date string verified")
        return True

    LOG.debug("Whoops! Incorrect date format")

    return False


####################################################################
### Datetime complex
###


def calc_ndays_fwd(ndays):
    """Returns a date string n days from today for use in
    an AWS schedule_deletion tag."""
    utc_time_now = datetime.utcnow()
    ndays_fwd = utc_time_now.date() + timedelta(days=ndays)
    ndays_fwd_str = format_dt_object(ndays_fwd, "%Y-%m-%d")

    return ndays_fwd_str


def calc_ndays_back_from_today(days_back):
    """Calculates the difference bewteen today and ndays back."""
    utc_time_now = datetime.utcnow().replace(tzinfo=tz.tzutc())
    ndays_back = utc_time_now - timedelta(days=days_back)
    return ndays_back


def calc_days_from_2dates_diff(prev_date):
    """Calculates the difference bewteen today and a previous date in days."""
    utc_time_now = datetime.utcnow().replace(tzinfo=tz.tzutc())
    # ndays_back = utc_time_now - timedelta(days=prev_date)
    ndays_back = utc_time_now - prev_date
    return ndays_back.days
