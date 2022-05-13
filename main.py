from tkinter import *

# Python program for implementation of heap Sort
  
# To heapify subtree rooted at index i.
# n is size of heap
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2
  
    # See if left child of root exists and is
    # greater than root
    if l < n and arr[i] < arr[l]:
        largest = l
  
    # See if right child of root exists and is
    # greater than root
    if r < n and arr[largest] < arr[r]:
        largest = r
  
    # Change root, if needed
    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i]  # swap
  
        # Heapify the root.
        heapify(arr, n, largest)
  
# The main function to sort an array of given size
def heapSort(arr):
    n = len(arr)
  
    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
  
    # One by one extract elements
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]   # swap
        heapify(arr, i, 0)
  

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
    self.seperators = heapSort(self.seperators)
    print(self.seperators)
    for i in heapSort(self.seperators):
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
    graph1 = Graph(10, 2, 6)
    #graph1.length = 10
    graph1.add_force(1,2)
    graph1.add_force(1.5,3)
    graph1.add_force(4.5,4)
    graph1.update_forces()
    print(graph1.outputs)
    window.after(1000, task)  # reschedule event in 2 seconds

window.after(2000, task)



window.mainloop()
# testing





