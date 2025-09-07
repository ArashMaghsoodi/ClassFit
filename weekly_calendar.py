# weekly_calendar.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import Qt

DAYS = ["شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

class WeeklyCalendar(QWidget):
    def __init__(self, schedule, parent=None):
        """
        schedule: dict
            {
                "ریاضی": ClassOption(times=[("دوشنبه", "14:00", "15:30")], teacher="محمدی"),
                ...
            }
        """
        super().__init__(parent)
        self.schedule = schedule
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        font = QFont("Vazir", 10)

        # ستون اول: ساعت‌ها (07:00 تا 20:00)
        hours = [f"{h:02d}:00" for h in range(7, 21)]
        for row, hour in enumerate(hours, start=1):
            lbl = QLabel(hour)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(font)
            layout.addWidget(lbl, row, 0)

        # سطر اول: روزها
        for col, day in enumerate(DAYS, start=1):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(font)
            layout.addWidget(lbl, 0, col)

        # قرار دادن کلاس‌ها
        colors = ["#ff9999", "#99ff99", "#9999ff", "#ffff99", "#ffcc99", "#cc99ff", "#99ffff"]
        color_idx = 0

        for course_name, option in self.schedule.items():
            color = QColor(colors[color_idx % len(colors)])
            color_idx += 1

            for day, start, end in option.times:
                col = DAYS.index(day) + 1
                row_start = int(start.split(":")[0]) - 8 + 1
                row_end = int(end.split(":")[0]) - 8 + 1
                span = max(1, row_end - row_start + 1)

                lbl = QLabel(f"{course_name}\n{option.teacher}")
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl.setFont(font)
                palette = lbl.palette()
                palette.setColor(QPalette.ColorRole.Window, color)
                palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
                lbl.setAutoFillBackground(True)
                lbl.setPalette(palette)

                layout.addWidget(lbl, row_start, col, span, 1)

        self.setLayout(layout)