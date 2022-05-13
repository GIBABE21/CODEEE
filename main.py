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
    #print(self.seperators)
    for i in self.seperators:
        if i == self.begin:
            ay = 0
            total = 0
            for k,v in self.forces.items():
                total += v * (self.length - k)
            ay = (total / self.length)
            #for k,v in self.forces.items():
                #if self.supports[0] - k < 0:
                    #total -= v * (self.length - k)
                #else:
                    #total += v * (self.length - k)
            #ay = (total / self.length)
            self.outputs.append(ay)
        elif i == self.end:
            by = 0
            total = 0
            for k,v in self.forces.items():
                total += (k * v)
            by = (total / self.length)
            #for k,v in self.forces.items():
                #if self.supports[1] - k < 0:
                    #total -= v * (self.length - k)
                #else:
                    #total += v * (self.length - k)
            #by = (total / self.length)
            self.outputs.append(by)
        else:
            if len(self.outputs) == 0:
                self.outputs.append(self.forces[i])
            else:
                self.outputs.append(self.forces[i] + self.outputs[-1])


def openGraph():
    global inputtxt
    global left_input
    global right_input
    print(value_inside.get())
    try:
      print(float(left_input.get()),float(right_input.get()),float(inputtxt.get()))
      graph1 = Graph(float(inputtxt.get()), float(left_input.get()), float(right_input.get()))
        #graph1.length = 10
      graph1.add_force(1,2)
      graph1.add_force(1.5,2)
      graph1.add_force(1.5,3)
      graph1.add_force(4.5,4)
      graph1.seperators = sorted(graph1.seperators) 
      graph1.update_forces()
      print(graph1.outputs)
      x = graph1.seperators
      y = graph1.outputs
      # plotting the points 
      plt.plot(x, y, color='black', linestyle='solid', linewidth = 3,
         marker='o', markerfacecolor='red', markersize=5)
      # naming the x axis
      plt.xlabel('x - axis')
      # naming the y axis
      plt.ylabel('y - axis')
      # giving a title to my graph
      plt.title('Beam Display')
      # function to show the plot
      plt.show()
    except:
      print("Invalid Inputs, Try again.") 

    

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





