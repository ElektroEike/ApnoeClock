""" This file is part of ApnoeClock, a timer app for diver.

database is apnoeclock.db
tables:
=======
* CREATE TABLE IF NOT EXISTS
    maxtime(date DATE, time UNSIGNED INT, PRIMARY KEY(date))
"""

import sqlite3
from datetime import date, timedelta


def current_date():
    """ just today, but as a string """
    today_date = date.today()
    return format_date(today_date)


def format_date(a_date):
    """ create a string from a date object """
    return f'{a_date.year}-{a_date.month:02d}-{a_date.day:02d}'


def date_from_string(datestr:str):
    """ create a new date object from a string like 2022-01-17"""
    dlist = datestr.split('-')
    d = date(int(dlist[0]), int(dlist[1]), int(dlist[2]))
    return d


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


def does_table_exists(tablename):
    """ returns (B,N):
        B: if table with given name exists, then B == True, else False
        N: number of rows in the given table, if exists, else 0
    """
    sql = f'SELECT name FROM sqlite_master WHERE type = \'table\' and name = \'{tablename}\''
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    result = cursor.execute(sql)
    list = result.fetchall()
    if len(list) == 0:
        connection.close()
        return (False, 0)
    result = cursor.execute(f'SELECT * FROM \'{tablename}\'' )
    list = result.fetchall()
    connection.close()
    return (True, len(list))


def list_maxtimes():
    """ output table 'maxtime' """
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    for row in cursor.execute("SELECT * FROM maxtime"):
        print(row)
    connection.close()


def insert_maxtime_values():
    """ insert some values for the last 100 days
        This function is just for testing stuff - just to have some data in the db """
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    for i in range(100, 0, -1):
        v = (current_minus_days(i), 120 - i)
        cursor.execute("INSERT INTO maxtime VALUES(?, ?)", v)
    connection.commit()
    connection.close()


def get_last_n_days_from_maxtime_as_plot(n):
    """ get the data from the last n days until today from 'maxtime'
        data becomes transformed, so that we can use it for a plot (x, y)
    """
    day_back = current_minus_days(n)
    day_back_date = date_from_string(day_back)      # same as a date object
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    sql = f'SELECT date, time FROM maxtime WHERE date >= \'{day_back}\''
    result = cursor.execute(sql)
    list = result.fetchall()
    points = []
    for (d, t) in list:                             # get (date, time) list
        d_date = date_from_string(d)                # as date object
        days = (d_date - day_back_date).days        # get the difference as days
        points.append((days, t))                    # coordinates
    connection.close()
    return points


if __name__ == '__main__':
    print(does_table_exists('maxtime'))
