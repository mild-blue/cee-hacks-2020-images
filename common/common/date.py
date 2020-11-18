import datetime
import re

from dateutil.parser import parse
from dateutil.tz import tzoffset
from dateutil.utils import default_tzinfo

_DEFAULT_TZ = tzoffset("UTC", 0)


def format_datetime_for_file(date: datetime.datetime) -> str:
    """
    Formats datetime to nicer format
    :param date: datetime
    :return: str
    """
    iso_date = date.replace(microsecond=0).isoformat()
    parts = iso_date.split(" ")
    if len(parts) == 1:
        parts = iso_date.split("T")
    begin = ":".join(parts[:-1])
    end = parts[-1]
    merged = begin + "T" + end.replace("-", "m").replace("+", "p")
    return merged.replace(":", "-").replace(".", "-")


def format_timestamp_for_file(timestamp: float) -> str:
    """
    Formats datetime to nicer format.
    :param timestamp: float
    :return: str
    """
    return format_datetime_for_file(timestamp_to_date(timestamp))


def get_utc() -> datetime.datetime:
    """
    Gets datetime in UTC.
    :return: datetime
    """
    return datetime.datetime.now(datetime.timezone.utc)


def get_local_datetime() -> datetime.datetime:
    """
    Gets local datetime
    :return: datetime
    """
    return datetime.datetime.now()


def timestamp_to_date(timestamp: float) -> datetime.datetime:
    """
    Transform timestamp to datetime in UTC.
    :param timestamp: float value
    :return: datetime in UTC
    """
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)


def iso_to_date(date: str) -> datetime.datetime:
    """
    Format string date in ISO 8601 to datetime.
    :param date: ISO date
    :return: datetime
    """
    return default_tzinfo(parse(date), _DEFAULT_TZ)


def parse_file_name_to_datetime(filename: str) -> datetime.datetime:
    """
    Parses date from filename to datetime
    Example: 2020-02-07T11-04-21-00-00
    :param filename:
    :return:
    """
    match = re.search(
        "(\\d{4}-\\d{2}-\\d{2}T)(\\d{2})-(\\d{2})-(\\d{2})([pm])(\\d{2})-(\\d{2})",
        filename
    )

    if not match:
        raise Exception(f"Could not parse {filename} to datetime.")

    return iso_to_date(
        f"{match.group(1)}{match.group(2)}:{match.group(3)}:{match.group(4)}"
        f"{'+' if match.group(5) == 'p' else 'm'}{match.group(6)}:{match.group(7)}")
