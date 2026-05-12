# Multi Use Calculator

A simple cross-platform calculator built with Python and Kivy.

## Features

- Basic arithmetic operations: addition, subtraction, multiplication, division
- Decimal point support
- Clear button
- Error handling for invalid expressions

## Running on PC

1. Ensure Python 3.11 is installed.
2. Activate the virtual environment:
   ```
   .\venv\Scripts\activate
   ```
3. Run the app:
   ```
   python main.py
   ```

## Building for Android

To build an APK for Android, you need to install buildozer.

1. Install buildozer:
   ```
   pip install buildozer
   ```

2. Create a buildozer.spec file (you can use `buildozer init` to generate a template).

3. Build the APK:
   ```
   buildozer android debug
   ```

Note: Building for Android requires Android SDK and NDK, which can be complex to set up.

## Future Enhancements

- Scientific calculator functions
- Graphical calculator functions
- History of calculations
- Themes
- More platforms