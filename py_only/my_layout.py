from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout


class MyLayout(BoxLayout): # Шаблон расположения виджитов, который мы заполняем всеми виджитами
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Устанавливаем цвет (R, G, B, A)
            Color(0, 0.5, 0, 1)  # Синеватый цвет
            self.rect = Rectangle(size=(1920, 1080), pos=self.pos)
