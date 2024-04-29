from kivy.uix.screenmanager import Screen


class InfoScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname

    def on_backbutton_press(self):
        self.manager.current = self.parent_screen_name

