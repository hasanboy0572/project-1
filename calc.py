from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.core.clipboard import Clipboard


class ColoredLabel(Label):
    """Label uchun orqa fon qo'shish"""
    def __init__(self, bg_color=(0, 0.4, 0, 1), **kwargs):  # To‘q yashil orqa fon
        super().__init__(**kwargs)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CalculatorApp(App):
    def build(self):
        root_layout = AnchorLayout(anchor_x='center', anchor_y='center')

        main_layout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(800, 700))

        # Son kiritish qismi (faqat raqamli klaviatura ochiladi)
        self.input_field = TextInput(
            hint_text="Son kiriting",
            font_size=56,
            size_hint_y=None,
            height=140,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            halign="center",
            input_filter="float",
            input_type="number",
            padding=(0, 35, 0, -35)  # Matnni 0.8 sm pastroqqa tushirish
        )
        main_layout.add_widget(self.input_field)

        # Hisoblash tugmasi
        calc_button = Button(
            text="Hisoblash",
            font_size=56,
            size_hint_y=None,
            height=140,
            background_color=(0, 0, 1, 1),  # Ko‘k rang
            color=(1, 1, 1, 1)
        )
        calc_button.bind(on_press=self.calculate)
        main_layout.add_widget(calc_button)

        # Natija chiqarish uchun quti
        self.result_layout = GridLayout(cols=3, size_hint_y=None, height=280)

        # BIG natijasi
        self.big_text = ColoredLabel(text="BIG:", font_size=56, color=(1, 1, 1, 1), bg_color=(0, 0.5, 0, 1))  # To‘q yashil
        self.big_label = ColoredLabel(text="0", font_size=56, color=(1, 1, 0, 1), bg_color=(0, 0.4, 0, 1))  # Yashil
        self.big_copy = Button(
            text="COPY", font_size=40, size_hint_x=None, width=140, background_color=(0.2, 0.2, 0.2, 1)  # To‘q kulrang
        )

        # SMALL natijasi
        self.small_text = ColoredLabel(text="SMALL:", font_size=56, color=(1, 1, 1, 1), bg_color=(0, 0.5, 0, 1))  # To‘q yashil
        self.small_label = ColoredLabel(text="0", font_size=56, color=(1, 1, 0, 1), bg_color=(0, 0.4, 0, 1))  # Yashil
        self.small_copy = Button(
            text="COPY", font_size=40, size_hint_x=None, width=140, background_color=(0.2, 0.2, 0.2, 1)  # To‘q kulrang
        )

        # Nusxalash tugmalarini bog'lash
        self.big_copy.bind(on_press=lambda x: self.copy_to_clipboard(self.big_label.text))
        self.small_copy.bind(on_press=lambda x: self.copy_to_clipboard(self.small_label.text))

        # Natijalarni joylashtirish
        self.result_layout.add_widget(self.big_text)
        self.result_layout.add_widget(self.big_label)
        self.result_layout.add_widget(self.big_copy)

        self.result_layout.add_widget(self.small_text)
        self.result_layout.add_widget(self.small_label)
        self.result_layout.add_widget(self.small_copy)

        # Natijalar maydonini asosiy layoutga qo‘shish
        main_layout.add_widget(self.result_layout)

        # Barcha narsalarni markazga joylashtirish
        root_layout.add_widget(main_layout)
        return root_layout

    def calculate(self, instance):
        try:
            user_input = float(self.input_field.text)
            big = (1.891 / (1.891 + 2.125)) * user_input
            small = user_input - big
            big_rounded = round(big, 2)
            small_rounded = round(small, 2)

            self.big_label.text = str(big_rounded)
            self.small_label.text = str(small_rounded)
        except ValueError:
            self.big_label.text = "Xato!"
            self.small_label.text = "Xato!"

    def copy_to_clipboard(self, text):
        Clipboard.copy(text)


if __name__ == "__main__":
    CalculatorApp().run()