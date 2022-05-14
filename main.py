from tkinter import *
import matplotlib.pyplot as plt

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
            for k,v in self.forces.items():
                if self.end - k < 0:
                    total += v * (abs(self.end - k))
                else:
                    total -= v * (self.end - k)
            ay = (total / (self.end - self.begin))
            self.outputs.append(ay)
        elif i == self.end:
            by = 0
            total = 0
            for k,v in self.forces.items():
                if self.begin - k < 0:
                    total += v * (self.begin - k)
                else:
                    total -= v * (abs(self.begin - k))
            by = (total / (self.end - self.begin))
            self.outputs.append(by)
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
      graph1.add_force(3,4)
      graph1.add_force(3.7,6)
      graph1.add_force(4.5,4)
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
      
      # plotting the points 
      plt.plot(x, y, color='black', linestyle='solid', linewidth = 3,
         marker='o', markerfacecolor='red', markersize=5)
      # naming the x axis
      plt.xlabel('Location ('+value_inside.get()+')')
      # naming the y axis
      plt.ylabel('Force')
      # giving a title to my graph
      plt.title('Beam Display')
      # function to show the plot
      plt.show()
    except Exception as e: print(e)

    

window = Tk()
window.geometry('500x500')
window.title("Determinate Beam Calculator")
#window.state('zoomed')
window.resizable(True,True)

title = Label(window,text="Beam Numbers").grid(row=0,column=2)
inputtxt = Entry(window, width = 10)
inputtxt.grid(row=1,column=2)
left_input = Entry(window, width = 10)#
left_input.grid(row=4,column=2)
right_input = Entry(window, width = 10)#
right_input.grid(row=4,column=5)

button = Button ( window,text="Submit", command=openGraph).grid(row=0,column=7)

value_inside = StringVar(window)
  
# Set the default value of the variable
value_inside.set("in")
options = ["in", "ft", "m", "mm"]

drop = OptionMenu(window, value_inside, *options).grid(row=2,column=2)

def task():
    
    #print(graph1.outputs)
    window.after(1000, task)  # reschedule event in 2 seconds

window.after(2000, task)



window.mainloop()
# testing





