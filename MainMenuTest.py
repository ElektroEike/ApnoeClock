from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', size_hint=(.8, .8), pos_hint={'center_x':0.5, 'center_y': 0.5})
        self.add_widget(layout)
        layout.add_widget(Button(text="Maximalversuch", on_press=self.on_maxtime_press))
        layout.add_widget(Button(text="Intervallatmung"))
        layout.add_widget(Button(text="CO_2-Tabelle"))
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


class SquareBreatheScreen(Screen):
    def __init__(self, **kwargs):
        super(SquareBreatheScreen, self).__init__(**kwargs)
        self.add_widget(Label(text=self.name))


class WidgetApp(App):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(MenuScreen(name="MenuScreen"))
        manager.add_widget(MaxTimeScreen(name="MaxTimeScreen"))
        manager.current="MenuScreen"
        return manager


if __name__ == '__main__':
    WidgetApp().run()
