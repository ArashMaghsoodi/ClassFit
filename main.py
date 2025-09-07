import tkinter as tk
from gui import CourseSchedulerGUI

def handle_submit(raw_input: str) -> str:
    # TODO: integrate parser + CSP solver
    return "Algorithm result will be shown here."

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseSchedulerGUI(root, handle_submit)
    root.mainloop()