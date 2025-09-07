import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont, QFontDatabase
from parser import parse_courses
from csp_solver import solve_all_schedules

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CourseSchedulerApp(QWidget):
    def __init__(self):
        super().__init__()
        logging.debug("Initializing CourseSchedulerApp")
        self.setWindowTitle("دستیار انتخاب واحد")
        self.setGeometry(200, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()
        logging.debug("Creating layout")

        # Instruction label
        instruction_label = QLabel(
            "📌 فرمت ورودی (هر درس یا اولویت در یک خط):\n"
            "درس: نام درس - نام استاد - روز ساعت شروع الی ساعت پایان[, روز ساعت شروع الی ساعت پایان ...] - واحد\n"
            "اولویت: نام درس - نام استاد\n"
            "مثال:\n"
            "سیگنال - حسینی - یکشنبه 7:45 الی 9:15، سه‌شنبه 7:45 الی 9:15 - 3\n"
            "سیگنال - هاشمی - یکشنبه 10:45 الی 12:15، دوشنبه 10:45 الی 12:15 - 3\n"
            "اولویت: سیگنال - حسینی\n"
            "اولویت: ماشین۱ - شیری"
        )
        instruction_label.setFont(QFont("Vazir", 12))
        instruction_label.setWordWrap(True)
        instruction_label.setStyleSheet("text-align: right;")
        layout.addWidget(instruction_label)
        logging.debug("Instruction label created")

        # Input text area
        self.input_box = QTextEdit()
        self.input_box.setFont(QFont("Vazir", 12))
        layout.addWidget(self.input_box)
        logging.debug("Input box created")

        # Submit button
        submit_btn = QPushButton("ثبت")
        submit_btn.setFont(QFont("Vazir", 12))
        submit_btn.setStyleSheet("background-color: green;")
        submit_btn.clicked.connect(self.on_submit)
        layout.addWidget(submit_btn)
        logging.debug("Submit button created")

        # Output text area
        self.output_box = QTextEdit()
        self.output_box.setFont(QFont("Vazir", 12))
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)
        logging.debug("Output box created")

        self.setLayout(layout)
        logging.debug("Layout set")

    def on_submit(self):
        """Handle submit button click."""
        logging.debug("Submit button clicked")
        input_text = self.input_box.toPlainText().strip()
        logging.debug(f"Input text: {input_text}")

        try:
            logging.debug("Parsing input")
            courses, priorities = parse_courses(input_text)
            logging.debug(f"Parsed courses: {courses}, priorities: {priorities}")

            logging.debug("Solving schedules")
            solutions = solve_all_schedules(courses)
            logging.debug(f"Found {len(solutions)} solutions")

            if not solutions:
                self.output_box.setPlainText("❌ هیچ برنامه‌ی بدون تداخل پیدا نشد.")
                logging.debug("No solutions found")
                return

            result_blocks = []
            for i, solution in enumerate(solutions, start=1):
                # Collect teacher names with non-zero priority
                priority_teachers = [opt.teacher for opt in solution.values() if opt.priority > 0]
                priority_text = f" (اولویت: {', '.join(priority_teachers)})" if priority_teachers else ""
                result_lines = [f"🔹 برنامه {i}{priority_text}:"]
                for course_name, option in solution.items():
                    times = "، ".join([f"{day} {start}-{end}" for day, start, end in option.times])
                    result_lines.append(f"{course_name} → {option.teacher} ({times})")
                result_blocks.append("\n".join(result_lines))
            self.output_box.setPlainText("\n\n".join(result_blocks))
            logging.debug("Output displayed")

        except Exception as e:
            error_message = f"❌ خطا در پردازش ورودی:\n{str(e)}"
            self.output_box.setPlainText(error_message)
            logging.error(f"Error processing input: {e}")

if __name__ == "__main__":
    logging.debug("Starting application")
    app = QApplication(sys.argv)
    window = CourseSchedulerApp()
    window.show()
    logging.debug("Window shown")
    sys.exit(app.exec())