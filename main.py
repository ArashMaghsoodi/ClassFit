import tkinter as tk
from tkinter import scrolledtext, font
from parser import parse_courses
from csp_solver import solve_all_schedules


def on_submit(input_text: str, output_label: tk.Label):
    """Handle submit button click: parse input, solve schedule, show results."""
    try:
        courses = parse_courses(input_text)
    except Exception as e:
        output_label.config(text=f"❌ خطا در پردازش ورودی: {e}", fg="red")
        return

    solutions = solve_all_schedules(courses)

    if solutions:
        result_blocks = []
        for i, solution in enumerate(solutions, start=1):
            result_lines = [f"🔹 برنامه {i}:"]
            for course_name, option in solution.items():
                times_str = "، ".join([f"{d} {s}-{e}" for d, s, e in option.times])
                result_lines.append(f"  {course_name} → {option.teacher} ({times_str})")
            result_blocks.append("\n".join(result_lines))
        output_text = "\n\n".join(result_blocks)
        output_label.config(text=output_text, fg="green", justify="right")
    else:
        output_label.config(text="❌ هیچ برنامه‌ی بدون تداخل پیدا نشد.", fg="red", justify="right")


def run_gui():
    root = tk.Tk()
    root.title("دستیار انتخاب واحد")

    # 🔹 Custom font (default fallback if not found)
    custom_font = font.Font(family="Vazirmatn", size=12)

    # Instruction label (format info)
    instruction_label = tk.Label(
        root,
        text="📌 فرمت ورودی (هر درس در یک خط):\n"
             "نام درس - نام استاد - روز ساعت شروع الی ساعت پایان[, روز ساعت شروع الی ساعت پایان ...] - واحد\n"
             "مثال:\nریاضی - محمدی - دوشنبه 14:00 الی 15:30، سه‌شنبه 14:00 الی 15:30 - 3",
        justify="right",
        anchor="e",
        font=custom_font
    )
    instruction_label.pack(padx=10, pady=10, fill="x")

    # Input area
    input_box = scrolledtext.ScrolledText(
        root,
        wrap=tk.WORD,
        width=70,
        height=15,
        font=custom_font
    )
    input_box.pack(padx=10, pady=10)

    # Submit button
    submit_btn = tk.Button(
        root,
        text="ثبت",
        font=custom_font,
        command=lambda: on_submit(input_box.get("1.0", tk.END).strip(), output_label)
    )
    submit_btn.pack(pady=5)

    # Output label
    output_label = tk.Label(root, text="", anchor="e", justify="right", font=custom_font)
    output_label.pack(padx=10, pady=10, fill="x")

    root.mainloop()


if __name__ == "__main__":
    run_gui()