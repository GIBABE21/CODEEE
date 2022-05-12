from tkinter import *

window = Tk()
window.geometry('500x500')
window.title("Determinate Beam Calculator")
window.resizable(True,True)
title = Label(window,text="Hello")
inputtxt = Text(window, height = 2, width = 10)
inputtxt.grid(row=1,column=0)
clicked = " "
options = ["in", "ft", "m", "mm",]
drop = OptionMenu(window , clicked , *options )
drop.grid(row=1,column=1)
title.grid(row=0,column=0)
window.mainloop()
# testing
