import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from parser import parse_courses
from csp_solver import solve_all_schedules
from weekly_calendar import WeeklyCalendar


class CourseSchedulerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("دستیار انتخاب واحد")
        self.setGeometry(200, 200, 900, 700)

        self.solutions = []
        self.current_schedule_index = 0

        layout = QVBoxLayout()

        # Instruction label
        self.label = QLabel(
            "📌 فرمت ورودی (هر درس در یک خط):\n"
            "نام درس - نام استاد - روز ساعت شروع الی ساعت پایان[, روز ساعت شروع الی ساعت پایان ...] - واحد\n"
            "نکات:\n"
            "۱. حتما اعداد رو انگلیسی وارد کنید.\n"
            "۲. ساعت شروع و پایان کلاس را با «الی» از همدیگر جدا کنید.\n"
            "مثال:\n"
            "ریاضی - محمدی - دوشنبه 14:00 الی 15:30، سه‌شنبه 14:00 الی 15:30 - 3"
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Vazir", 12))
        layout.addWidget(self.label)

        # Input text
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Vazir", 12))
        self.text_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.text_input)

        # Submit button
        self.submit_btn = QPushButton("ثبت")
        self.submit_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.submit_btn.clicked.connect(self.process_input)
        layout.addWidget(self.submit_btn)

        # Calendar area (scrollable)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("← قبلی")
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(self.show_prev_schedule)
        nav_layout.addWidget(self.prev_btn)

        self.next_btn = QPushButton("بعدی →")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.show_next_schedule)
        nav_layout.addWidget(self.next_btn)

        layout.addLayout(nav_layout)

        self.setLayout(layout)

    def process_input(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            return

        try:
            courses = parse_courses(text)
            self.solutions = solve_all_schedules(courses)
            self.current_schedule_index = 0

            if not self.solutions:
                lbl = QLabel("❌ هیچ برنامه‌ی بدون تداخل پیدا نشد.")
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.scroll_area.setWidget(lbl)
                self.prev_btn.setEnabled(False)
                self.next_btn.setEnabled(False)
                return

            # نمایش اولین برنامه
            self.show_schedule(self.current_schedule_index)

            # فعال/غیرفعال کردن دکمه‌ها
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(len(self.solutions) > 1)

        except Exception as e:
            lbl = QLabel(f"⚠️ خطا در پردازش ورودی: {e}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scroll_area.setWidget(lbl)
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)

    def show_schedule(self, index):
        schedule = self.solutions[index]
        calendar_widget = WeeklyCalendar(schedule)
        self.scroll_area.setWidget(calendar_widget)

    def show_next_schedule(self):
        if self.current_schedule_index + 1 < len(self.solutions):
            self.current_schedule_index += 1
            self.show_schedule(self.current_schedule_index)

        # بروزرسانی وضعیت دکمه‌ها
        self.prev_btn.setEnabled(self.current_schedule_index > 0)
        self.next_btn.setEnabled(self.current_schedule_index < len(self.solutions) - 1)

    def show_prev_schedule(self):
        if self.current_schedule_index > 0:
            self.current_schedule_index -= 1
            self.show_schedule(self.current_schedule_index)

        # بروزرسانی وضعیت دکمه‌ها
        self.prev_btn.setEnabled(self.current_schedule_index > 0)
        self.next_btn.setEnabled(self.current_schedule_index < len(self.solutions) - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseSchedulerApp()
    window.show()
    sys.exit(app.exec())