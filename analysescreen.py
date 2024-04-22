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

        self.layout.add_widget(Label(text="Analyse", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9}))
        self.layout.add_widget(Button(text='↩', font_name='DejaVuSans', font_size="20pt",
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.01, 'y': 0.89},
                                      on_press=self.on_backbutton_press))
        # Graph
        with self.canvas:
            Color(1, 1, 0, 1)
            self.graph = Line(width=2, point=(10, 10, 100, 200))
        self.graphpoints = dbtools.get_last_n_days_from_maxtime_as_plot(100)
        self.graph_minmax = dbtools.get_minmax_breathholding_time()

        # Trainingsrecords in a calendar view
        self.date_colors = []
        self.date_rects = []
        with self.canvas:
            for i in range(0, 31):
                self.date_colors.append(Color(0, 0, 1, 0.5, mode='rgba'))
                self.date_rects.append(Rectangle(size=(10, 10), size_hint=(None, None)))
        self.trainingsrecords = {}

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
        # background
        with self.layout.canvas.before:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=self.layout.pos, size=self.layout.size)

        width, height = self.size
        # Progress Plot
        plot_x = 10
        plot_y = height / 3
        plot_width = width - 20
        plot_height = height / 2
        with self.layout.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            Rectangle(pos=(10, height / 3), size=(plot_width, plot_height))
        points = []
        num_points = len(self.graphpoints)
        for d, m in self.graphpoints:
            x = plot_width//num_points * d + plot_x + 5
            y = plot_height // self.graph_minmax[1] * m + plot_y
            points.append(x)
            points.append(y)
        self.graph.points = points

        # Calendar
        size = min(width, height) / 15
        for index, rect in enumerate(self.date_rects):
            rect.size = (size, size)
            col = index % 7
            row = index // 7
            x = (2 * col + 1) * size
            y = 7 * size - (2 * row + 1) * size * 2 / 3
            rect.pos = (x, y)

