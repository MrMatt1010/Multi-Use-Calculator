import unittest
from kivy.uix.button import Button
from main import CalculatorApp

class CalculatorAppScientificTests(unittest.TestCase):
    def setUp(self):
        self.app = CalculatorApp()
        self.app.build()

    def test_build_sets_mode_button(self):
        self.assertFalse(self.app.scientific_mode)
        self.assertEqual(self.app.mode_button.text, "Scientific")

    def test_build_sets_mode_button_fail(self):
        self.assertEqual(self.app.mode_button.text, "Normal")

    def test_toggle_scientific_mode_switches_mode(self):
        self.app.toggle_scientific_mode(None)
        self.assertTrue(self.app.scientific_mode)
        self.assertEqual(self.app.mode_button.text, "Normal")

    def test_toggle_scientific_mode_fail(self):
        self.app.toggle_scientific_mode(None)
        self.assertEqual(self.app.mode_button.text, "Scientific")

    def test_on_scientific_button_press_sin(self):
        self.app.solution.text = ""
        button = Button(text="sin")
        self.app.on_scientific_button_press(button)
        self.assertEqual(self.app.solution.text, "sin(")

    def test_on_scientific_button_press_fail(self):
        self.app.solution.text = ""
        button = Button(text="sin")
        self.app.on_scientific_button_press(button)
        self.assertEqual(self.app.solution.text, "sin)")

    def test_on_backspace_removes_character(self):
        self.app.solution.text = "123"
        self.app.on_backspace(None)
        self.assertEqual(self.app.solution.text, "12")

    def test_on_backspace_fail(self):
        self.app.solution.text = "123"
        self.app.on_backspace(None)
        self.assertEqual(self.app.solution.text, "1234")

    def test_on_solution_sqrt(self):
        self.app.solution.text = "sqrt(16)"
        self.app.on_solution(None)
        self.assertEqual(self.app.solution.text, "4.0")

    def test_on_solution_wrong_result_fail(self):
        self.app.solution.text = "sqrt(16)"
        self.app.on_solution(None)
        self.assertEqual(self.app.solution.text, "5")

if __name__ == "__main__":
    unittest.main()
