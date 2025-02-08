import re
import time
from datetime import datetime, timedelta


def parse_time_range(time_text):
    """Parses time input and returns (start_timestamp, end_timestamp) in milliseconds, defaulting to today."""
    now = datetime.now()
    current_year = now.year
    today_str = now.strftime("%Y-%m-%d")  # "2025-02-08"

    def to_unix(dt):
        return int(time.mktime(dt.timetuple()) * 1000)  # Convert to milliseconds

    # Match: HH:MM-HH:MM  (defaults to today)
    if re.match(r"^\d{2}:\d{2}-\d{2}:\d{2}$", time_text):
        times = time_text.split("-")
        start_time = datetime.strptime(f"{today_str} {times[0]}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{today_str} {times[1]}", "%Y-%m-%d %H:%M")
        return to_unix(start_time), to_unix(end_time)

    # Match: HH:MM (defaults to current time)
    elif re.match(r"^\d{2}:\d{2}$", time_text):
        start_time = datetime.strptime(f"{today_str} {time_text}", "%Y-%m-%d %H:%M")
        end_time = now
        print(end_time)
        return to_unix(start_time), to_unix(end_time)

    # Match: MM-DD HH:MM-HH:MM  or  YYYY-MM-DD HH:MM-HH:MM
    elif re.match(r"^\d{1,4}-\d{2} \d{2}:\d{2}-\d{2}:\d{2}$", time_text):
        date_part, times = time_text.split(" ")
        times = times.split("-")

        if len(date_part) == 5:  # MM-DD case
            date_part = f"{current_year}-{date_part}"

        start_time = datetime.strptime(f"{date_part} {times[0]}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{date_part} {times[1]}", "%Y-%m-%d %H:%M")
        return to_unix(start_time), to_unix(end_time)

    # Match: MM-DD HH:MM  or  YYYY-MM-DD HH:MM (Single timestamp)
    elif re.match(r"^\d{1,4}-\d{2} \d{2}:\d{2}$", time_text):
        if len(time_text.split(" ")[0]) == 5:  # MM-DD case
            time_text = f"{current_year}-{time_text}"

        start_time = datetime.strptime(time_text, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{start_time.strftime("%Y-%m-%d")} 23:59", "%Y-%m-%d %H:%M")
        print(end_time)
        return to_unix(start_time), to_unix(end_time)

    # Match: MM-DD  or  YYYY-MM-DD (Full day)
    elif re.match(r"^\d{1,4}-\d{2}$", time_text):
        if len(time_text) == 5:  # MM-DD case
            time_text = f"{current_year}-{time_text}"

        start_time = datetime.strptime(time_text, "%Y-%m-%d")
        end_time = start_time + timedelta(days=1)  # Full day
        return to_unix(start_time), to_unix(end_time)

    return None  # Invalid format
