import calendar
from datetime import timedelta


def get_db_uri(user, password, host, db):
    return f"postgres://{user}:{password}@{host}:5432/{db}"


def get_weeks_in_month(year: int, month: int):
    """
    Get the start and end dates of each week in a given month.

    :param year: The year of the month.
    :param month: The month for which to get the weeks.
    :return: A list of tuples containing the start and end dates of each week.
    """
    weeks = []
    cal = calendar.Calendar()

    for week in cal.monthdatescalendar(year, month):
        week_start = week[0]
        week_end = week[-1] + timedelta(days=1)
        weeks.append((week_start, week_end))

    return weeks


if __name__ == "__main__":
    pass
