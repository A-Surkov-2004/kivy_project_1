import math

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
import io
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Устанавливаем цвет (R, G, B, A)
            Color(0, 0.5, 0, 1)  # Синеватый цвет
            self.rect = Rectangle(size=(1920, 1080), pos=self.pos)



class MyProgressBar(ProgressBar):
    def __init__(self, App, **kwargs):
        super().__init__(**kwargs)
        self.touched = 0
        self.app = App


    def on_touch_move(self, touch):
        self.touched = 10
        self.app.image.current_frame = self.value

        return super().on_touch_down(touch)  # Важно для корректной работы виджетов!


class MyImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.pos = (touch.x - self.width / 2, touch.y - self.height / 2)
        return super().on_touch_down(touch)




class AnimatedGif(MyImage):
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
        """Загружает GIF и разбирает его на отдельные кадры"""
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
        """Обновляет текущий кадр анимации"""
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





class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorotate = True
        self.sound = SoundLoader.load('music.mp3')
        self.sound.loop = True

    def build(self):

        # Главный контейнер (вертикальный)
        layout = MyLayout(orientation='vertical', spacing=10, padding=10)

        # 1. Метка (Label)
        self.label = Label(text="Демо Kivy", font_size=24, size_hint=(1, 0.1))


        # 2. Текстовое поле (TextInput)
        self.text_input = TextInput(
            hint_text="Введите текст...",
            size_hint=(1, 0.1),
            multiline=False
        )
        self.text_input.bind(on_text_validate=self.on_enter_pressed)

        # 3. Кнопка (Button)
        button = Button(text="Обновить текст", size_hint=(1, 0.1))
        button.bind(on_press=self.update_label)

        # 6. Изображение (Image)
        self.image = AnimatedGif(self)

        # 4. Слайдер (Slider) + ProgressBar
        self.slider = Slider(min=0, max=len(self.image.frames), value=0, size_hint=(1, 0.1))
        self.progress_bar = MyProgressBar(self,max=len(self.image.frames), size_hint=(1, 0.1))
        self.progress_bar.touched = 3600*24*365
        self.slider.bind(value=self.on_slider_change)

        # 5. Переключатель (Switch)
        switch = Switch(size_hint=(1, 0.1)
                        )
        switch.bind(active=self.on_switch_active)



        # Добавляем все виджеты в layout
        widgets = [
            self.label,
            self.text_input,
            button,
            self.slider,
            self.progress_bar,
            switch,
            self.image
        ]
        for widget in widgets:
            layout.add_widget(widget)

        # Обновляем ProgressBar каждые 0.1 сек (анимация)
        Clock.schedule_interval(self.update_progress, 0.1)

        return layout

    # --- Обработчики событий ---
    def on_enter_pressed(self, instance):
        self.label.text = f"Вы ввели: {instance.text}"

    def update_label(self, instance):
        self.label.text = f"Текст: {self.text_input.text}"

    def on_slider_change(self, instance, value):
        self.progress_bar.value = value
        self.label.text = f"Слайдер: {int(value)}"

    def on_switch_active(self, instance, value):
        if not value:
            self.progress_bar.touched = 60*60*24*365
            self.autorotate = False
            self.sound.stop()
        else:
            self.sound.play()
            self.progress_bar.touched = 0
            self.autorotate = True
        self.label.text = f"Switch: {'Вкл' if value else 'Выкл'}"

    def update_progress(self, dt):
        # Анимация ProgressBar (если слайдер не трогают)
        if self.progress_bar.touched == 0:
            self.progress_bar.value = self.image.current_frame
        else:
            if self.autorotate:
                self.progress_bar.touched -= 1

        return  # Важно для корректной работы виджетов!




# Запуск приложения
if __name__ == "__main__":
    MyApp().run()
