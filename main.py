from operator import length_hint
from tkinter import *

class Graph():
  def __init__(self):
      self.length = 0
      self.seperators = [0,self.length]   # |____|____|  [0, 0.4,0.8,2.2,4.7,10]
      self.forces = {0.4:6} # location:value
      self.moments = {} # location:values
      self.outputs = []
  def add_force(self,location,value):
    if location in self.forces:
      self.forces[location] += value
    else:
      self.forces[location] = value
      self.seperators.append(location)
  def add_moment(self,location,value):
    if location in self.forces:
      self.moments[location] += value
    else:
      self.moments[location] = value
      self.seperators.append(location)
  def update_forces(self):
    #self.seperators = self.seperators.sort()
    for i in self.seperators:
        if i == 0 or i == self.length:
            self.outputs.append(0)
        else:
            self.outputs.append(self.forces[i] + self.outputs[-1])
            #test

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



def task():
    graph1 = Graph()
    graph1.length = 10
    graph1.add_force(1,2)
    graph1.add_force(1.5,3)
    graph1.add_force(4.5,4)
    graph1.update_forces()
    print(graph1.outputs)
    window.after(1000, task)  # reschedule event in 2 seconds

window.after(2000, task)



window.mainloop()
# testing




