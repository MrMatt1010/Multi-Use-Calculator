# Import necessary modules from Kivy for building the GUI application
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# Define the main application class that inherits from Kivy's App class
class CalculatorApp(App):
    # The build method is called automatically by Kivy to create the UI
    def build(self):
        # List of arithmetic operators used in the calculator
        self.operators = ["/", "*", "+", "-"]
        # Track if the last button pressed was an operator
        self.last_was_operator = None
        # Track the text of the last button pressed
        self.last_button = None

        # Create the main vertical layout for the calculator
        main_layout = BoxLayout(orientation="vertical")
        # Create a text input widget to display the current expression and results
        # It's read-only, right-aligned, and has a large font size
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        # Add the text input to the main layout
        main_layout.add_widget(self.solution)
        # Define the button layout in a 4x4 grid (excluding the equals button)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        # Loop through each row of buttons
        for row in buttons:
            # Create a horizontal layout for each row
            h_layout = BoxLayout()
            # Loop through each button label in the row
            for label in row:
                # Create a button with the label text
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                # Bind the button's on_press event to the on_button_press method
                button.bind(on_press=self.on_button_press)
                # Add the button to the horizontal layout
                h_layout.add_widget(button)
            # Add the horizontal layout (row) to the main layout
            main_layout.add_widget(h_layout)

        # Create the equals button separately
        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        # Bind the equals button to the on_solution method
        equals_button.bind(on_press=self.on_solution)
        # Add the equals button to the main layout
        main_layout.add_widget(equals_button)

        # Return the main layout as the root widget of the app
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
