from kivy.uix.image import Image


class MyImage(Image):  # Своя реализация виджета-картинки, позволяющая перетаскивать его мышкой по экрану
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_move(self, touch): # Функция, выполняющася при движении зажатой мышки по виджету
        if self.collide_point(*touch.pos):
            self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)
        return super().on_touch_down(touch)
