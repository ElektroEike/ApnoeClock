from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, Line
from stateclock import StateClock


class SquareBreath(FloatLayout):
    def __init__(self, **kwargs):
        super(SquareBreath, self).__init__(**kwargs)
        # states: StateNum: (LabelText, DurationOfState, NextStateNum), ...
        # NextStateNum==-1 ==> end
        self.states = {0: ("Prepare...", 5, 1),
                       1: ("Breathe in", 4, 2),
                       2: ("Hold Breath", 3, 3),
                       3: ("Breathe out...", 5, 4),
                       4: ("Hold Breath", 4, 1)}

        self.add_widget(Label(text="Square Breath", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.label_todo = Label(text="ToDo", font_size="30pt",  size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.55})
        self.add_widget(self.label_todo)
        self.label_time = Label(text="00:00", font_size="30pt", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.45})
        self.add_widget(self.label_time)
        self.add_widget(Button(text="Start/Stop", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.05},
                               on_press=self.on_startstop_press))
        self.add_widget(Button(text="back", size_hint=(0.1, 0.1), pos_hint={'x': 0.05, 'y': 0.9},
                               on_press=self.on_backbutton_press))

        self.colors = []
        self.ellipses = []
        self.lines = []
        self.points = []        # filled and updated in update_rect()
        with self.canvas:
            for i in range(0, 4):
                self.colors.append(Color(0, 0, 1, .5, mode='rgba'))
                self.ellipses.append(Ellipse(size=(0, 0), size_hint=(None, None)))
                self.lines.append(Line())

        self.current_state_num = -2     # start after preparation

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.clock = StateClock(self.states, self.stateclock_reports)

    def stateclock_reports(self, reason, label, duration, time):
        self.label_todo.text = label
        if reason == StateClock.NEW_STATE:
            self.current_state_num = self.current_state_num + 1
            if self.current_state_num >= 0:
                self.current_state_num = self.current_state_num % 4
                self._set_color_from_state(self.current_state_num)
            self.label_time.text = '{:d} s'.format(round(duration))
        elif reason == StateClock.RUN_STATE:
            self.label_time.text = '{:d} s'.format(round(duration - time))
        else:
            # "Finished" should not happen in this module
            pass

    def _set_color_from_state(self, statenum ):
        self.colors[0].rgba = (0, 0, 1, 0.5)
        self.colors[1].rgba = (0, 0, 1, 0.5)
        self.colors[2].rgba = (0, 0, 1, 0.5)
        self.colors[3].rgba = (0, 0, 1, 0.5)
        for i in range(statenum + 1):
            self.colors[i].rgba = (0, 1, 0, 1)

    def on_startstop_press(self, _instance):
        self.clock.start_stop_clock()

    def on_backbutton_press(self, _instance):
        pass

    def update_rect(self, *_args):
        width, height = self.size
        min_size = min(width, height)

        eli_size = min_size / 20
        eli_size_half = eli_size / 2
        x0 = width / 10
        x1 = 9 * width / 10 - eli_size
        y0 = 8 * height / 10
        y1 = 5 * height / 10
        # position of circles
        self.ellipses[0].size = (eli_size, eli_size)
        self.ellipses[0].pos = (x0, y0)
        self.ellipses[1].size = (eli_size, eli_size)
        self.ellipses[1].pos = (x1, y0)
        self.ellipses[2].size = (eli_size, eli_size)
        self.ellipses[2].pos = (x0, y1)
        self.ellipses[3].size = (eli_size, eli_size)
        self.ellipses[3].pos = (x1, y1)
        # draw rect connecting all points
        self.points= [x0+eli_size_half, y0+eli_size_half,
                      x1+eli_size_half, y0+eli_size_half,
                      x1+eli_size_half, y1+eli_size_half,
                      x0+eli_size_half, y1+eli_size_half,
                      x0+eli_size_half, y0+eli_size_half]
        self.lines[0].points = self.points[0:4]
        self.lines[1].points = self.points[2:6]
        self.lines[2].points = self.points[4:8]
        self.lines[3].points = self.points[6:10]


class WidgetApp(App):
    def build(self):
        return SquareBreath()


if __name__ == '__main__':
    WidgetApp().run()
