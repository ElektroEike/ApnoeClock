""" This file is part of ApnoeClock, a timer application for apnoe divers."""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from maxtimescreen import MaxTimeScreen
from squarebreathscreen import SquareBreathScreen
from co2tablescreen import Co2TableScreen
from analysescreen import AnalyseScreen
from settingsscreen import SettingsScreen
import dbtools


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', size_hint=(.8, .8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(layout)
        layout.add_widget(Button(text="Maximalversuch", font_size="14pt", on_press=self.on_maxtime_press))
        layout.add_widget(Button(text="Intervallatmung", font_size="14pt", on_press=self.on_interval_press))
        layout.add_widget(Button(text="CO_2-Tabelle", font_size="14pt", on_press=self.on_co2table_press))
        layout.add_widget(Button(text="O_2-Tabelle", font_size="14pt", ))
        layout.add_widget(Button(text="Auswertung", font_size="14pt", on_press=self.on_analyse_press))
        layout.add_widget(Button(text="Einstellung", font_size="14pt", on_press=self.on_settings_press))
        layout.add_widget(Button(text="Über", font_size="14pt", ))
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

    def on_analyse_press(self, _instance):
        self.manager.current = "AnalyseScreen"

    def on_settings_press(self, _instance):
        self.manager.current = "SettingsScreen"


class ApnoeClockApp(App):
    def build(self):
        dbtools.init_tables()       # uh, we need tables ;-)
        manager = ScreenManager()
        manager.add_widget(MenuScreen(name="MenuScreen"))
        manager.add_widget(MaxTimeScreen("MenuScreen", name="MaxTimeScreen"))
        manager.add_widget(SquareBreathScreen("MenuScreen", name="SquareBreathScreen"))
        manager.add_widget(Co2TableScreen("MenuScreen", name="Co2TableScreen"))
        manager.add_widget(AnalyseScreen("MenuScreen", name="AnalyseScreen"))
        manager.add_widget(SettingsScreen("MenuScreen", name="SettingsScreen"))
        manager.current = "MenuScreen"
        return manager


if __name__ == '__main__':
    Config.set('graphics', 'width', '432')
    Config.set('graphics', 'height', '768')
    ApnoeClockApp().run()
