from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
import dbtools


class AnalyseScreen(Screen):
    def __init__(self, parentname, **kwargs):
        super(AnalyseScreen, self).__init__(**kwargs)
        self.parent_screen_name = parentname
        self.layout = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text="Auswertung", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.layout.add_widget(Button(text='↩', font_name='DejaVuSans', font_size="20pt",
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                                      on_press=self.on_backbutton_press))
        # Graph
        with self.canvas:
            Color(0.1, 0.8, 0.1)
            self.plot_milestoneline = Line(width=1)
            Color(1, 1, 0, 1)
            self.graph = Line(width=2, point=(10, 10, 100, 200))

        self.graphpoints = dbtools.get_last_n_days_from_maxtime_as_plot(100)
        self.graph_minmax = dbtools.get_minmax_breathholding_time()
        self.plot_milestone_value = 150

        # Trainingsrecords in a calendar view
        self.date_colors = []
        self.date_rects = []
        with self.canvas:
            for i in range(0, 31):
                self.date_colors.append(Color(0, 0, 1, 0.5, mode='rgba'))
                self.date_rects.append(Rectangle(size=(10, 10), size_hint=(None, None)))
        self.trainingsrecords = {}

        # background
        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5)
            self.background_rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
            Color(0.6, 0.6, 0.6, 1)
            self.plot_rect = Rectangle()
            self.calendar_rect = Rectangle()

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def on_enter(self, *args):
        # Graph
        self.graphpoints = dbtools.get_last_n_days_from_maxtime_as_plot(100)
        self.graph_minmax = dbtools.get_minmax_breathholding_time()
        # Trainingsrecords
        self.trainingsrecords = dbtools.get_trainingsrecord_this_month()
        for i in range(1, 32):
            if self.trainingsrecords[i] == 0:
                self.date_colors[i-1].rgba = (0.7, 0.7, 0.7, 1)
            elif self.trainingsrecords[i] > 0:
                self.date_colors[i - 1].rgba = (0, 1, 0, self.trainingsrecords[i] / 4)
            else:
                self.date_colors[i - 1].rgb = (0.5, 0.5, 0.5)

    def on_backbutton_press(self, _instance):
        self.manager.current = self.parent_screen_name

    def update_rect(self, *_args):
        width, height = self.size
        plot_x = 10
        plot_y = height / 3
        plot_width = width - 20
        plot_height = height / 2
        cal_x = plot_x
        cal_y = cal_x
        cal_width = plot_width
        cal_height = height / 3 - 2 * cal_y
        # background
        self.background_rect.pos = self.layout.pos
        self.background_rect.size = self.layout.size
        self.plot_rect.pos = (plot_x, plot_y)
        self.plot_rect.size = (plot_width, plot_height)
        self.calendar_rect.pos = (cal_x, cal_y)
        self.calendar_rect.size = (cal_width, cal_height)
        # Plot
        points = []
        num_points = len(self.graphpoints)
        if num_points > 0:
            scale_x = (plot_width+10) // num_points
            maxy = max(self.graph_minmax[1], self.plot_milestone_value) + 20
            scale_y = plot_height / maxy
            start_x = plot_x + 10
            start_y = plot_y
            for d, m in self.graphpoints:
                x = scale_x * d + start_x
                y = scale_y * m + start_y
                points.append(x)
                points.append(y)
            self.graph.points = points
            milestone_points = [start_x, scale_y * self.plot_milestone_value + start_y,
                                plot_width, scale_y * self.plot_milestone_value + start_y]
            self.plot_milestoneline.points = milestone_points

        # Calendar
        cal_size_w, cal_size_h = cal_width // 15, cal_height // 11
        for index, rect in enumerate(self.date_rects):
            rect.size = (cal_size_w, cal_size_h)
            col = index % 7
            row = index // 7
            x = (2 * col + 1) * cal_size_w + cal_x
            y = 10 * cal_size_h - (2 * row + 1) * cal_size_h + cal_y
            rect.pos = (x, y)
