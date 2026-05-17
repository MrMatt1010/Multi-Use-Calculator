import unittest
from kivy.uix.button import Button
from main import CalculatorApp

class CalculatorAppMainTests(unittest.TestCase):
    def setUp(self):
        self.app = CalculatorApp()
        self.app.build()

    def test_build_returns_boxlayout(self):
        root = self.app.build()
        self.assertEqual(root.__class__.__name__, "BoxLayout")
        self.assertTrue(hasattr(self.app, "solution"))

    def test_build_returns_button_fail(self):
        root = self.app.build()
        self.assertEqual(root.__class__.__name__, "Button")

    def test_on_button_press_adds_digit(self):
        self.app.solution.text = ""
        button = Button(text="5")
        self.app.on_button_press(button)
        self.assertEqual(self.app.solution.text, "5")

    def test_on_button_press_operator_start_fail(self):
        self.app.solution.text = ""
        button = Button(text="+")
        self.app.on_button_press(button)
        self.assertEqual(self.app.solution.text, "+")

    def test_on_solution_calculates_result(self):
        self.app.solution.text = "2+3*4"
        self.app.on_solution(None)
        self.assertEqual(self.app.solution.text, "14")

    def test_on_solution_wrong_result_fail(self):
        self.app.solution.text = "2+3*4"
        self.app.on_solution(None)
        self.assertEqual(self.app.solution.text, "15")

if __name__ == "__main__":
    unittest.main()
