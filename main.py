from ctypes.wintypes import RGB
from tkinter import *
from matplotlib.patches import Rectangle
from ttkthemes import ThemedTk,THEMES
import matplotlib.pyplot as plt
from numpy import blackman

class Graph():
  def __init__(self, length, begin, end):
      self.length = length
      self.seperators = list()   # |____|____|  [0, 0.4,0.8,2.2,4.7,10]
      self.seperators.append(begin)
      self.seperators.append(end)
      self.forces = {} # location:value
      self.moments = {} # location:value
      self.outputs = []
      self.begin = begin
      self.end = end
  def add_force(self, location, value):
    if location in self.forces:
      self.forces[location] += value
    else:
      self.forces[location] = value
      self.seperators.append(location)
  def add_moment(self, location, value):
    if location in self.moments:
      self.moments[location] += value
    else:
      self.moments[location] = value
      self.seperators.append(location)
  def update_forces(self):
    for i in self.seperators:
        if i == self.begin:
            ay = 0
            total = 0
            jump = 0
            for k,v in self.forces.items():
                if self.end - k < 0:
                    total += v * (abs(self.end - k))
                else:
                    total -= v * (self.end - k)
            ay = (total / (self.end - self.begin))
            #print(ay)
            jump = self.outputs[-1] + ay
            self.outputs.append(jump)
        elif i == self.end:
            by = 0
            total = 0
            jump = 0
            for k,v in self.forces.items():
                if self.begin - k < 0:
                    total -= v * (abs(self.begin - k))
                else:
                    total += v * (self.begin - k)
            by = (total / (self.end - self.begin))
            #print(by)
            jump = self.outputs[-1] + by
            self.outputs.append(jump)
        else:
            if len(self.outputs) == 0:
                self.outputs.append(self.forces[i])
            else:
                self.outputs.append(self.forces[i] + self.outputs[-1])

# 10 2 6
def openGraph():
    global inputtxt
    global left_input
    global right_input
    print(value_inside.get())
    try:
      graph1 = Graph(float(inputtxt.get()), float(left_input.get()), float(right_input.get()))
      graph1.add_force(1,4)
      graph1.add_force(2,6)
      graph1.add_force(4.5,4)
      graph1.add_force(8,10)
      graph1.add_force(9.5,1)
      graph1.seperators = sorted(graph1.seperators) 
      graph1.update_forces()

      # duplicating x for the graph
      x = graph1.seperators
      x += graph1.seperators
      x.append(0)
      x.append(float(inputtxt.get()))
      x = sorted(x)
      # duplicating y for the graph
      y = [0,0]
      for i,v in enumerate(graph1.outputs):
        if i < len(graph1.outputs)-1:
          y.append(v)
          y.append(v) 
      y += [0,0]
      print(x)
      print(y)
      fig, axs = plt.subplots(3)
      fig.suptitle('')
      axs[0].axes.yaxis.set_visible(False)
      axs[0].plot([0,float(inputtxt.get())],[0,10],color='gray', linestyle='None', linewidth = 3, markerfacecolor='white', markersize=5)
      axs[0].set_title('Load Diagram')
      axs[0].add_patch(Rectangle((0,4),float(inputtxt.get()),2,color = 'grey'))
      axs[0].arrow(1,10,0,-4,head_width = 0.1,head_length = 0.3,width = 0.05,color='blue')
      axs[0].arrow(2,6,0,4,head_width = 0.1,head_length = 0.3,width = 0.05,color='blue')
      axs[1].plot(x, y, color='black', linestyle='solid', linewidth = 3,
         marker='o', markerfacecolor='red', markersize=5)
      axs[1].set_title("Sheer Diagram")
      axs[1].set_xlabel('Location ('+value_inside.get()+')')
      axs[1].set_ylabel('Force')
      #axs[0].xlabel("x")
      #axs[0].ylabel("y")
      axs[2].plot([1,2,3,4], [1,2,3,1], color='gray', linestyle='solid', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=5)
      axs[2].set_title("Moment Diagram")
      axs[2].set_xlabel('some else ('+value_inside.get()+')')
      axs[2].set_ylabel('Force')
      # plotting the points 
      plt.tight_layout()
      # function to show the plot
      plt.show()
    except Exception as e: print(e)

    

window = ThemedTk(themebg=True)
window.set_theme('black')
window.geometry('350x200')
window.title("Determinate Beam Calculator")
#window.config(background='black')
#window.state('zoomed')
window.resizable(True,True)
frame = Frame(window)
frame.pack(side=TOP)
title = Label(frame,text="Beam Length").grid(row=0,column=1)
inputtxt = Entry(frame, width = 10)
inputtxt.grid(row=3,column=1)
label1 = Label(frame,text="Left Support").grid(row=15,column=0)
left_input = Entry(frame, width = 10)
left_input.grid(row=16,column=0)
label1 = Label(frame,text="Right Support").grid(row=15,column=2)
right_input = Entry(frame, width = 10)
right_input.grid(row=16,column=2)

button = Button ( frame,text="Submit", command=openGraph).grid(row=20,column=1)

value_inside = StringVar(window)
  
# Set the default value of the variable
value_inside.set("in")
options = ["in", "ft", "m", "mm"]

drop = OptionMenu(frame, value_inside, *options).grid(row=3,column=2)

def task():
    
    #print(graph1.outputs)
    window.after(1000, task)  # reschedule event in 2 seconds

window.after(2000, task)



window.mainloop()
# testing





