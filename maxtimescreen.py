from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import math
import dbtools


class MaxTimeScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(MaxTimeScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        self.clock = None
        self.clock_is_running = False
        self.elapsed_time = 0
        self.prepare_user = False
        self.prepare_clock = None
        self.prepare_clock_is_running = False

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

        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)

        self.layout.bind(size=self.update_rect)

    def on_enter(self, *args):
        valid, value = dbtools.get_configvalue('maxtime_prepare_time')
        if valid and value == 1:
            self.prepare_user = True
            self.prepare_clock = None
            self.prepare_clock_is_running = False
            self.action_button.text = "Prepare"
        else:
            self.action_button.text = "Start"
        self.elapsed_time = 0
        self.timer_label.text = "00:00"
        self.timer_label.color = [1, 1, 1, 1]
        self.max_breathholding_of_all_the_time = dbtools.get_maximum_breathholding_time()

    def on_leave(self, *args):
        if self.clock_is_running:
            self._clock.cancel()
        if self.prepare_clock_is_running:
            self._prepare_clock_cancel()
        self.timer_label.color = [1, 1, 1, 1]

    def _clock_cancel(self):
        self.clock.cancel()
        self.clock_is_running = False

    def _prepare_clock_cancel(self):
        self.prepare_clock.cancel()
        self.prepare_clock_is_running = False

    def on_actionbutton_press(self, _instance):
        if self.clock_is_running:
            self._clock_cancel()
            self.action_button.text = "Prepare" if self.prepare_user else "Start"
            # Insert the today's max breathholding time into database
            # 10 s is the absolute minimum, we would accept. """
            if self.elapsed_time > 10:
                time = math.trunc(self.elapsed_time)
                dbtools.insert_maxtime_today(time)
                dbtools.insert_training(dbtools.Exercise.MaxTime)
        elif self.prepare_clock_is_running:
            self._prepare_clock_cancel()
            self.action_button.text = "Prepare"
        else:
            self.elapsed_time = 0
            self.timer_label.color = [1, 1, 1, 1]
            self.action_button.text = "Stop"
            if self.prepare_user:
                # run preparation
                self.elapsed_time = 5      # 60 seconds preparation time
                self.prepare_clock = Clock.schedule_interval(self.prepare_clock_callback, 0.1)
                self.prepare_clock_is_running = True
            else:
                # run normal clock
                self.clock = Clock.schedule_interval(self.clock_callback, 0.1)
                self.clock_is_running = True

    def clock_callback(self, tick):
        self.elapsed_time += tick
        if self.elapsed_time > self.max_breathholding_of_all_the_time:
            self.timer_label.color = [0, 1, 0, 1]
        time = math.trunc(self.elapsed_time)
        minutes = time // 60
        seconds = time % 60
        if minutes > 0:
            time_text = "{0}:{1:02d} min".format(minutes, seconds)
        else:
            time_text = "{0:d} s".format(seconds)
        self.timer_label.text = time_text

    def prepare_clock_callback(self, tick):
        self.elapsed_time -= tick
        time = math.trunc(self.elapsed_time)
        time_text = f"prepare {time} s"
        self.timer_label.text = time_text
        if time <= 0:        # finished with preparation
            self._prepare_clock_cancel()
            self.elapsed_time = 0
            self.timer_label.text = "00 s"
            # run normal clock
            self.clock = Clock.schedule_interval(self.clock_callback, 0.1)
            self.clock_is_running = True

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, _instance, _value):
        self.background_rect.pos = self.layout.pos
        self.background_rect.size = self.layout.size
