from datetime import datetime

from backend.settings import tz


def get_lecture_intervals(raw_date, raw_start, raw_end):
    start = datetime.combine(datetime.strptime(raw_date, "%Y-%m-%d"),
                             datetime.strptime(raw_start, "%H:%M").time(), tzinfo=tz)
    end = datetime.combine(datetime.strptime(raw_date, "%Y-%m-%d"),
                           datetime.strptime(raw_end, "%H:%M").time(), tzinfo=tz)
    return start, end