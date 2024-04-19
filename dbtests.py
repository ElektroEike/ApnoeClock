import sqlite3
from datetime import date, timedelta
"""

database is apnoeclock.db
tables:
=======
CREATE TABLE IF NOT EXISTS 
maxtime(date DATE, time UNSIGNED INT, PRIMARY KEY(date))

"""


def current_date():
    today_date = date.today()
    return format_date(today_date)


def format_date(a_date):
    return f'{a_date.year}-{a_date.month:02d}-{a_date.day:02d}'


def current_minus_days(number_of_days):
    """ returns a date minus given number of days """
    today_date = date.today()
    delta = timedelta(days=number_of_days)
    d = today_date - delta
    return format_date(d)


def current_plus_days(number_of_days):
    """ returns a date plus given number of days """
    today_date = date.today()
    delta = timedelta(days=number_of_days)
    d = today_date + delta
    return format_date(d)


def list_maxtimes():
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    for row in cursor.execute("SELECT * FROM maxtime"):
        print(row)
    connection.close()

def insert_maxtime_values():
    """insert some values for the last 100 days """
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    for i in range(100, 0, -1):
        v = (current_minus_days(i), 120 - i)
        cursor.execute("INSERT INTO maxtime VALUES(?, ?)", v)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    # insert_maxtime_values()
    list_maxtimes()