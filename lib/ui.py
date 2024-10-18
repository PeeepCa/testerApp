import tkinter as tk
from tkinter import ttk

import lib.shared_variables


class UI:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("APAG Tester App")
        self.root.geometry(f'640x480')
        # self.root.config(bg='white')
        # self.root.anchor('center')

        # Create listbox
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()

        # Create progressbar
        self.progressbar = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="indeterminate")
        self.progressbar.place(x=70, y=410)
        # self.progressbar.pack()

        # Create menubar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Others
        self.update_interval = 100  # 1000 milliseconds = 1 second
        self.step_prev = ''
        self.update_text()

    def update_text(self):
        if lib.shared_variables.step_name != self.step_prev:
            self.listbox.insert(tk.END, lib.shared_variables.step_name)
        else:
            pass
        self.step_prev = lib.shared_variables.step_name
        self.root.after(self.update_interval, self.update_text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.run()