from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, Line


class StateClock:
    def __init__(self, state_dict):
        self._states = state_dict
        self.clock = None
        self.clock_is_running = False
        self.duration_of_state = 0          # duration of current state
        self.elapsed_time_in_state = 0      # elapsed time in this state
        self.next_state = 0
        self.state_load(self.next_state)
        # ... continue ...


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
        self.clock = None
        self.clock_is_running = False
        self.duration_of_state = 0          # duration of current state
        self.elapsed_time_in_state = 0      # elapsed time in this state
        self.next_state = 0
        self.add_widget(Label(text="Square Breath", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.label_todo = Label(text="ToDo", font_size="30pt",  size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.55})
        self.add_widget(self.label_todo)
        self.label_time = Label(text="00:00", font_size="30pt", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.45})
        self.add_widget(self.label_time)
        self.add_widget(Button(text="Start/Stop", size_hint=(0.9, 0.4), pos_hint={'x': 0.05, 'y': 0.05},
                               on_press=self.on_startstop_press))
        self.add_widget(Button(text="back", size_hint=(0.1, 0.1), pos_hint={'x': 0.05, 'y': 0.9},
                               on_press=self.on_backbutton_press))
        self.state_load(self.next_state)

        with self.canvas:
            Color(0, 1, 0, .5, mode='rgba')
            self.eli1 = Ellipse(size=(10, 10), size_hint=(None, None))
            self.eli2 = Ellipse(size=(10, 10), size_hint=(None, None))
            self.eli3 = Ellipse(size=(10, 10), size_hint=(None, None))
            self.eli4 = Ellipse(size=(10, 10), size_hint=(None, None))
            self.line1 = Line()

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def on_startstop_press(self, _instance):
        if self.clock_is_running:
            self.clock.cancel()
            self.clock_is_running = False
            self.state_load(0)
        else:
            self.state_run()

    def on_backbutton_press(self, _instance):
        pass

    def state_load(self, state_num):
        self.label_todo.text, self.duration_of_state, self.next_state = self.states[state_num]
        self.label_time.text = '{:d} s'.format(round(self.duration_of_state))

    def state_run(self):
        self.elapsed_time_in_state = 0
        self.clock = Clock.schedule_interval(self.time_tick, 0.1)
        self.clock_is_running = True

    def state_next(self):
        if self.next_state == -1:
            self.state_load(0)
        else:
            self.state_load(self.next_state)
            self.state_run()

    def time_tick(self, dt):
        self.elapsed_time_in_state += dt
        if self.elapsed_time_in_state >= self.duration_of_state:
            self.clock.cancel()
            self.clock_is_running = False
            self.state_next()
        else:
            self.label_time.text = '{:d} s'.format(round(self.duration_of_state - self.elapsed_time_in_state))

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
        self.eli1.size = (eli_size, eli_size)
        self.eli1.pos = (x0, y0)
        self.eli2.size = (eli_size, eli_size)
        self.eli2.pos = (x1, y0)
        self.eli3.size = (eli_size, eli_size)
        self.eli3.pos = (x0, y1)
        self.eli4.size = (eli_size, eli_size)
        self.eli4.pos = (x1, y1)
        # draw rect connecting all points
        self.line1.points = [x0+eli_size_half, y0+eli_size_half,
                             x1+eli_size_half, y0+eli_size_half,
                             x1+eli_size_half, y1+eli_size_half,
                             x0+eli_size_half, y1+eli_size_half,
                             x0+eli_size_half, y0+eli_size_half]


class WidgetApp(App):
    def build(self):
        return SquareBreath()


if __name__ == '__main__':
    WidgetApp().run()
