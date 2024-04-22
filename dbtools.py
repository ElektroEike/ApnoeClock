""" This file is part of ApnoeClock, a timer app for diver.

database is apnoeclock.db
tables:
=======
* CREATE TABLE IF NOT EXISTS
    maxtime(date DATE, time UNSIGNED INT, PRIMARY KEY(date))

- each try, a max value is stored. If user makes more attempts, than just the max is stored.

* CREATE TABLE IF NOT EXISTS trainingdays(date DATE,
        tmaxtime UNSIGNED INT, tco2table UNSIGNED INT, to2table UNSIGNED INT,
        PRIMARY KEY(date))
- saves a trainingrecord: for every day (with training), the value 0/1 is stored in the relevant column.

"""

import sqlite3
from datetime import date, timedelta
from enum import Enum


# Fields in trainingdays table
class Exercise(Enum):
    MaxTime = 1
    Co2Table = 2
    O2Table = 3


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
    names_list = result.fetchall()
    if len(names_list) == 0:
        connection.close()
        return False, 0
    result = cursor.execute(f'SELECT * FROM \'{tablename}\'' )
    content_list = result.fetchall()
    connection.close()
    return True, len(content_list)


def init_tables():
    """ create table maxtime and populate it with at least one element """
    sql1 = "CREATE TABLE IF NOT EXISTS maxtime(date DATE, time UNSIGNED INT, PRIMARY KEY(date))"
    sql2 = "SELECT COUNT(*) FROM maxtime"
    sql3 = "INSERT INTO maxtime VALUES('2000-01-02', '10')"
    sql4 = """CREATE TABLE IF NOT EXISTS trainingdays(date DATE, 
        tmaxtime UNSIGNED INT, tco2table UNSIGNED INT, to2table UNSIGNED INT, 
        PRIMARY KEY(date))"""
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    cursor.execute(sql1)
    cursor.execute(sql2)
    row = cursor.fetchone()
    if row[0] == 0:
        # insert a record
        cursor.execute(sql3)
    cursor.execute(sql4)
    connection.commit()
    connection.close()


def drop_tables():
    """ Drops all tables created for AbnoeClock. Just for testing purpose """
    sql1 = "DROP TABLE IF EXISTS maxtime"
    sql2 = "DROP TABLE IF EXISTS trainingdays"
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    cursor.execute(sql1)
    cursor.execute(sql2)
    connection.commit()
    connection.close()


def list_maxtimes():
    """ output table 'maxtime' """
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    for row in cursor.execute("SELECT * FROM maxtime"):
        print(row)
    connection.close()


def list_trainingdays():
    """ output table 'trainingdays' """
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    for row in cursor.execute("SELECT * FROM trainingdays"):
        print(row)
    connection.close()


def insert_maxtime_today(time_in_seconds):
    today = current_date()
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    # did we run today?
    cursor.execute(f"SELECT COUNT(*), time FROM maxtime WHERE date='{today}'")
    row = cursor.fetchone()
    run_today, todays_time = row[0] > 0, row[1]
    if run_today:
        # we were running today, so we write the maximum into database
        time = max(todays_time, time_in_seconds)
        insert_stmt = f"UPDATE maxtime SET time='{time}' WHERE date='{today}'"
    else:
        insert_stmt = f"INSERT INTO maxtime VALUES('{today}', '{time_in_seconds}')"
    cursor.execute(insert_stmt)
    connection.commit()
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
    day_back_date = date_from_string(day_back)      # same but as a date object
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    sql = f'SELECT date, time FROM maxtime WHERE date >= \'{day_back}\''
    result = cursor.execute(sql)
    maxtime_list = result.fetchall()
    points = []
    for (d, t) in maxtime_list:                     # get (date, time) list
        d_date = date_from_string(d)                # as date object
        days = (d_date - day_back_date).days        # get the difference as days
        points.append((days, t))                    # coordinates
    connection.close()
    return points


def insert_training(whichone : Exercise):
    """ today, we have done our exercises. Insert in database.
    Each field gets a "1", if we have done the specific exercise. """
    today = current_date()
    sql1 = f"SELECT date, tmaxtime, tco2table, to2table FROM trainingdays WHERE date = '{today}'"
    connection = sqlite3.connect("apnoeclock.db")
    cursor = connection.cursor()
    result = cursor.execute(sql1)
    traininglist = result.fetchone()
    if traininglist is None:
        maxt = 1 if whichone == Exercise.MaxTime else 0
        co2t = 1 if whichone == Exercise.Co2Table else 0
        o2ta = 1 if whichone == Exercise.O2Table else 0
        sql2 = f"INSERT INTO trainingdays VALUES('{today}', {maxt}, {co2t}, {o2ta})"
    else:
        maxt = 1 if whichone == Exercise.MaxTime else traininglist[1]
        co2t = 1 if whichone == Exercise.Co2Table else traininglist[2]
        o2ta = 1 if whichone == Exercise.O2Table else traininglist[3]
        sql2 = f"UPDATE trainingdays SET tmaxtime={maxt}, tco2table={co2t}, to2table={o2ta} WHERE date='{today}'"
    cursor.execute(sql2)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    drop_tables()
    init_tables()

