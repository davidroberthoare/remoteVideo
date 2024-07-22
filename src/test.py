from tkinter import *
from tkinter import ttk
from tkvideo import tkvideo

root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
my_label = Label(root)
my_label.pack()
player = tkvideo.tkvideo("../media_client/test3.mp4", my_label, loop = 1, size = (1280,720))
player.play()


root.mainloop()