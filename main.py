import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from parser import parse_courses
from csp_solver import solve_all_schedules


class CourseSchedulerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("دستیار انتخاب واحد")
        self.setGeometry(200, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()

        # Instruction label
        instruction_label = QLabel(
            "📌 فرمت ورودی (هر درس در یک خط):\n"
            "نام درس - نام استاد - روز ساعت شروع الی ساعت پایان[, روز ساعت شروع الی ساعت پایان ...] - واحد\n"
            "مثال:\n"
            "ریاضی - محمدی - دوشنبه 14:00 الی 15:30، سه‌شنبه 14:00 الی 15:30 - 3"
        )
        instruction_label.setFont(QFont("Vazirmatn", 12))
        instruction_label.setWordWrap(True)
        instruction_label.setStyleSheet("text-align: right;")
        layout.addWidget(instruction_label)

        # Input text area
        self.input_box = QTextEdit()
        self.input_box.setFont(QFont("Vazirmatn", 12))
        layout.addWidget(self.input_box)

        # Submit button
        submit_btn = QPushButton("ثبت")
        submit_btn.setFont(QFont("Vazirmatn", 12))
        submit_btn.setStyleSheet("background-color: green;")
        submit_btn.clicked.connect(self.on_submit)
        layout.addWidget(submit_btn)

        # Output text area
        self.output_box = QTextEdit()
        self.output_box.setFont(QFont("Vazirmatn", 12))
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def on_submit(self):
        """Handle submit button click."""
        input_text = self.input_box.toPlainText().strip()

        try:
            courses = parse_courses(input_text)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"❌ خطا در پردازش ورودی:\n{e}")
            return

        solutions = solve_all_schedules(courses)

        if not solutions:
            self.output_box.setPlainText("❌ هیچ برنامه‌ی بدون تداخل پیدا نشد.")
            return

        result_blocks = []
        for i, solution in enumerate(solutions, start=1):
            result_lines = [f"🔹 برنامه {i}:"]
            for course_name, option in solution.items():
                times_str = "، ".join([f"{d} {s}-{e}" for d, s, e in option.times])
                result_lines.append(f"{course_name} → {option.teacher} ({times_str})")
            result_blocks.append("\n".join(result_lines))

        self.output_box.setPlainText("\n\n".join(result_blocks))


def run_app():
    app = QApplication(sys.argv)
    window = CourseSchedulerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()