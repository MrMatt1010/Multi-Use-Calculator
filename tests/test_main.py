import unittest
from kivy.uix.button import Button
from main import CalculatorApp

class CalculatorAppInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.app = CalculatorApp()
        self.app.build()

    def test_build_loads_interface_kv(self):
        root = self.app.build()
        self.assertEqual(root.__class__.__name__, "BoxLayout")
        self.assertTrue(hasattr(self.app, "solution"))
        self.assertEqual(self.app.solution.text, "")

    def test_build_returns_button_fail(self):
        root = self.app.build()
        self.assertEqual(root.__class__.__name__, "Button")

    def test_on_button_press_adds_digit(self):
        self.app.solution.text = ""
        button = Button(text="7")
        self.app.on_button_press(button)
        self.assertEqual(self.app.solution.text, "7")

    def test_on_button_press_block_double_operator_fail(self):
        self.app.solution.text = "5+"
        self.app.last_was_operator = True
        button = Button(text="+")
        self.app.on_button_press(button)
        self.assertEqual(self.app.solution.text, "5++")

    def test_on_solution_calculates_result(self):
        self.app.solution.text = "4*5"
        self.app.on_solution(None)
        self.assertEqual(self.app.solution.text, "20")

    def test_on_solution_wrong_result_fail(self):
        self.app.solution.text = "4*5"
        self.app.on_solution(None)
        self.assertEqual(self.app.solution.text, "21")

if __name__ == "__main__":
    unittest.main()
