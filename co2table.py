""" co2table is a module for ApneaClock - a timer application for apnea divers
    CO_2 tables help you to manage increasing CO_2 levels in your body.
    Training:
    Prepare - Apnea 30 s - Breathe a time, Apnea 30 s, Breathe a shorter time and so on. 8 rounds.
"""
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color
from stateclock import StateClock


class Co2Table(FloatLayout):
    def __init__(self, **kwargs):
        super(Co2Table, self).__init__(**kwargs)
        # 8 turns of apnea and breathing
        self.states = {0: ("Prepare...", 3, 1),
                       1: ("Hold Breath", 3, 2), 2: ("Breathe...", 3, 3),
                       3: ("Hold Breath", 3, 4), 4: ("Breathe...", 3, 5),
                       5: ("Hold Breath", 3, 6), 6: ("Breathe...", 3, 7),
                       7: ("Hold Breath", 3, 8), 8: ("Breathe...", 3, 9),
                       9: ("Hold Breath", 3, 10), 10: ("Breathe...", 3, 11),
                       11: ("Hold Breath", 3, 12), 12: ("Breathe...", 3, 13),
                       13: ("Hold Breath", 3, 14), 14: ("Breathe...", 3, 15),
                       15: ("Hold Breath", 3, -1)}

        self.add_widget(Label(text="CO2 Table", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.label_todo = Label(text="ToDo", font_size="30pt", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.55})
        self.add_widget(self.label_todo)
        self.label_time = Label(text="00:00", font_size="30pt", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.45})
        self.add_widget(self.label_time)
        self.add_widget(Button(text="Start/Stop", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.05},
                               on_press=self.on_startstop_press))
        self.add_widget(Button(text="back", size_hint=(0.1, 0.1), pos_hint={'x': 0.05, 'y': 0.9},
                               on_press=self.on_backbutton_press))

        self.colors = []
        self.ellipses = []
        with self.canvas:
            for i in range(0, 8):
                self.colors.append(Color(0, 0, 1, .5, mode='rgba'))
                self.ellipses.append(Ellipse(size=(10, 10), size_hint=(None, None)))

        self.current_state_num = -2     # we start after preparation

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.clock = StateClock(self.states, self.stateclock_reports)

    def stateclock_reports(self, reason, label, duration, time):
        print("tick")
        self.label_todo.text = label
        if reason == StateClock.NEW_STATE:
            self.label_time.text = '{:d} s'.format(round(duration))

            self.current_state_num += 1
            if self.current_state_num >= 0:
                index = self.current_state_num // 2
                if self.current_state_num % 2 == 0:         # apnea
                    self.colors[index].rgb = [1, 0, 0]
                else:                                       # breathe
                    self.colors[index].rgb = [0, 1, 0]
        elif reason == StateClock.RUN_STATE:
            self.label_time.text = '{:d} s'.format(round(duration - time))
        else:
            # finished -> draw the last Elipse
            self.label_time.text = 'Congratulation!'
            self.colors[self.current_state_num//2].rgb = [0, 1, 0]

    def on_startstop_press(self, _instance):
        self.clock.start_stop_clock()

    def on_backbutton_press(self, _instance):
        pass

    def update_rect(self, *_args):
        width, height = self.size
        size = min(width, height) / 20
        y = 5 * height / 10
        for index, elipse in enumerate(self.ellipses):
            elipse.size = (size, size)
            x = (index + 1) * width / 10
            elipse.pos = (x, y)


class WidgetApp(App):
    def build(self):
        return Co2Table()


if __name__ == '__main__':
    WidgetApp().run()
