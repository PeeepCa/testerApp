import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import lib.shared_variables


class UI:
    def __init__(self):
        self.file_opener = None
        self.root = tk.Tk()
        self.serial_number = None
        self.progressbar = None
        self.menubar = None
        self.file_menu = None

        self.update_interval = 100  # 1000 milliseconds = 1 second

        self.build_main_window()
        self.update_text()

    def build_main_window(self):
        # Create main window
        self.root.title("APAG Tester App")
        self.root.geometry(f'640x480')

        # Create serial number label
        self.serial_number = ttk.Label(self.root, text="Serial number: " + str(lib.shared_variables.serial_number))
        self.serial_number.place(x=320, y=390, anchor="center")

        # Create progressbar
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate", value=0)
        self.progressbar.place(x=70, y=410)

        # Create menubar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open)
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    @staticmethod
    def open():
        lib.shared_variables.sequence_file = tk.filedialog.askopenfilename()
        lib.shared_variables.program_status = 'PREUUT'

    def exit_app(self):
        lib.shared_variables.program_run = False
        lib.shared_variables.program_status = 'POSTUUT'
        lib.shared_variables.app_exit = True
        self.root.destroy()

    def update_text(self):
        self.serial_number['text'] = "Serial number: " + str(lib.shared_variables.serial_number)
        self.progressbar['value'] = int(lib.shared_variables.progress_bar)
        self.root.after(self.update_interval, self.update_text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.run()