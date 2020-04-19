#!/usr/bin/env python3

from tkinter import messagebox
import tkinter as tk

from molecular_mass import get_molecular_mass

class GUI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        proportion = 100
        self.columnconfigure([0, 2], weight=0, minsize=proportion)
        self.columnconfigure([1, 3], weight=0, minsize=proportion/2)
        self.rowconfigure([1], weight=0, minsize=proportion)

        introduction = tk.Label(self, text='Wellcome to the molecular mass calculator\nInput a simple molecular formula where all numbers have 1 digit')
        introduction.grid(column=0, row=0, columnspan=4)

        label1 = tk.Label(self, text='Simplified molecular formula')
        label1.grid(column=0, row=1)
        self.entry1 = tk.Entry(self)
        self.entry1.grid(column=1, row=1)

        button1 = tk.Button(self, text='Calc', command=self.give_result)
        button1.grid(column=2, row=1)
        self.label2 = tk.Label(self, text='')
        self.label2.grid(column=3, row=1)

        button2 = tk.Button(self, text='Calc', command=self.give_results)
        button2.grid(column=2, row=3)

        label_counts = tk.Label(self, text='Amount of this molecule')
        label_counts.grid(column=0, row=3)

        self.entry_counts = tk.Entry(self)
        self.entry_counts.grid(column=1, row=3)

        self.result_mult = tk.Label(self, text='')
        self.result_mult.grid(column=3, row=3)

    def check_for_entry(self, ent):
        if not ent:
            messagebox.showwarning('Warning', 'You need to imput something :)')

    def give_result(self):
        try:
            ent = self.entry1.get()
            total = get_molecular_mass(ent)
            self.label2['text'] = str(total) + 'g/mol'
        except:
            self.check_for_entry(self.entry1.get())

    def give_results(self):
        try:
            ent = self.entry1.get()
            ent2 = float(self.entry_counts.get())
            total = get_molecular_mass(ent)
            self.result_mult['text'] = str(round(total*ent2, 2)) + 'g/mol'
        except:
            try:
                self.check_for_entry(self.entry1.get())
            except:
                self.check_for_entry(self.entry_counts.get())

def main():
    root = tk.Tk()
    root.title('Predro Molecular mass calculator')
    window = GUI(root)
    window.pack()
    root.mainloop()

if __name__ == "__main__":
    main()

