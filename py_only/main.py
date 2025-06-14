from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from my_layout import MyLayout
from py_only.animated_gif import AnimatedGif
from py_only.my_progress_bar import MyProgressBar


class MyApp(App):  # Основной класс-приложение, которое мы запускаем
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorotate = True
        self.sound = SoundLoader.load('music.mp3')
        self.sound.loop = True

    def build(self):

        # Главный контейнер (вертикальный)
        layout = MyLayout(orientation='vertical', spacing=10, padding=10)  # Шаблон расположения виджитов, который мы заполняем всеми виджитами

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
        self.progress_bar = MyProgressBar(self, max=len(self.image.frames), size_hint=(1, 0.1))
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
