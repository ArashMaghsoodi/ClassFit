# ClassFit

A Python-based application for generating conflict-free course schedules based on user-defined courses, teachers, time slots, and priorities. Built with PyQt6 for a graphical user interface.

## Features
- Generates all possible conflict-free schedules for a given set of courses.
- Supports course prioritization based on teacher preferences.
- Displays schedules with prioritized teachers' names instead of numerical priorities.
- User-friendly GUI with Persian text support.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ArashMaghsoodi/ClassFit.git
   cd course-scheduler
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. In the GUI, enter your course details and priorities in the input box using the following format:
   ```
   درس: نام درس - نام استاد - روز ساعت شروع الی ساعت پایان[, روز ساعت شروع الی ساعت پایان ...] - واحد
   اولویت: نام درس - نام استاد
   ```
   Example:
   ```
   سیگنال - حسینی - یکشنبه 7:45 الی 9:15، سه‌شنبه 7:45 الی 9:15 - 3
   سیگنال - هاشمی - یکشنبه 10:45 الی 12:15، دوشنبه 10:45 الی 12:15 - 3
   مدار۲ - شمس - شنبه 7:45 الی 9:15، دوشنبه 7:45 الی 9:15 - 3
   ماشین۱ - قندهاری - شنبه 7:45 الی 9:15، دوشنبه 7:45 الی 9:15 - 3
   ماشین۱ - قندهاری - شنبه 9:15 الی 10:45، دوشنبه 9:15 الی 10:45 - 3
   ماشین۱ - شیری - شنبه 9:15 الی 10:45، دوشنبه 9:15 الی 10:45 - 3
   ماشین۱ - حسینی - شنبه 9:15 الی 10:45، دوشنبه 9:15 الی 10:45 - 3
   اولویت: سیگنال - حسینی
   اولویت: ماشین۱ - شیری
   ```
3. Click the "ثبت" (Submit) button to generate and display conflict-free schedules.
4. The output will show schedules sorted by priority, with prioritized teachers' names displayed (e.g., `اولویت: حسینی، شیری`).

## Project Structure
- `main.py`: Main application with the PyQt6 GUI.
- `parser.py`: Parses user input into course objects and priorities.
- `csp_solver.py`: Solves the scheduling problem using a backtracking algorithm.
- `models.py`: Defines data models (`Course` and `ClassOption`).

## Requirements
See `requirements.txt` for dependencies. Currently requires:
- PyQt6 (>=6.7.0)
- pyinstaller (>=5.13.0)

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss improvements.

## Contact
For questions or feedback, contact animats84@gmail.com.