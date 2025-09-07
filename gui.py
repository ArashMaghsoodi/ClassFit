import tkinter as tk
from tkinter import messagebox

class CourseSchedulerGUI:
    def __init__(self, root, on_submit_callback):
        self.root = root
        self.root.title("University Course Scheduler")

        # Input label
        tk.Label(root, text="Enter course list:").pack(anchor="w", padx=10, pady=5)

        # Multi-line text field
        self.text_field = tk.Text(root, height=15, width=80)
        self.text_field.pack(padx=10, pady=5)

        # Submit button
        submit_btn = tk.Button(root, text="Submit", command=self.submit)
        submit_btn.pack(pady=5)

        # Result label
        self.result_label = tk.Label(
            root,
            text="",
            justify="left",
            anchor="w",
            wraplength=600,
            fg="blue"
        )
        self.result_label.pack(padx=10, pady=10, fill="x")

        # Callback for handling logic outside GUI
        self.on_submit_callback = on_submit_callback

    def submit(self):
        raw_input = self.text_field.get("1.0", tk.END).strip()
        if not raw_input:
            messagebox.showerror("Error", "Please enter courses data!")
            return

        # Call external callback (parser + CSP solver)
        result = self.on_submit_callback(raw_input)

        # Display result
        self.result_label.config(text=result)