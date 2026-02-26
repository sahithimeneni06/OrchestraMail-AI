from datetime import timedelta
import dateparser
import re

def format_date_range(date_dict):
    start = date_dict["start_date"].strftime("%B %d, %Y")
    end = date_dict["end_date"].strftime("%B %d, %Y")

    if start == end:
        return start
    return f"{start} to {end}"

def extract_dates(text, base_date=None):

    if base_date is None:
        base_date = dateparser.parse("today")

    text = text.lower()

    # duration
    duration_match = re.search(r'(\d+)\s*(day|days|week|weeks)', text)
    duration_days = None

    if duration_match:
        value = int(duration_match.group(1))
        unit = duration_match.group(2)

        duration_days = value * 7 if "week" in unit else value

    # explicit range
    range_match = re.search(r'from (.+?) to (.+)', text)

    if range_match:

        start = dateparser.parse(range_match.group(1),
                                 settings={"PREFER_DATES_FROM": "future"})

        end = dateparser.parse(range_match.group(2),
                               settings={"PREFER_DATES_FROM": "future"})

        if start and end:
            return {
                "start_date": start.date(),
                "end_date": end.date(),
                "total_days": (end.date() - start.date()).days + 1
            }

    # single date
    start_date = dateparser.parse(
        text,
        settings={"PREFER_DATES_FROM": "future"}
    )

    if start_date and duration_days:
        end_date = start_date + timedelta(days=duration_days - 1)

        return {
            "start_date": start_date.date(),
            "end_date": end_date.date(),
            "total_days": duration_days
        }

    if start_date:
        return {
            "start_date": start_date.date(),
            "end_date": start_date.date(),
            "total_days": 1
        }

    return None