from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from stateclock import StateClock


class SquareBreathScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(SquareBreathScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        # states: StateNum: (LabelText, DurationOfState, NextStateNum), ...
        # NextStateNum==-1 ==> end
        self.states = {0: ("Prepare...", 5, 1),
                       1: ("Inhale", 4, 2),
                       2: ("Hold Breath", 3, 3),
                       3: ("Exhalte", 5, 4),
                       4: ("Hold Breath", 4, 1)}

        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text="Square Breath", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.label_todo = Label(text="ToDo", font_size="30pt",  size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.56})
        self.layout.add_widget(self.label_todo)
        self.label_time = Label(text="00:00", font_size="30pt", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.48})
        self.layout.add_widget(self.label_time)
        self.layout.add_widget(Button(text="Start/Stop", size_hint=(0.98, 0.5), pos_hint={'x': 0.01, 'y': 0.01},
                               on_press=self.on_startstop_press))
        self.layout.add_widget(Button(text="back", size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                               on_press=self.on_backbutton_press))

        self.colors = []
        self.ellipses = []
        self.lines = []
        self.points = []        # filled and updated in update_rect()
        with self.canvas:
            for i in range(0, 4):
                self.colors.append(Color(0, 0, 1, .5, mode='rgba'))
                self.ellipses.append(Ellipse(size=(0, 0), size_hint=(None, None)))
                self.lines.append(Line(width=3))

        self.current_state_num = -2     # start after preparation

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.clock = StateClock(self.states, self.stateclock_reports)

    def on_enter(self, *args):
        self._reset()

    def on_leave(self, *args):
        self.clock.reset()
        self._reset_color()
        self._reset_lines()

    def stateclock_reports(self, reason, label, duration, time):
        self.label_todo.text = label
        if reason == StateClock.NEW_STATE:
            self.current_state_num = self.current_state_num + 1
            if self.current_state_num >= 0:
                self.current_state_num = self.current_state_num % 4
                self._set_color_from_state(self.current_state_num)
                self._set_lines_from_state(self.current_state_num, time/duration)
            self.label_time.text = '{:d} s'.format(round(duration))
        elif reason == StateClock.RUN_STATE:
            self.label_time.text = '{:d} s'.format(round(duration - time))
            if self.current_state_num >= 0:
                self._set_lines_from_state(self.current_state_num, time / duration)
        else:
            # "Finished" should not happen in this module
            pass

    def _reset_color(self):
        self.colors[0].rgba = (0, 0, 1, 0.5)
        self.colors[1].rgba = (0, 0, 1, 0.5)
        self.colors[2].rgba = (0, 0, 1, 0.5)
        self.colors[3].rgba = (0, 0, 1, 0.5)

    def _reset_lines(self):
        self.lines[0].points = self.points[0:4]
        self.lines[1].points = self.points[2:6]
        self.lines[2].points = self.points[4:8]
        self.lines[3].points = self.points[6:10]

    def _reset(self):
        """ reset everything t start values """
        self.current_state_num = -2
        self._reset_lines()
        self._reset_color()
        self.clock.init()

    def _set_color_from_state(self, statenum):
        self._reset_color()
        for i in range(statenum + 1):
            self.colors[i].rgba = (0, 1, 0, 1)

    def _set_lines_from_state(self, statenum, percent):
        """ this shows a moving line. Line length is calculated by the
            percentage of the maximum length. """
        self._reset_lines()
        # calculate the length of the line
        startindex = statenum * 2
        points = self.points[startindex:startindex + 4]
        x_length = (points[2] - points[0]) * percent
        y_length = (points[3] - points[1]) * percent
        new_points = [points[0], points[1], points[0] + x_length, points[1] + y_length]
        self.lines[statenum].points = new_points

    def on_startstop_press(self, _instance):
        running = self.clock.start_stop_clock()
        if not running:
            # if we stop, we reset everything just in case user wants to start again
            self._reset()

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, *_args):
        with self.layout.canvas.before:
            # Background
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)

        width, height = self.size
        min_size = min(width, height)
        eli_size = min_size / 20
        x0 = width / 10
        x1 = 9 * width / 10 - eli_size
        y0 = 8.3 * height / 10
        y1 = 5.3 * height / 10
        # position of circles
        self.ellipses[0].size = (eli_size, eli_size)
        self.ellipses[0].pos = (x0, y0)
        self.ellipses[1].size = (eli_size, eli_size)
        self.ellipses[1].pos = (x1, y0)
        self.ellipses[2].size = (eli_size, eli_size)
        self.ellipses[2].pos = (x1, y1)
        self.ellipses[3].size = (eli_size, eli_size)
        self.ellipses[3].pos = (x0, y1)
        # draw rect connecting all points
        self.points = [x0 + eli_size, y0, x1, y0, x1, y1 + eli_size, x0 + eli_size, y1 + eli_size, x0 + eli_size, y0]
        self._reset_lines()
