import calendar
from datetime import timedelta, date


def get_db_uri(user, password, host, db):
    return f"postgres://{user}:{password}@{host}:5432/{db}"


def get_weeks_in_month(year: int, month: int):
    """
    Get the start and end dates of each week in a given month.

    :param year: The year of the month.
    :param month: The month for which to get the weeks.
    :return: A list of tuples containing the start and end dates of each week.
    """
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")
    if not (1 <= year <= 9999):
        raise ValueError(f"Invalid year: {year}. Year must be between 1 and 9999.")
    weeks = []
    cal = calendar.Calendar()
    for week in cal.monthdatescalendar(year, month):
        week_start = week[0]
        week_end = week[-1] + timedelta(days=1)

        # Ensure the week_start and week_end are within the specified month
        if week_start.month != month:
            week_start = date(year, month, 1)
        if week_end.month != month:
            last_day_of_month = calendar.monthrange(year, month)[1]
            week_end = date(year, month, last_day_of_month) + timedelta(days=1)
        weeks.append((week_start, week_end))

    return weeks


if __name__ == "__main__":
    pass
