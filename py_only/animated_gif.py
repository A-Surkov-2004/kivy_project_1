import math

from PIL import Image as PILImage
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from py_only.my_image import MyImage


class AnimatedGif(MyImage):  # Своя реализация виджета-картинки, позволяющая загружать GIF изображения
    def __init__(self, App, **kwargs):
        super().__init__(**kwargs)
        self.app = App
        self.frames = []
        self.current_frame = 0
        self.delay = 0.05  # Задержка между кадрами (в секундах)

        # Загрузка GIF из файла или ресурсов
        self.load_gif("img.gif")  # Укажите путь к вашему GIF

        # Запуск анимации
        Clock.schedule_interval(self.update_frame, self.delay)

    def load_gif(self, filename):
        # Загружает GIF и разбирает его на отдельные кадры
        try:
            with PILImage.open(filename) as gif:
                self.frames = []
                try:
                    while True:
                        frame = gif.copy()
                        frame = frame.rotate(180)
                        if frame.mode != 'RGBA':
                            frame = frame.convert('RGBA')
                        self.frames.append(frame)
                        gif.seek(len(self.frames))  # Переход к следующему кадру
                except EOFError:
                    pass

                # Установка задержки из GIF, если она есть
                if hasattr(gif, 'info') and 'duration' in gif.info:
                    self.delay = gif.info['duration'] / 1000.0
        except Exception as e:
            print(f"Ошибка загрузки GIF: {e}")

    def update_frame(self, dt):
        #  Обновляет текущий кадр анимации
        if not self.frames:
            return

        if self.app.progress_bar.touched == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        frame = self.frames[math.floor(self.current_frame)% len(self.frames)]

        # Создаем текстуру Kivy из кадра
        buf = frame.tobytes()
        texture = Texture.create(
            size=frame.size,
            colorfmt='rgba'
        )
        texture.blit_buffer(
            buf,
            colorfmt='rgba',
            bufferfmt='ubyte'
        )
        self.texture = texture
