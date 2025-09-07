import tkinter as tk
from tkinter import scrolledtext
from parser import parse_courses
from csp_solver import solve_all_schedules


def on_submit(input_text: str, output_label: tk.Label):
    # Parse courses from user input
    try:
        courses = parse_courses(input_text)
    except Exception as e:
        output_label.config(text=f"❌ Error parsing input: {e}", fg="red")
        return

    # Run CSP solver
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
        output_label.config(text=output_text, fg="green", justify="left")
    else:
        output_label.config(text="❌ هیچ برنامه‌ی بدون تداخل پیدا نشد.", fg="red")


def run_gui():
    root = tk.Tk()
    root.title("Course Scheduler")

    # Input area
    input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
    input_box.pack(padx=10, pady=10)

    # Output label
    output_label = tk.Label(root, text="", anchor="w", justify="left")
    output_label.pack(padx=10, pady=10)

    # Submit button
    submit_btn = tk.Button(
        root,
        text="ثبت",
        command=lambda: on_submit(input_box.get("1.0", tk.END).strip(), output_label)
    )
    submit_btn.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    run_gui()