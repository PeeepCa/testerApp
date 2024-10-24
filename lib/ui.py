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
        self.view_menu = None
        self.file_menu = None
        self.run_button = None
        self.stop_button = None
        self.test_result = None
        self.c = None
        self.result_box = None
        self.update_interval = 100  # 1000 milliseconds = 1 second
        self.application_path = lib.shared_variables.application_path

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

        self.build_main_window()
        self.update_text()

    def build_main_window(self):
        # Create main window
        self.root.title("APAG Tester App")
        self.root.geometry(f'640x480')
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap(str(self.application_path) + "\\app_icon.ico")
        except tk.TclError:
            pass

        # Create serial number label
        self.serial_number = ttk.Label(self.root, text="Serial number: " + str(lib.shared_variables.serial_number))
        self.serial_number.place(x=320, y=380, anchor="center")

        # Create progressbar
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate", value=0)
        self.progressbar.place(x=70, y=400)

        # Create menubar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open)
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        # Create view menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='View', menu=self.view_menu)
        self.view_menu.add_command(label="Debugger", command='')

        # Create help menu
        self.menubar.add_cascade(label='Help', command='')

        # Create buttons
        self.run_button = ttk.Button(self.root, text="Run", command=self.run_button_click)
        self.run_button.place(x=460, y=440, anchor="center")
        self.run_button.config(state='disabled')

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_button_click)
        self.stop_button.place(x=535, y=440, anchor="center")
        self.stop_button.config(state='disabled')

        # Create label with test result
        self.test_result = ttk.Label(self.root, text="Result: " + str(lib.shared_variables.test_result))
        self.test_result.place(x=320, y=360, anchor="center")

        # Create canvas
        self.c = tk.Canvas(self.root, width=500, height=330)
        self.result_box = self.c.create_rectangle(0, 20, 500, 330, fill="white", outline="white")
        self.c.pack()

    def open(self):
        with lib.shared_variables.shared_condition:
            lib.shared_variables.sequence_file = tk.filedialog.askopenfilename()
            lib.shared_variables.program_status = 'PREUUT'
            self.run_button.config(state='normal')
            lib.shared_variables.shared_condition.notify()

    def run_button_click(self):
        with lib.shared_variables.shared_condition:
            self.menubar.entryconfig('File', state='disabled')
            self.menubar.entryconfig('View', state='disabled')
            self.menubar.entryconfig('Help', state='disabled')
            self.run_button.config(state='disabled')
            self.stop_button.config(state='normal')
            lib.shared_variables.main_run = True
            lib.shared_variables.program_status = 'SEQUENCE'
            lib.shared_variables.shared_condition.notify()

    def stop_button_click(self):
        self.menubar.entryconfig('File', state='normal')
        self.menubar.entryconfig('View', state='normal')
        self.menubar.entryconfig('Help', state='normal')
        self.run_button.config(state='normal')
        lib.shared_variables.main_run = False
        lib.shared_variables.program_status = None

    def exit_app(self):
        lib.shared_variables.main_run = False
        with lib.shared_variables.shared_condition:
            lib.shared_variables.program_status = 'POSTUUT'
            lib.shared_variables.shared_condition.notify()
        self.root.after(100, self.root.quit)
        self.root.after(200, self.root.destroy)


    def update_text(self):
        self.serial_number['text'] = "Serial number: " + str(lib.shared_variables.serial_number)
        self.progressbar['value'] = int(lib.shared_variables.progress_bar)
        self.test_result['text'] = "Result: " + str(lib.shared_variables.test_result)
        match lib.shared_variables.test_result:
            case 'PASS':
                self.c.itemconfig(self.result_box, fill="green", outline="green")
            case 'FAIL':
                self.c.itemconfig(self.result_box, fill="red", outline="red")
            case None:
                self.c.itemconfig(self.result_box, fill="white", outline="white")
        self.root.after(self.update_interval, self.update_text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.run()