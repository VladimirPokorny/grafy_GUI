import tkinter as tk
settings = {"foo": 1, "bar": 1, "baz": 1}

def makeSomething(name):
    print(settings[name])

root = tk.Tk()
tk.Button(root, text='Set foo', command=lambda *args: makeSomething("foo")).pack()
tk.Button(root, text='Set bar', command=lambda *args: makeSomething("bar")).pack()
tk.Button(root, text='Set baz', command=lambda *args: makeSomething("baz")).pack()
root.mainloop()


