from datetime import timedelta
from random import randint
from pathlib import Path


# return random week in each month between given dates
def random_week_in_month(begin_date, end_date):
    current_date = begin_date
    while current_date <= end_date:
        next_month = current_date.replace(day=28) + timedelta(days=4)
        last_day_of_month = next_month - timedelta(days=next_month.day)
        latest_start_date = last_day_of_month - timedelta(days=6)

        if latest_start_date < current_date:
            latest_start_date = current_date

        if latest_start_date > end_date:
            break

        week_start_date = current_date + timedelta(days=randint(0, (latest_start_date - current_date).days))
        week_end_date = week_start_date + timedelta(days=6)
        if week_end_date > end_date:
            week_end_date = end_date

        yield (week_start_date, week_end_date)

        current_date = last_day_of_month + timedelta(days=1)


# return tuple (montn, day) for each day between given dates
def get_month_day(begin_date, end_date):
    current = begin_date
    while current <= end_date:
        yield current.month, current.day
        current += timedelta(days=1)

# return weekly periods of random length (min_len, max_len) between given dates
def gen_week_periods(begin_date, end_date, min_len, max_len):
    periods = []
    current_start = begin_date
    seconds_in_day = 24 * 60 * 60
    while current_start < end_date:
        duration = timedelta(weeks=randint(min_len, max_len))
        current_end = current_start + duration
        periods.append((current_start, current_end))
        # offset between periods
        offset = timedelta(seconds=randint(seconds_in_day, seconds_in_day * 7))
        current_start = current_end + offset
        if current_end > end_date:
            break

    return [(start, end) for start, end in periods]


def get_path(dir_name):
    return Path(__file__).absolute().parent / dir_name

