# Import necessary modules from Kivy for building the GUI application
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
import math

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
        # Track if in scientific mode
        self.scientific_mode = False
        # Store reference to the main button grid
        self.button_grid = None
        # Store reference to the mode toggle button
        self.mode_button = None

        # Create the main vertical layout for the calculator
        main_layout = BoxLayout(orientation="vertical")
        
        # Create a horizontal layout for the mode toggle button
        mode_layout = BoxLayout(size_hint_y=0.1)
        self.mode_button = Button(
            text="Scientific",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.mode_button.bind(on_press=self.toggle_scientific_mode)
        mode_layout.add_widget(self.mode_button)
        main_layout.add_widget(mode_layout)
        
        # Create a text input widget to display the current expression and results
        # It's read-only, right-aligned, and has a large font size
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        # Add the text input to the main layout
        main_layout.add_widget(self.solution)
        
        # Create a grid layout for buttons (will be updated)
        self.button_grid = BoxLayout(orientation="vertical")
        main_layout.add_widget(self.button_grid)
        
        # Initialize normal mode buttons
        self.update_button_layout()

        # Return the main layout as the root widget of the app
        return main_layout

    def update_button_layout(self):
        """Update the button grid based on the current mode"""
        self.button_grid.clear_widgets()
        
        if self.scientific_mode:
            self.create_scientific_layout()
        else:
            self.create_normal_layout()
    
    def create_normal_layout(self):
        """Create the normal calculator button layout"""
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
            # Add the horizontal layout (row) to the button grid
            self.button_grid.add_widget(h_layout)

        # Create the equals button
        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        # Bind the equals button to the on_solution method
        equals_button.bind(on_press=self.on_solution)
        # Add the equals button to the button grid
        self.button_grid.add_widget(equals_button)
    
    def create_scientific_layout(self):
        """Create the scientific calculator button layout"""
        # Scientific functions in rows
        sci_buttons = [
            ["sin", "cos", "tan", "/"],
            ["sqrt", "log", "ln", "*"],
            ["π", "e", "(", ")"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "."],
            ["0", "C", "=", "Backspace"],
        ]
        
        for row in sci_buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                if label == "=":
                    button.bind(on_press=self.on_solution)
                elif label == "Backspace":
                    button.bind(on_press=self.on_backspace)
                else:
                    button.bind(on_press=self.on_scientific_button_press)
                h_layout.add_widget(button)
            self.button_grid.add_widget(h_layout)
    
    def toggle_scientific_mode(self, instance):
        """Toggle between normal and scientific mode"""
        self.scientific_mode = not self.scientific_mode
        self.mode_button.text = "Normal" if self.scientific_mode else "Scientific"
        self.update_button_layout()

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

    def on_scientific_button_press(self, instance):
        """Handle scientific button presses"""
        current = self.solution.text
        button_text = instance.text
        
        if button_text == "C":
            self.solution.text = ""
        elif button_text == "sin":
            self.solution.text = current + "sin("
        elif button_text == "cos":
            self.solution.text = current + "cos("
        elif button_text == "tan":
            self.solution.text = current + "tan("
        elif button_text == "sqrt":
            self.solution.text = current + "sqrt("
        elif button_text == "log":
            self.solution.text = current + "log10("
        elif button_text == "ln":
            self.solution.text = current + "log("
        elif button_text == "π":
            self.solution.text = current + "pi"
        elif button_text == "e":
            self.solution.text = current + "e"
        elif button_text in ["(", ")"]:
            self.solution.text = current + button_text
        elif button_text in self.operators:
            if current and not self.last_was_operator:
                self.solution.text = current + button_text
        else:
            self.solution.text = current + button_text
        
        self.last_button = button_text
        self.last_was_operator = button_text in self.operators
    
    def on_backspace(self, instance):
        """Remove the last character from the display"""
        current = self.solution.text
        if current:
            self.solution.text = current[:-1]

    # Method called when the equals button is pressed to calculate the result
    def on_solution(self, instance):
        # Get the current expression text
        text = self.solution.text
        # If there's text to evaluate
        if text:
            try:
                # Replace scientific constants and functions
                expression = text.replace("π", str(math.pi))
                expression = expression.replace("e", str(math.e))
                expression = expression.replace("sin(", "math.sin(math.radians(")
                expression = expression.replace("cos(", "math.cos(math.radians(")
                expression = expression.replace("tan(", "math.tan(math.radians(")
                expression = expression.replace("sqrt(", "math.sqrt(")
                expression = expression.replace("log10(", "math.log10(")
                expression = expression.replace("log(", "math.log(")
                
                # Add closing parentheses for trig functions
                if "math.sin(math.radians(" in expression:
                    expression = expression.rstrip(")") + "))"
                elif "math.cos(math.radians(" in expression:
                    expression = expression.rstrip(")") + "))"
                elif "math.tan(math.radians(" in expression:
                    expression = expression.rstrip(")") + "))"
                
                # Use Python's eval to compute the result and convert to string
                solution = str(eval(expression))
                # Display the result
                self.solution.text = solution
            except Exception:
                # If evaluation fails (e.g., invalid expression), show error
                self.solution.text = "Error"

# Standard Python idiom to run the app when the script is executed directly
if __name__ == "__main__":
    CalculatorApp().run()
