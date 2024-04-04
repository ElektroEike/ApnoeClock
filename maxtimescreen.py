from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import math


class MaxTimeScreen(Screen):
    def __init__(self, **kwargs):
        super(MaxTimeScreen, self).__init__(**kwargs)
        self.clock = None
        self.clock_is_running = False
        self.elapsed_time = 0
        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text="Maximalversuch", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.timer_label = Label(text="00:00", font_size="30pt",  size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.6})
        self.layout.add_widget(self.timer_label)
        self.layout.add_widget(Button(text="Start/Stop", size_hint=(0.9, 0.5), pos_hint={'x': 0.05, 'y': 0.1},
                                      on_press=self.on_actionbutton_press))
        self.layout.add_widget(Button(text="back", size_hint=(0.1, 0.1), pos_hint={'x': 0.05, 'y': 0.9},
                                      on_press=self.on_backbutton_press))
        self.layout.bind(size=self.update_rect)

    def on_actionbutton_press(self, _instance):
        if self.clock_is_running:
            self.clock.cancel()
        else:
            self.elapsed_time = 50
            self.clock = Clock.schedule_interval(self.clock_callback, 0.1)
        self.clock_is_running = not self.clock_is_running

    def clock_callback(self, tick):
        self.elapsed_time += tick
        minutes = math.trunc(self.elapsed_time // 60)
        seconds = math.trunc(self.elapsed_time % 60)
        if minutes > 0:
            time_text = "{0}:{1:02d} min".format(minutes, seconds)
        else:
            time_text = "{0:d} s".format(seconds)
        self.timer_label.text = time_text
        print(tick, self.elapsed_time, time_text)

    def on_backbutton_press(self, _instance):
        self.manager.current = "MenuScreen"

    def update_rect(self, _instance, _value):
        with self.layout.canvas.before:
            Color(1, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)
            print("update", self.layout.pos, self.layout.size)
