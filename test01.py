from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse,  Color, Rectangle


class ClockWidget(Widget):
    def __init__(self, **kwargs):
        super(ClockWidget, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 0, 0, .5, mode='rgba')
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(0, 1, 0, .5, mode='rgba')
            self.circle = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def update_rect(self, *_args):
        self.rect.pos = self.pos
        self.rect.size = self.size

        self.circle.pos = self.pos

        if self.size[0] > self.size[1]:     # width > height
            # circle has minimum width/height of rect
            self.circle.size = (self.size[1], self.size[1])
            # Correct pos: circle is not in center of rect
            # CirclePos = (x, y), y=current_x + (rect.width-circle.width)/2
            self.circle.pos = (self.circle.pos[0] + (self.rect.size[0]-self.circle.size[0])/2, self.circle.pos[1])
        else:
            self.circle.size = (self.size[0], self.size[0])
            self.circle.pos = (self.circle.pos[0], self.circle.pos[1] + (self.rect.size[1] - self.circle.size[1]) / 2)


class Layout(FloatLayout):
    def __init__(self, **kwargs):
        super(Layout, self).__init__(**kwargs)
        self.w = ClockWidget(size_hint=(0.8, 0.6), pos_hint={'x': 0.1, 'y': 0.3})
        self.add_widget(self.w)


class WidgetApp(App):
    def build(self):
        return Layout(size=(300, 600))


if __name__ == '__main__':
    WidgetApp().run()
