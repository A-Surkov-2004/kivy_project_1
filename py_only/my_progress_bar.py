from kivy.uix.progressbar import ProgressBar


class MyProgressBar(ProgressBar):  # прогресс бар, что тут еще сказать
    def __init__(self, App, **kwargs):
        super().__init__(**kwargs)
        self.touched = 0
        self.app = App


    def on_touch_move(self, touch): # Функция, выполняющася при движении зажатой мышки по виджету
        self.touched = 10
        self.app.image.current_frame = self.value

        return super().on_touch_down(touch)
