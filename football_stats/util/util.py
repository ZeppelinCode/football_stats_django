from datetime import datetime
from typing import Optional
from pytz import timezone


def western_europe_time_to_utc(dt: Optional[str]) -> Optional[datetime]:
    if dt is None:
        return dt

    datetime_obj = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f")
    datetime_obj_as_western_europe_time = datetime_obj.replace(
        tzinfo=timezone('Europe/Berlin'))
    return datetime_obj_as_western_europe_time.astimezone(
        timezone('UTC'))
