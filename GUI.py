#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *


class App:
    def __init__(self, master):
        self.var = IntVar()
        frame = Frame(master)
        frame.pack()

        top = Toplevel(frame)
        top.title("欢迎光临")

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
        )
        self.button.pack(side=LEFT)
        self.button.config(relief=RAISED)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi, state=DISABLED)
        self.hi_there.pack(side=LEFT)
        self.button.config(relief=SUNKEN)

        self.check_button = Checkbutton(master, text='Color image', variable=self.var,
                                        command=self.cb)
        self.check_button.pack()

        self.entry = Entry(master)
        self.entry.pack()
        self.entry.focus_get()

        self.entry_button = Button(master, text="get", width=10, command=self.callback)
        self.entry_button.pack()

        Label(text="one").pack()

        separator = Frame(height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)

        Label(text="two").pack()
        Label(master, text="API_Schema_Model", font=("Helvetica", 16)).pack()

        group = LabelFrame(master, text="Group", padx=5, pady=5)
        group.pack(padx=10, pady=10)

        w = Entry(group)
        w.pack()

        self.list = Listbox(selectmode=EXTENDED)
        for item in ["api", "input_schema", "output_schema", "deser_schema", "model"]:
            self.list.insert(END, item)

        self.list.pack(fill=BOTH, expand=1)
        self.current = None
        self.poll()

        w = Message(master, text="this is a message")
        w.pack()

        m1 = PanedWindow()
        m1.pack(fill=BOTH, expand=1)

        left = Label(m1, text="left pane")
        m1.add(left)

        m2 = PanedWindow(m1, orient=VERTICAL)
        m1.add(m2)

        top = Label(m2, text="top pane")
        m2.add(top)

        bottom = Label(m2, text="bottom pane")
        m2.add(bottom)

        MODES = [
            ("Monochrome", "1"),
            ("Grayscale", "L"),
            ("True color", "RGB"),
            ("Color separation", "CMYK"),
        ]

        v = StringVar()
        v.set("L")  # initialize

        for text, mode in MODES:
            b = Radiobutton(master, text=text,
                            variable=v, value=mode)
            b.pack(anchor=W)

        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(master, yscrollcommand=scrollbar.set)
        for i in range(1000):
            listbox.insert(END, str(i))
        listbox.pack(side=LEFT, fill=BOTH)

        scrollbar.config(command=listbox.yview)

    def poll(self):
        now = self.list.curselection()
        if now != self.current:
            self.list_has_changed(now)
            self.current = now
        # self.after(250, self.poll)

    def list_has_changed(self, selection):
        print "selection is", selection

    def say_hi(self):
        print "hi there, everyone!"

    def cb(self):
        print "variable is", self.var.get()

    def callback(self):
        print self.entry.get()


root = Tk()
app = App(root)
root.mainloop()
root.destroy()  # optional; see description below
