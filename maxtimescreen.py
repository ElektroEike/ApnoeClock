from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import math
import sqlite3
from datetime import date


class MaxTimeScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(MaxTimeScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        self.clock = None
        self.clock_is_running = False
        self.elapsed_time = 0
        self.max_breathholding_of_all_the_time = 0
        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text="Maximalversuch", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.timer_label = Label(text="00:00", font_size="30pt",  size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.6})
        self.layout.add_widget(self.timer_label)
        self.action_button = Button(text="Start", size_hint=(0.98, 0.5), pos_hint={'x': 0.01, 'y': 0.01},
                                    on_press=self.on_actionbutton_press)
        self.layout.add_widget(self.action_button)
        self.layout.add_widget(Button(text='↩', font_name='DejaVuSans', font_size="20pt",
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                                      on_press=self.on_backbutton_press))
        self.layout.bind(size=self.update_rect)

    def on_enter(self, *args):
        self.elapsed_time = 0
        self.action_button.text = "Start"
        self.timer_label.text = "00:00"
        self._db_get_maxtime()

    def on_leave(self, *args):
        if self.clock_is_running:
            self.clock.cancel()
        self.clock_is_running = False

    def on_actionbutton_press(self, _instance):
        if self.clock_is_running:
            self.clock.cancel()
            self.clock_is_running = False
            self.action_button.text = "Start"
            self._db_insert_maxtime()
        else:
            self.elapsed_time = 0
            self.clock = Clock.schedule_interval(self.clock_callback, 0.1)
            self.clock_is_running = True
            self.action_button.text = "Stop"

    def clock_callback(self, tick):
        self.elapsed_time += tick
        time = math.trunc(self.elapsed_time)
        minutes = time // 60
        seconds = time % 60
        if minutes > 0:
            time_text = "{0}:{1:02d} min".format(minutes, seconds)
        else:
            time_text = "{0:d} s".format(seconds)
        self.timer_label.text = time_text

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, _instance, _value):
        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)

    def _db_get_maxtime(self):
        """ return the maximum breathholding time of all the times """
        connection = sqlite3.connect("apnoeclock.db")
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(time) FROM maxtime")
        connection.commit()
        row = cursor.fetchone()
        connection.close()
        self.max_breathholding_of_all_the_time = row[0]

    def _db_insert_maxtime(self):
        """Insert the today's max breathholding time into database
            10 s is the absolute minimum, we would accept. """
        if not self.clock_is_running and self.elapsed_time > 10:
            today_date = date.today()
            today = f'{today_date.year}-{today_date.month}-{today_date.day}'
            time = math.trunc(self.elapsed_time)
            connection = sqlite3.connect("apnoeclock.db")
            cursor = connection.cursor()
            # did we run today?
            cursor.execute(f"SELECT COUNT(*), time FROM maxtime WHERE date='{today}'")
            row = cursor.fetchone()
            run_today, todays_time = row[0] > 0, row[1]
            if run_today:
                # we were running today, so we write the maximum into database
                time = max(todays_time, time)
                insert_stmt = f"UPDATE maxtime SET time='{time}' WHERE date='{today}'"
            else:
                insert_stmt = f"INSERT INTO maxtime VALUES('{today}', '{time}')"
            cursor.execute(insert_stmt)
            connection.commit()
            connection.close()
