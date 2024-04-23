""" co2table is a module for ApneaClock - a timer application for apnea divers
    CO_2 tables help you to manage increasing CO_2 levels in your body.
    Training:
    Prepare - Apnea 30 s - Breathe a time, Apnea 30 s, Breathe a shorter time and so on. 8 rounds.
"""
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from stateclock import StateClock
import dbtools


class Co2TableScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(Co2TableScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        # 8 turns of apnea and breathing
        self.states = {0: ("Prepare...", 3, 1),
                       1: ("Hold Breath", 1, 2), 2: ("Breathe...", 1, 3),
                       3: ("Hold Breath", 1, 4), 4: ("Breathe...", 2, 5),
                       5: ("Hold Breath", 1, 6), 6: ("Breathe...", 1, 7),
                       7: ("Hold Breath", 1, 8), 8: ("Breathe...", 1, 9),
                       9: ("Hold Breath", 1, 10), 10: ("Breathe...", 1, 11),
                       11: ("Hold Breath", 1, 12), 12: ("Breathe...", 1, 13),
                       13: ("Hold Breath", 1, 14), 14: ("Breathe...", 1, 15),
                       15: ("Hold Breath", 3, -1)}

        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)
        self.layout.add_widget(Label(text="CO2 Table", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.label_todo = Label(text="ToDo", font_size="30pt", size_hint=(0.9, 0.1), pos_hint={'x': 0.05, 'y': 0.8})
        self.layout.add_widget(self.label_todo)
        self.label_time = Label(text="00:00", font_size="30pt", size_hint=(0.9, 0.1), pos_hint={'x': 0.05, 'y': 0.71})
        self.layout.add_widget(self.label_time)
        self.action_button = Button(text="Start", size_hint=(0.98, 0.5), pos_hint={'x': 0.01, 'y': 0.01},
                                    on_press=self.on_startstop_press)
        self.layout.add_widget(self.action_button)
        self.layout.add_widget(Button(text='↩', font_name='DejaVuSans', font_size="20pt",
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                                      on_press=self.on_backbutton_press))
        # show, what the user has to do next
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

        # Ellipses showing the number of rounds
        self.ellipse_colors = []
        self.ellipses = []
        with self.canvas:
            for i in range(0, 8):
                self.ellipse_colors.append(Color(0.6, 0.6, 0.6))
                self.ellipses.append(Ellipse(size=(10, 10), size_hint=(None, None)))

        # draw a rect arround label_todo_next
        self.labelrects = []
        with self.label_todo_states[0].canvas.before:  # seem to work for all labels. don't know why but it's ok.
            for i in range(0, 2):
                Color(0.6, 0.6, 0.6)
                self.labelrects.append(Rectangle())

        self.current_state_num = -2                     # we start after preparation

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.clock = StateClock(self.states, self.stateclock_reports)

    def on_enter(self, *args):
        self._prepare()

    def on_leave(self, *args):
        self.clock.reset()
        self._reset_color()
        self._reset_labels()

    def stateclock_reports(self, reason, label, duration, time):
        self.label_todo.text = label
        if reason == StateClock.NEW_STATE:
            self.label_time.text = '{:d} s'.format(round(duration))
            self.current_state_num += 1
            if self.current_state_num >= 0:
                index = self.current_state_num // 2
                self._set_labels_from_state(self.current_state_num + 1)
                if self.current_state_num % 2 == 0:         # apnea
                    self.ellipse_colors[index].rgb = [1, 0, 0]
                else:                                       # breathe
                    self.ellipse_colors[index].rgb = [0, 1, 0]
        elif reason == StateClock.RUN_STATE:
            self.label_time.text = '{:d} s'.format(round(duration - time))
        else:
            # finished -> draw the last Elipse
            self.ellipse_colors[self.current_state_num // 2].rgb = [0, 1, 0]
            self.label_todo.text = "Congratulation"
            # write a trainingsrecord
            dbtools.insert_training(dbtools.Exercise.Co2Table)
            Clock.schedule_once(self._prepare, 1)

    def _reset_color(self):
        for i in range(0, 8):
            self.ellipse_colors[i].rgb = [0.6, 0.6, 0.6]

    def _reset_labels(self):
        for i in range(0, 2):
            self.label_todo_states[i].bold = False
            self.label_todo_states[i].color = (1, 1, 1)

    def _prepare(self, _dt=None):
        """ prepare for next start """
        self.current_state_num = -2
        self.action_button.text = "Start"
        self._reset_color()
        self._reset_labels()
        self.label_todo_states[0].text = f'{self.states[1][0]} {self.states[1][1]} s'
        self.label_todo_states[1].text = f'{self.states[2][0]} {self.states[2][1]} s'
        self.clock.init()

    def _set_labels_from_state(self, statenum):
        """ statenum is a state from 1...N """
        self._reset_labels()
        max_states = len(self.states) - 1
        next_statenum = statenum + 1
        if next_statenum > max_states:
            text = "finished"
        else:
            text = f'{self.states[next_statenum][0]} {self.states[next_statenum][1]} s'
        if statenum % 2 == 1:
            self.label_todo_states[0].bold = True
            self.label_todo_states[0].color = (0, 1, 0)
            self.label_todo_states[1].text = text
        else:
            self.label_todo_states[1].bold = True
            self.label_todo_states[1].color = (0, 1, 0)
            self.label_todo_states[0].text = text

    def on_startstop_press(self, _instance):
        running = self.clock.start_stop_clock()
        if running:
            self.action_button.text = "Stop"
        else:
            self._prepare()

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, *_args):
        # Background
        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)
        # Ellipses - showing the round number
        width, height = self.size
        size = min(width, height) / 20
        y = 5.5 * height / 10
        for index, elipse in enumerate(self.ellipses):
            elipse.size = (size, size)
            x = (index + 1) * width / 9 - size / 2
            elipse.pos = (x, y)
        # labels todo
        for i in range(0, 2):
            x = self.label_todo_states[i].x
            y = self.label_todo_states[i].y
            size = self.label_todo_states[i].size
            self.labelrects[i].pos = (x, y)
            self.labelrects[i].size = size
