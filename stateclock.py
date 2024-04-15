""" StateClock is a module for ApneaClock - a timer application for apnea divers
    StateClock holds, as you may expect, states for a given time.
    Lets say you want to breathe, then stop breathing then breathing again, you have 2 states
    and a time where yu are in this state. There is also a next state, a first state and the
    last state, except for infinite exercises which you just stop by a button.

    Data Structure
    ~~~~~~~~~~~~~~
    states = {0: ("Prepare...", 5, 1),
              1: ("Breathe in", 4, 2),
              2: ("Hold Breath", 3, 3),
              3: ("Breathe out...", 5, 4),
              4: ("Hold Breath", 4, 1)}

    First state is 0, with the label "Prepare...". It takes 5 seconds, then the next state is 1.
    The last state is number 4, 4 seconds long and the following state is number 1. So this is an example of
    an infinite clock.

    An example for an finite clock is:

    states = {0: ("Prepare...", 5, 1),
              1: ("Breathe in", 4, 2),
              2: ("Breathe out", 4, -1)}

    The last state follows the state with the number "-1", which indicates, we are finished.

    TODO:
    - Implment finite clock
    - CONSTANT for a FINITE STATE
    - document report method
"""

from kivy.clock import Clock


class StateClock:
    NEW_STATE = 1
    RUN_STATE = 2
    FINISHED = 3

    def __init__(self, state_dict, report_method):
        """the states and a method to report to the outside world """

        self._states = state_dict
        self._report_method = report_method     # tell outside world about our state and time
        self.clock = None                   # clock object
        self.clock_is_running = False       # True, if clock is running
        self.state_label = ""               # label (name) of current state - just to report
        self.duration_of_state = 0          # duration of current state
        self.elapsed_time_in_state = 0      # elapsed time in this state
        self.next_state = 0
        self.state_load(self.next_state)

    def state_load(self, state_num):
        self.state_label, self.duration_of_state, self.next_state = self._states[state_num]
        self.elapsed_time_in_state = 0
        self._report_method(self.NEW_STATE, self.state_label, self.duration_of_state, self.elapsed_time_in_state)

    def state_next(self):
        self._stop_clock()
        if self.next_state == -1:
            self._report_method(self.FINISHED, "", 0, 0)
        else:
            self.state_load(self.next_state)
            self._start_clock()

    def time_tick(self, dt):
        self.elapsed_time_in_state += dt
        if self.elapsed_time_in_state >= self.duration_of_state:
            self.state_next()
        else:
            self._report_method(self.RUN_STATE, self.state_label, self.duration_of_state, self.elapsed_time_in_state)

    def _start_clock(self):
        self.elapsed_time_in_state = 0
        self.clock = Clock.schedule_interval(self.time_tick, 0.1)
        self.clock_is_running = True

    def _stop_clock(self):
        self.clock.cancel()
        self.clock_is_running = False

    def start_stop_clock(self):
        if self.clock_is_running:
            # user wants to stop
            self._stop_clock()
            # so it's safe to begin with first state
            self.state_load(0)
        else:
            self._start_clock()
