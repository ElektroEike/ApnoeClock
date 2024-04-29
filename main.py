""" This file is part of ApnoeClock, a timer application for apnoe divers."""
__version__ = "0.1"
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from maxtimescreen import MaxTimeScreen
from squarebreathscreen import SquareBreathScreen
from co2tablescreen import Co2TableScreen
from o2tablescreen import O2TableScreen
from analysescreen import AnalyseScreen
from settingsscreen import SettingsScreen
from infoscreen import InfoScreen
import dbtools


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', size_hint=(.8, .8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(layout)
        layout.add_widget(Button(text="Maximalversuch", on_press=self.on_maxtime_press))
        layout.add_widget(Button(text="Intervallatmung", on_press=self.on_interval_press))
        layout.add_widget(Button(text="CO_2-Tabelle", on_press=self.on_co2table_press))
        layout.add_widget(Button(text="O_2-Tabelle", on_press=self.on_o2table_press))
        layout.add_widget(Button(text="Auswertung", on_press=self.on_analyse_press))
        layout.add_widget(Button(text="Einstellung", on_press=self.on_settings_press))
        layout.add_widget(Button(text="Infos", on_press=self.on_infos_press))
        self.tt = Label(text="xx")

        layout.add_widget(self.tt)

        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

    def update_rect(self, _instance, _value):
        with self.canvas.before:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.pos, size=self.size)
        self.tt.text = str(self.size)


    def on_maxtime_press(self, _instance):
        self.manager.current = "MaxTimeScreen"

    def on_interval_press(self, _instance):
        self.manager.current = "SquareBreathScreen"

    def on_co2table_press(self, _instance):
        self.manager.current = "Co2TableScreen"

    def on_o2table_press(self, instance):
        max_breathholding_of_all_the_time = dbtools.get_maximum_breathholding_time()
        if max_breathholding_of_all_the_time >= 90:
            self.manager.current = "O2TableScreen"
        else:
            instance.text = "Nee, Maximalzeit zu kurz"

    def on_analyse_press(self, _instance):
        self.manager.current = "AnalyseScreen"

    def on_settings_press(self, _instance):
        self.manager.current = "SettingsScreen"

    def on_infos_press(self, _instance):
        self.manager.current = "InfoScreen"


class ApnoeClockApp(App):
    def build(self):
        dbtools.init_tables()       # uh, we need tables ;-)
        manager = ScreenManager()
        manager.add_widget(MenuScreen(name="MenuScreen"))
        manager.add_widget(MaxTimeScreen("MenuScreen", name="MaxTimeScreen"))
        manager.add_widget(SquareBreathScreen("MenuScreen", name="SquareBreathScreen"))
        manager.add_widget(Co2TableScreen("MenuScreen", name="Co2TableScreen"))
        manager.add_widget(O2TableScreen("MenuScreen", name="O2TableScreen"))
        manager.add_widget(AnalyseScreen("MenuScreen", name="AnalyseScreen"))
        manager.add_widget(SettingsScreen("MenuScreen", name="SettingsScreen"))
        manager.add_widget(InfoScreen("MenuScreen", name="InfoScreen"))
        manager.current = "MenuScreen"
        return manager


if __name__ == '__main__':
    #Config.set('graphics', 'width', '432')
    #Config.set('graphics', 'height', '768')
    ApnoeClockApp().run()
