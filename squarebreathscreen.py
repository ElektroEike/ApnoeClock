from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

import dbtools
from stateclock import StateClock


class SquareBreathScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(SquareBreathScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        # states: StateNum: (LabelText, DurationOfState, NextStateNum), ...
        # NextStateNum==-1 ==> end
        self.states = {0: ("Prepare...", 3, 1),
                       1: ("Inhale", 4, 2),
                       2: ("Hold Breath", 5, 3),
                       3: ("Exhale", 6, 4),
                       4: ("Hold Breath", 7, 1)}

        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text="Square Breath", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.label_todo = Label(text="ToDo", font_size="30pt", size_hint=(0.9, 0.1), pos_hint={'x': 0.05, 'y': 0.8})
        self.layout.add_widget(self.label_todo)
        self.label_time = Label(text="00:00", font_size="30pt", size_hint=(0.9, 0.1), pos_hint={'x': 0.05, 'y': 0.72})
        self.layout.add_widget(self.label_time)
        self.action_button = Button(text="Start/Stop", size_hint=(0.98, 0.5), pos_hint={'x': 0.01, 'y': 0.01},
                                    on_press=self.on_startstop_press)
        self.layout.add_widget(self.action_button)
        self.layout.add_widget(Button(text='↩', font_name='DejaVuSans', font_size="20pt",
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                                      on_press=self.on_backbutton_press))
        # show, what the user has to do in the states
        self.label_todo_states = []
        text = f'{self.states[1][0]} {self.states[1][1]} s'
        label_todo_state1 = Label(text=text, font_size="14pt",
                                  size_hint=(0.48, 0.05), pos_hint={'x': 0.01, 'y': 0.64})
        self.layout.add_widget(label_todo_state1)
        self.label_todo_states.append(label_todo_state1)

        text = f'{self.states[2][0]} {self.states[2][1]} s'
        label_todo_state2 = Label(text=text, font_size="14pt",
                                  size_hint=(0.48, 0.05), pos_hint={'x': 0.5, 'y': 0.64})
        self.layout.add_widget(label_todo_state2)
        self.label_todo_states.append(label_todo_state2)

        text = f'{self.states[3][0]} {self.states[3][1]} s'
        label_todo_state3 = Label(text=text, font_size="14pt",
                                  size_hint=(0.48, 0.05), pos_hint={'x': 0.5, 'y': 0.55})
        self.layout.add_widget(label_todo_state3)
        self.label_todo_states.append(label_todo_state3)

        text = f'{self.states[4][0]} {self.states[4][1]} s'
        label_todo_state4 = Label(text=text, font_size="14pt",
                                  size_hint=(0.48, 0.05), pos_hint={'x': 0.01, 'y': 0.55})
        self.layout.add_widget(label_todo_state4)
        self.label_todo_states.append(label_todo_state4)

        # draw lines arround border as a progress bar duing exercise
        self.colors = []
        self.lines = []
        self.points = []        # filled and updated in update_rect()
        with self.canvas:
            for i in range(0, 4):
                self.colors.append(Color(0, 0, 1, .5, mode='rgba'))
                self.lines.append(Line(width=2))

        # draw a rect arround label_todo_next
        self.labelrects = []
        with self.label_todo_states[0].canvas.before:  # seem to work for all labels. don't know why but it's ok.
            for i in range(0, 4):
                Color(0.6, 0.6, 0.6)
                self.labelrects.append(Rectangle())

        self.current_state_num = -2                     # start after preparation
        self.we_can_write_a_trainingsrecord = False     # only _after_ exercise!

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.clock = StateClock(self.states, self.stateclock_reports)

    def on_enter(self, *args):
        self._prepare()

    def on_leave(self, *args):
        """ if you leave and enter again, it looks ugly if colors jump arround. so we reset the colors here """
        self.clock.reset()
        self._reset_color()
        self._reset_lines()
        self._reset_labels()

    def stateclock_reports(self, reason, label, duration, time):
        self.label_todo.text = label
        if reason == StateClock.NEW_STATE:
            self.current_state_num = self.current_state_num + 1
            if self.current_state_num >= 0:
                if self.current_state_num == 4:     # this must go _before_ the modulo op
                    # allow a trainingsrecord after one turn
                    self.we_can_write_a_trainingsrecord = True
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
        self.colors[0].rgb = (0.5, 0.5, 0.6)
        self.colors[1].rgb = (0.5, 0.5, 0.6)
        self.colors[2].rgb = (0.5, 0.5, 0.6)
        self.colors[3].rgb = (0.5, 0.5, 0.6)

    def _reset_lines(self):
        self.lines[0].points = self.points[0:4]
        self.lines[1].points = self.points[2:6]
        self.lines[2].points = self.points[4:8]
        self.lines[3].points = self.points[6:10]

    def _reset_labels(self):
        for i in range(0, 4):
            self.label_todo_states[i].bold = False
            self.label_todo_states[i].color = (1, 1, 1)

    def _prepare(self):
        """ for next start """
        self.current_state_num = -2
        self.we_can_write_a_trainingsrecord = False
        self._reset_lines()
        self._reset_color()
        self._reset_labels()
        self.action_button.text = "Start"
        self.clock.init()

    def _set_color_from_state(self, statenum):
        """ depending on the state, we set the color of each line
            note: this is not the real state num, as "prepare state"
                does not count """
        self._reset_color()
        self._reset_labels()
        for i in range(statenum + 1):
            self.colors[i].rgba = (0, 1, 0, 1)
        self.label_todo_states[statenum].bold = True
        self.label_todo_states[statenum].color = (0, 1, 0, 0.5)

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
        if running:
            self.action_button.text = "Stop"
        else:
            # if we stop, we reset everything just in case user wants to start again
            # write a trainingsrecord
            if self.we_can_write_a_trainingsrecord:
                dbtools.insert_training(dbtools.Exercise.SquareBreath)
            self._prepare()

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, *_args):
        with self.layout.canvas.before:
            # Background
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)

        # draw lines along the border
        width, height = self.size
        w2 = width - 1
        h2 = height - 1
        # draw rect connecting all points
        self.points = [1, h2, w2, h2, w2, 0, 1, 0, 1, h2]
        self._reset_lines()

        for i in range(0, 4):
            x = self.label_todo_states[i].x
            y = self.label_todo_states[i].y
            size = self.label_todo_states[i].size
            self.labelrects[i].pos = (x, y)
            self.labelrects[i].size = size
