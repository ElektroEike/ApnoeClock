from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen


class MaxTimeScreen(Screen):
    def __init__(self, **kwargs):
        super(MaxTimeScreen, self).__init__(**kwargs)
        self.layout = FloatLayout(size_hint=(1, 1))
        layout = self.layout    # FIXME!
        self.add_widget(layout)
        layout.add_widget(Label(text="Maximalversuch", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.timer_label = Label(text="00:00", font_size="30pt",  size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.6})
        layout.add_widget(self.timer_label)
        layout.add_widget(Button(text="Start/Stop", size_hint=(0.9, 0.5), pos_hint={'x': 0.05, 'y': 0.1}))
        layout.add_widget(Button(text="back", size_hint=(0.1, 0.1), pos_hint={'x': 0.05, 'y': 0.9},
                                 on_press=self.on_backbutton_press))
        layout.bind(size=self.update_rect)

    def on_backbutton_press(self, _instance):
        self.manager.current = "MenuScreen"

    def update_rect(self, _instance, _value):
        with self.layout.canvas.before:
            Color(1, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)
            print("update", self.layout.pos, self.layout.size)

