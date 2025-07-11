from datetime import datetime
import re
from backend.settings import time_zone


def get_lecture_intervals(raw_date, raw_start, raw_end):
    start = datetime.combine(datetime.strptime(raw_date, "%Y-%m-%d"),
                             datetime.strptime(raw_start, "%H:%M").time(), tzinfo=time_zone)
    end = datetime.combine(datetime.strptime(raw_date, "%Y-%m-%d"),
                           datetime.strptime(raw_end, "%H:%M").time(), tzinfo=time_zone)
    return start, end


def validate_time(str_time):
    return re.search(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")


def validate_date(str_date, format='%Y-%m-%d'):
    try:
        datetime.strptime(str_date, format)
        return True
    except ValueError:
        return False