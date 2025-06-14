from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty
from kivy.animation import Animation


# Кастомный виджет (можно использовать в .kv)
class FancyButton(Screen):
    counter = NumericProperty(0)  # Счётчик для анимации
    status_text = StringProperty("Нажми меня!")  # Динамический текст

    def on_press(self):
        self.canvas.before
        self.counter += 1
        self.status_text = f"Нажато: {self.counter} раз"

        # Анимация кнопки
        anim = Animation(size=(90, 90), duration=0.05)+Animation(size=(80, 80), duration=0.05)

        anim.start(self.ids.btn)


# Главный класс приложения
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FancyButton(name="main"))
        return sm


if __name__ == "__main__":
    MyApp().run()