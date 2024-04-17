""" This file is part of ApnoeClock, a timer application for apnoe divers."""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from maxtimescreen import MaxTimeScreen
from squarebreathscreen import SquareBreathScreen
from co2tablescreen import Co2TableScreen


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', size_hint=(.8, .8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(layout)
        layout.add_widget(Button(text="Maximalversuch", on_press=self.on_maxtime_press))
        layout.add_widget(Button(text="Intervallatmung", on_press=self.on_interval_press))
        layout.add_widget(Button(text="CO_2-Tabelle", on_press=self.on_co2table_press))
        layout.add_widget(Button(text="O_2-Tabelle"))
        layout.add_widget(Button(text="Auswertung"))
        layout.add_widget(Button(text="Einstellung"))
        layout.add_widget(Button(text="About"))
        self.bind(size=self.update_rect)

    def update_rect(self, _instance, _value):
        with self.canvas.before:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.pos, size=self.size)

    def on_maxtime_press(self, _instance):
        self.manager.current = "MaxTimeScreen"

    def on_interval_press(self, _instance):
        self.manager.current = "SquareBreathScreen"

    def on_co2table_press(self, _instance):
        self.manager.current = "Co2TableScreen"


class ApnoeClockApp(App):
    def build(self):
        connection = sqlite3.connect("apnoeclock.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS maxtime(date DATE, time UNSIGNED INT)")
        connection.commit()
        connection.close()
        manager = ScreenManager()
        manager.add_widget(MenuScreen(name="MenuScreen"))
        manager.add_widget(MaxTimeScreen("MenuScreen", name="MaxTimeScreen"))
        manager.add_widget(SquareBreathScreen("MenuScreen", name="SquareBreathScreen"))
        manager.add_widget(Co2TableScreen("MenuScreen", name="Co2TableScreen"))
        manager.current = "MenuScreen"
        return manager


if __name__ == '__main__':
    ApnoeClockApp().run()
