""" Settingsscreen is a module for ApneaClock - a timer application for apnea divers

    The configuration elements
    ==========================
    key : value
    'maxtime_prepare_time':
        0 (Default): no preparation at all. User prepares self, then starts by pressing start
        1: 1 minute prepare time, then we start
    'squarebreath_prepare_time':
        0 (Default): 10 seconds prepare time
        1: 1 minute prepare time, then the exercise starts
    'squarebreath_inhale_time':
        [value] (10 seconds is default): time to inhale and time to hold. time to exhale is 2 * value.
    'co2table_prepare_time':
        0 (Default): 10 seconds prepare time
        1: 1 minute prepare time
    'co2table_use_maxtime':
        0 (Default): use 'co2table_hold_time' to define the breath hold time.
        1: use 40% up to 50% of the maximum breathholding time as the hold time.
    co2table_hold_time:
        [value] (30 seconds is default): the breath holding time, if you select co2table_use_maxtime=0
        Please note, that whatever you select, the minimum breathholding time in CO2-Table is 30 seconds
    o2table_prepare_time:
        0 (Default): 10 seconds prepare time
        1: 1 minute prepare time
    For actual default values, see get_default_config() in this file
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
import dbtools


class SliderWithLabel(BoxLayout):
    def __init__(self, config_item_name, min_value, max_value, current_value, **kwargs):
        super(SliderWithLabel, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.config_item_name = config_item_name
        self.slider = Slider(min=min_value, max=max_value, size_hint=(0.9, 1))
        self.slider.value = current_value
        self.add_widget(self.slider)
        self.label = Label(text=f"{current_value} s", size_hint=(0.1, 1))
        self.add_widget(self.label)
        # and now something completly different
        self.slider.bind(value=self.on_slider)

    def on_slider(self, _a, value):
        v = int(value)
        self.label.text = f"{v} s"
        dbtools.set_configvalue(self.config_item_name, v)


class TogglebuttonWithLabel(BoxLayout):
    def __init__(self, config_item_name, current_value, text_normal, text_down, **kwargs):
        super(TogglebuttonWithLabel, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.config_item_name = config_item_name
        self.text_normal = text_normal
        self.text_down = text_down
        self.togglebutton = ToggleButton()
        self.add_widget(self.togglebutton)
        self.togglebutton.bind(state=self.on_toggle)
        self.togglebutton.state = 'normal' if current_value == 0 else 'down'
        self.set_text()

    def set_text(self):
        d = {'normal': self.text_normal, 'down': self.text_down}
        self.togglebutton.text = d[self.togglebutton.state]

    def on_toggle(self, _a, togglestate):
        d = {'normal': 0, 'down': 1}
        self.set_text()
        dbtools.set_configvalue(self.config_item_name, d[togglestate])


class SettingsScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        # overall layout
        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)
        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5)
            self.layout_rect = Rectangle()
        self.layout.add_widget(Label(text="Einstellungen", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.layout.add_widget(Button(text='↩', font_name='DejaVuSans', font_size="20pt",
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                                      on_press=self.on_backbutton_press))
        # grid layout for items to change
        self.gridlayout = GridLayout(size_hint=(0.98, 0.8), pos_hint={'x': 0.01, 'y': 0.01}, cols=2)
        self.layout.add_widget(self.gridlayout)
        with self.gridlayout.canvas.before:
            Color(0.4, 0.4, 0.4)
            self.grid_rect = Rectangle()

        self.current_config = {}
        self.init_current_config()

        # Config Items
        self.gridlayout.add_widget(Label(text="Maximalversuch\nVorbereitung?", size_hint_x=0.45, font_size="12dp"))
        self.gridlayout.add_widget(TogglebuttonWithLabel("maxtime_prepare_time",
                                                         self.current_config['maxtime_prepare_time'],
                                                         "Nein", "1 Minute"))

        self.gridlayout.add_widget(Label(text="Intervallatmung\nVorbereitungszeit", size_hint_x=0.45, font_size="12dp"))
        self.gridlayout.add_widget(TogglebuttonWithLabel("squarebreath_prepare_time",
                                                         self.current_config['squarebreath_prepare_time'],
                                                         "10 s", "1 Minute"))

        self.gridlayout.add_widget(Label(text="Intervallatmung\nEinatmen:", size_hint_x=0.45, font_size="12dp"))
        self.gridlayout.add_widget(SliderWithLabel("squarebreath_inhale_time",
                                                   5, 15,
                                                   self.current_config['squarebreath_inhale_time']))

        self.gridlayout.add_widget(Label(text="CO2-Tabelle\nVorbereitungszeit", size_hint_x=0.45, font_size="12dp"))
        self.gridlayout.add_widget(TogglebuttonWithLabel("co2table_prepare_time",
                                                         self.current_config['co2table_prepare_time'],
                                                         "10 s", "1 Minute"))

        self.gridlayout.add_widget(Label(text="CO2-Tabelle\nHaltezeit von\nMaxZeit ableiten?", size_hint_x=0.45,
                                         font_size="10dp"))
        self.gridlayout.add_widget(TogglebuttonWithLabel("co2table_use_maxtime",
                                                         self.current_config['co2table_use_maxtime'],
                                                         "Nein", "Ja (40-50%)"))

        self.gridlayout.add_widget(Label(text="CO2-Tabelle\nEigene Haltezeit", size_hint_x=0.45, font_size="12dp"))
        self.gridlayout.add_widget(SliderWithLabel("co2table_hold_time",
                                                   30, 120, self.current_config['co2table_hold_time']))

        self.gridlayout.add_widget(Label(text="O2-Tabelle\nVorbereitungszeit", size_hint_x=0.45, font_size="12dp"))
        self.gridlayout.add_widget(TogglebuttonWithLabel("o2table_prepare_time",
                                                         self.current_config['o2table_prepare_time'],
                                                         "10 s", "1 Minute"))

        # connect events to callbacks
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    @staticmethod
    def get_default_config() -> dict:
        """ sets default values for config items """
        config_dict = {
            'maxtime_prepare_time': 0,          # No prepare time
            'squarebreath_prepare_time': 0,     # 0 means : 10 seconds prepare time
            'squarebreath_inhale_time': 10,     # 10 seconds inhale, 20 seconds exhale
            'co2table_prepare_time': 0,         # 0 means: 10 seconds prepare time
            'co2table_use_maxtime': 0,          # 0: use value from co2table_hold_time, not from maximum holding time
            'co2table_hold_time': 30,           # 30 is the very minimum for CO2 table
            'o2table_prepare_time': 0           # 0 means 10 seconds prepare time
        }
        return config_dict

    def init_current_config(self):
        """ read config from database. If database does not provide a config item, we read
            ths from default items and write it to database. """
        self.current_config = self.get_default_config()     # our config
        stored_config = dbtools.get_full_config()           # config on database
        current_config_keys = self.current_config.keys()
        stored_config_keys = stored_config.keys()
        for key in current_config_keys:
            if key in stored_config_keys:
                # update our local config value with what we found in the database
                self.current_config[key] = stored_config[key]
            else:
                # key not found, database is not up to date
                # store the key in the database
                dbtools.set_configvalue(key, self.current_config[key])

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, *_args):
        self.layout_rect.pos = self.layout.pos
        self.layout_rect.size = self.layout.size
        self.grid_rect.pos = self.gridlayout.pos
        self.grid_rect.size = self.gridlayout.size
