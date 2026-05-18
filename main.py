import os
import math
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
Builder.load_file(os.path.join(os.path.dirname(__file__), 'interface.kv'))
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle

SAFE_MATH = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'sqrt': math.sqrt,
    'exp': math.exp,
    'pi': math.pi,
    'e': math.e,
    'abs': abs,
    'pow': pow,
}


def safe_eval(expression, x=None):
    expression = expression.replace('^', '**')
    local_vars = {'x': x} if x is not None else {}
    local_vars.update(SAFE_MATH)
    try:
        return eval(expression, {'__builtins__': None}, local_vars)
    except Exception:
        return None


class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expression = ''
        self.bind(pos=self.redraw, size=self.redraw)

    def plot(self, expression):
        self.expression = expression
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.06, 0.12, 0.2, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.6, 0.6, 0.6, 1)
            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2
            Line(points=[self.x, center_y, self.right, center_y], width=1)
            Line(points=[center_x, self.y, center_x, self.top], width=1)

            if not self.expression:
                return

            points = []
            samples = 240
            x_range = 10.0
            y_limit = 10.0
            prev_point = None

            for i in range(samples + 1):
                x = -x_range + (2 * x_range) * i / samples
                y = safe_eval(self.expression, x)
                if y is None or isinstance(y, complex) or abs(y) > y_limit:
                    prev_point = None
                    continue
                gx = center_x + (x / x_range) * (self.width / 2)
                gy = center_y + (y / y_limit) * (self.height / 2)
                if prev_point is not None:
                    points.extend([prev_point[0], prev_point[1], gx, gy])
                prev_point = (gx, gy)

            if points:
                Color(0.18, 0.78, 1, 1)
                Line(points=points, width=2)


class CalculatorApp(App):
    def build(self):
        self.operators = ['/', '*', '+', '-']
        self.last_was_operator = False
        self.last_button = None
        self.mode_buttons = {}

        root = BoxLayout(orientation='vertical')
        mode_bar = BoxLayout(size_hint_y=None, height=48)
        for mode in ['Normal', 'Scientific', 'Graphical']:
            button = Button(text=mode)
            button.bind(on_press=self.on_mode_switch)
            self.mode_buttons[mode] = button
            mode_bar.add_widget(button)
        root.add_widget(mode_bar)

        self.screen_manager = ScreenManager()
        self.normal_screen = Screen(name='Normal')
        self.scientific_screen = Screen(name='Scientific')
        self.graph_screen = Screen(name='Graphical')

        self.setup_normal_screen()
        self.setup_scientific_screen()
        self.setup_graph_screen()

        self.screen_manager.add_widget(self.normal_screen)
        self.screen_manager.add_widget(self.scientific_screen)
        self.screen_manager.add_widget(self.graph_screen)

        root.add_widget(self.screen_manager)
        self.switch_mode('Normal')
        return root

    def on_mode_switch(self, instance):
        self.switch_mode(instance.text)

    def switch_mode(self, mode):
        self.screen_manager.current = mode
        self.current_mode = mode
        if mode == 'Normal':
            self.solution = self.normal_display
        elif mode == 'Scientific':
            self.solution = self.scientific_display
        else:
            self.solution = self.graph_input

        for name, button in self.mode_buttons.items():
            button.background_color = (0.14, 0.18, 0.28, 1) if name == mode else (0.08, 0.10, 0.16, 1)

    def setup_normal_screen(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.normal_display = TextInput(multiline=False, readonly=True, halign='right', font_size=48)
        layout.add_widget(self.normal_display)

        button_grid = GridLayout(cols=4, spacing=10, size_hint_y=None)
        button_grid.bind(minimum_height=button_grid.setter('height'))
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', 'C', '+',
        ]
        for label in buttons:
            button = Button(text=label)
            button.bind(on_press=self.on_button_press)
            button_grid.add_widget(button)
        layout.add_widget(button_grid)

        equals_button = Button(text='=', size_hint_y=None, height=60)
        equals_button.bind(on_press=self.on_solution)
        layout.add_widget(equals_button)

        self.normal_screen.add_widget(layout)

    def setup_scientific_screen(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.scientific_display = TextInput(multiline=False, readonly=True, halign='right', font_size=48)
        layout.add_widget(self.scientific_display)

        button_grid = GridLayout(cols=5, spacing=10, size_hint_y=None)
        button_grid.bind(minimum_height=button_grid.setter('height'))
        buttons = [
            'sin', 'cos', 'tan', 'log', 'sqrt',
            '(', ')', '^', 'C', 'ANS',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', '00', '+',
        ]
        for label in buttons:
            button = Button(text=label)
            button.bind(on_press=self.on_scientific_button_press)
            button_grid.add_widget(button)
        layout.add_widget(button_grid)

        equals_button = Button(text='=', size_hint_y=None, height=60)
        equals_button.bind(on_press=self.on_solution)
        layout.add_widget(equals_button)

        self.scientific_screen.add_widget(layout)

    def setup_graph_screen(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        input_row = BoxLayout(size_hint_y=None, height=60, spacing=10)
        input_row.add_widget(Label(text='f(x)=', size_hint_x=None, width=70, color=(0.94, 0.98, 1, 1)))
        self.graph_input = TextInput(multiline=False, halign='left', font_size=32)
        plot_button = Button(text='Plot', size_hint_x=None, width=100)
        plot_button.bind(on_press=self.on_graph_plot)
        input_row.add_widget(self.graph_input)
        input_row.add_widget(plot_button)
        layout.add_widget(input_row)

        self.graph_widget = GraphWidget()
        layout.add_widget(self.graph_widget)
        self.graph_screen.add_widget(layout)

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        if button_text == 'C':
            self.solution.text = ''
        else:
            if current and self.last_was_operator and button_text in self.operators:
                return
            if current == '' and button_text in self.operators:
                return
            new_text = current + button_text
            self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_scientific_button_press(self, instance):
        label = instance.text
        if label == 'C':
            self.scientific_display.text = ''
            self.last_button = None
            self.last_was_operator = False
            return
        if label == 'ANS':
            self.scientific_display.text += self.scientific_display.text or ''
            return
        current = self.scientific_display.text
        if current and self.last_was_operator and label in self.operators:
            return
        if current == '' and label in self.operators:
            return
        self.scientific_display.text = current + label
        self.last_button = label
        self.last_was_operator = label in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if not text:
            return
        text = text.replace('^', '**')
        result = safe_eval(text)
        self.solution.text = str(result) if result is not None else 'Error'

    def on_graph_plot(self, instance):
        expression = self.graph_input.text.strip()
        if not expression:
            return
        self.graph_widget.plot(expression)


if __name__ == '__main__':
    CalculatorApp().run()
