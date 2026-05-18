import os
import math
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
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


class HoverBehavior:
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        inside = self.collide_point(*self.to_widget(*pos))
        self.hovered = inside


class HoverButton(HoverBehavior, Button):
    pass


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
            Color(0.04, 0.08, 0.16, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.08, 0.14, 0.25, 1)
            Rectangle(pos=self.pos, size=(self.width, self.height * 0.35))

            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2
            grid_color = (0.22, 0.32, 0.45, 1)
            Color(*grid_color)
            steps = 10
            for i in range(steps + 1):
                x = self.x + i * self.width / steps
                y = self.y + i * self.height / steps
                Line(points=[x, self.y, x, self.top], width=0.7)
                Line(points=[self.x, y, self.right, y], width=0.7)

            Color(0.55, 0.7, 0.92, 1)
            Line(points=[self.x, center_y, self.right, center_y], width=1.4)
            Line(points=[center_x, self.y, center_x, self.top], width=1.4)

            if not self.expression:
                return

            points = []
            samples = 280
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
                Color(0.15, 0.80, 1, 1)
                Line(points=points, width=3, cap='round', joint='round')




class CalculatorApp(App):
    def build(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'interface.kv')
        if os.path.abspath(kv_path) in Builder.files:
            Builder.unload_file(os.path.abspath(kv_path))
        root = Builder.load_file(kv_path)

        self.operators = ['/', '*', '+', '-']
        self.last_was_operator = False
        self.last_button = None
        self.current_mode = 'Normal'

        self.normal_display = root.ids.normal_display
        self.scientific_display = root.ids.scientific_display
        self.graph_input = root.ids.graph_input
        self.graph_widget = root.ids.graph_widget
        self.screen_manager = root.ids.screen_manager

        self.mode_buttons = {
            'Normal': root.ids.btn_normal,
            'Scientific': root.ids.btn_scientific,
            'Graphical': root.ids.btn_graphical,
        }

        self.switch_mode('Normal')
        return root

    def on_mode_switch(self, mode):
        self.switch_mode(mode)

    def switch_mode(self, mode):
        self.current_mode = mode
        self.screen_manager.current = mode

        if mode == 'Normal':
            self.solution = self.normal_display
        elif mode == 'Scientific':
            self.solution = self.scientific_display
        else:
            self.solution = self.graph_input

        for name, button in self.mode_buttons.items():
            if name == mode:
                button.background_color = (0.06, 0.45, 0.92, 1)
                button.color = (1, 1, 1, 1)
            else:
                button.background_color = (0.08, 0.10, 0.16, 1)
                button.color = (0.94, 0.98, 1, 1)

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
            self.solution.text = current + button_text
        self.last_button = button_text
        self.last_was_operator = button_text in self.operators

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
