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
    def __init__(self, min_value, max_value, current_value, **kwargs):
        super(SliderWithLabel, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.slider = Slider(min=min_value, max=max_value, size_hint=(1.9, 1))
        self.add_widget(self.slider)
        self.label = Label(text="foo", size_hint=(0.1, 1))
        self.add_widget(self.label)
        # and now something completly different
        self.slider.bind(value=self.on_slider)
        self.set_value(current_value)
        self.on_slider(None, self.slider.value)

    def set_value(self, v):
        self.slider.value = v

    def on_slider(self, _a, value):
        v = int(value)
        self.label.text = f"{v} s"


class SettingsScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text="Einstellungen", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.layout.add_widget(Button(text='↩', font_name='DejaVuSans', font_size="20pt",
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                                      on_press=self.on_backbutton_press))

        self.gridlayout = GridLayout(size_hint=(0.9, 0.8), cols=2, # spacing=10,
                                     row_force_default=True, row_default_height=50,
                                     )
        self.layout.add_widget(self.gridlayout)
        self.gridlayout.add_widget(Label(text="Intervallatmung\nEinatmen:", size_hint_x=0.5))
        self.gridlayout.add_widget(SliderWithLabel(5, 15, 10, size_hint_x=1))

        # self.gridlayout.add_widget(ToggleButton(text="foo", size_hint_x=0.5))
        # self.gridlayout.add_widget(Label(text="Mehr!", size_hint_x=1))

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def on_enter(self, *args):
        pass

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, *_args):
        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)
