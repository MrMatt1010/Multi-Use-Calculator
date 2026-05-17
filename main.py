# Import necessary modules from Kivy for building the GUI application
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class NeonButton(Button):
    pass

class NeonTextInput(TextInput):
    pass

# Define the main application class that inherits from Kivy's App class
class CalculatorApp(App):
    # The build method is called automatically by Kivy to create the UI
    def build(self):
        Builder.load_file("interface.kv")
        Window.clearcolor = (0.02, 0.03, 0.08, 1)

        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation="vertical")

        self.solution = NeonTextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=55,
            text="",
        )
        main_layout.add_widget(self.solution)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]

        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for label in row:
                button = NeonButton(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = NeonButton(
            text="=",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint_y=0.95,
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    # Method called when any button (except equals) is pressed
    def on_button_press(self, instance):
        # Get the current text in the solution display
        current = self.solution.text
        # Get the text of the button that was pressed
        button_text = instance.text

        # If the clear button is pressed, reset the display
        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        else:
            # Prevent adding two operators in a row
            if current and (
                self.last_was_operator and button_text in self.operators):
                # Don't add two operators right after each other
                return
            # Prevent starting with an operator
            elif current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                # Append the button text to the current expression
                new_text = current + button_text
                self.solution.text = new_text
        # Update the last button pressed
        self.last_button = button_text
        # Update the flag for whether the last button was an operator
        self.last_was_operator = self.last_button in self.operators

    # Method called when the equals button is pressed to calculate the result
    def on_solution(self, instance):
        # Get the current expression text
        text = self.solution.text
        # If there's text to evaluate
        if text:
            try:
                # Use Python's eval to compute the result and convert to string
                solution = str(eval(text))
                # Display the result
                self.solution.text = solution
            except Exception:
                # If evaluation fails (e.g., invalid expression), show error
                self.solution.text = "Error"

# Standard Python idiom to run the app when the script is executed directly
if __name__ == "__main__":
    CalculatorApp().run()
