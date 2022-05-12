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

graph1 = Graph()
graph1.add_force(2,5)


class Graph():
  def __init__(self):
      self.seperators = []   # |____|____|  [ 0, 0.4,0.8,2.2,4.7,10]
      self.forces = {0.4:6} # location:value
      self.length = 0
      self.moments = {} # location:values
  def add_force(self,value,location):
    if location in self.forces:
      self.forces[location] += value
    else:
      self.forces[location] = value
      self.seperators.append(location)
  def add_moment(self,value,location):
    if location in self.forces:
      self.moments[location] += value
    else:
      self.moments[location] = value
      self.seperators.append(location)
  def update_forces(self):
    print('do it here')