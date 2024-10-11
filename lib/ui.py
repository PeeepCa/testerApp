import traceback

import tkinter as tk

import lib.shared_variables


class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Basic Tkinter Window")
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()
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