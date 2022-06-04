import os
from tkinter import *
from tkinter import messagebox
import tkinter
import customtkinter
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import cv2
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pygame import GL_BLUE_SIZE

script_dir = os.path.dirname(__file__)
img1_path = "img/aside.png"
img2_path = "img/bside.png"
addmultiplier = 1
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
      self.total = 0
      self.ay = 0
      self.by = 0
  # adding force to a dictionary as a key:value pair being location:value
  def add_force(self, location, value):
    if location in self.forces:
      self.forces[location] += value
    else:
      self.forces[location] = value
      self.seperators.append(location)
  # adding evenly distributed load
  def add_bi_load(self, location1, location2, value):
      midpoint = (1 / 2) * (location1 + location2)
      #print(midpoint)
      bi_value = value * (location2 - location1)
      self.add_force(midpoint, bi_value)
 # adding an increasing/decreasing distributed load
  def add_tri_load(self, location1, location2, value1, value2):
      midpoint = (1 / 2) * (location1 + location2)
      bi_value = value1 * (location2 - location1)
      self.add_force(midpoint, bi_value)
      midpoint = (2 / 3) * (location2 - location1) + location1
      tri_value = (1 / 2) * (location2 - location1) * (value2 - value1)
      self.add_force(midpoint, tri_value)

  def add_moment(self, location, value):
    if location in self.moments:
      self.moments[location] += value
    else:
      self.moments[location] = value
      self.seperators.append(location)
  # goes through all the forces and returns outputs that are used to display the middle graph
  def update_moments(self):
    for k,v in self.moments.items():
      self.total +=v
  
  def update_forces(self):
    for i in self.seperators:
        if i == self.begin:
            jump = 0
            for k,v in self.forces.items():
                if self.end - k < 0:
                    self.total += v * (abs(self.end - k))
                else:
                    self.total -= v * (self.end - k)
            self.ay = (self.total / (self.end - self.begin))
            print("AY HERE:",self.ay)
            if len(self.outputs) > 0:
              jump = self.outputs[-1] + self.ay
              self.outputs.append(jump)
            else:
              self.outputs.append(self.ay)
        elif i == self.end:

            jump = 0
            for k,v in self.forces.items():
                if self.begin - k < 0:
                    self.total -= v * (abs(self.begin - k))
                else:
                    self.total += v * (self.begin - k)
            self.by = (self.total / (self.end - self.begin))
            print("BY HERE:")
            print(self.by)
            if len(self.outputs) > 0:
              jump = self.outputs[-1] + self.by
              self.outputs.append(jump)
            else:
              self.outputs.append(self.ay)
        else:
            print(self.forces, 'lol')
            print(i,'lol')
            if len(self.outputs) == 0:
                self.outputs.append(self.forces[i])
            else:
                self.outputs.append(self.forces[i] + self.outputs[-1])

  def update_graph(self):
    
    global x,y,fig,axs,graph1,length_input,left_input,right_input,options,current_unit
    # resetting the graph
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    graph1.seperators = sorted(graph1.seperators)
    x = list()
    y = [0,0]
    self.update_forces()
    self.update_moments()
    x += graph1.seperators
    x += graph1.seperators
    x.append(0)
    x.append(float(length_input.get()))
    x = sorted(x)
    # duplicating y for the graph
    y = [0,0]
    for i,v in enumerate(graph1.outputs):
      if i < len(graph1.outputs)-1:
        y.append(v)
        y.append(v) 
    y += [0,0]
    print('axs1 x + y : ',x,y)
    axs[1].plot(x, y, color='gray', linestyle='solid', linewidth = 3,
           marker='o', markerfacecolor='blue', markersize=5)
    for i, j in zip(x, y):
      axs[1].text(i, j+0.5, str(round(j,2)))

    print("after",graph1.seperators,graph1.forces,graph1.outputs)
    fig.suptitle('')
    axs[0].axes.yaxis.set_visible(False)
    axs[0].plot([0,float(length_input.get())],[0,10],color='gray', linestyle='None', linewidth = 3, markerfacecolor='white', markersize=5)
    axs[0].set_title('Load Diagram')
    axs[0].add_patch(Rectangle((0,4),float(length_input.get()),2,color = 'grey'))
    # arrows for each force (not including bi and tri load)
    for key,value in graph1.forces.items():
        if value < 0:
          axs[0].arrow(key,10,0,-4,head_width = 0.1,head_length = 0.3,width = 0.05,color='blue')
        else:
          axs[0].arrow(key,6,0,4,head_width = 0.1,head_length = 0.3,width = 0.05,color='blue')
    img1 = cv2.imread(os.path.join(script_dir,img1_path))
    img2 = cv2.imread(os.path.join(script_dir,img2_path))
    im = OffsetImage(img1,zoom=1)
    a1 = AnnotationBbox(im,(float(left_input.get()),2),frameon=False)
    im2 = OffsetImage(img2,zoom=1)
    a2 = AnnotationBbox(im2,(float(right_input.get())+0.05,2),frameon=False)
    axs[0].add_artist(a1)
    axs[0].add_artist(a2)
    axs[1].plot(x, y, color='gray', linestyle='solid', linewidth = 3,
       marker='o', markerfacecolor='blue', markersize=5)
    for i, j in zip(x, y):
      axs[1].text(i, j+0.5, str(round(j,2)))
    axs[1].set_title("Sheer Diagram")
    axs[1].set_xlabel('Location ('+options[current_unit.get()]+')')
    axs[1].set_ylabel('Force')
    plt.show()

def addForce():
  try:
    global loc1,loc2,mag1,mag2
    graph1.outputs = []
    if mag2 == 0 and loc2 == 0: 
      graph1.add_force(float(loc1.get()),float(mag1.get())*addmultiplier)
    elif mag2 == 0:
      graph1.add_bi_load(float(loc1.get()), float(loc2.get()), float(mag1.get())*addmultiplier)
    else:
      graph1.add_tri_load(float(loc1.get()), float(loc2.get()), float(mag1.get())*addmultiplier,float(mag2.get())*addmultiplier)
    graph1.update_graph()
  except:
    print('Something went wrong when adding a Force...')

def addMoment():
  try:
    global loc1,mag1
    graph1.add_moment(float(loc1.get()),float(mag1.get())*addmultiplier)
  except:
    print('Something went wrong when adding a Moment...')

def cLoad():
  global loc1,mag1
  load_frame = customtkinter.CTkFrame(frame,width=200,height=500,corner_radius=5)
  load_frame.grid(row=5,column=1)
  txt1 = customtkinter.CTkLabel(load_frame,text="Load Location").grid(row=0,column=0)
  loc1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  loc1.grid(row=1,column=0)
  txt2 = customtkinter.CTkLabel(load_frame,text="Load Magnitude").grid(row=0,column=2)
  mag1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  button1 = customtkinter.CTkButton(master=load_frame,text="Add To Graph", command=addForce, fg_color="#119149", hover_color="#45ba78").grid(row=2,column=1,pady=(20,10))
  mag1.grid(row=1,column=2)

def uLoad():
  global loc1,loc2,mag1
  load_frame = customtkinter.CTkFrame(frame,width=200,height=500,corner_radius=5)
  load_frame.grid(row=5,column=1)
  txt1 = customtkinter.CTkLabel(load_frame,text="Load Start Location").grid(row=0,column=0)
  loc1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  loc1.grid(row=1,column=0)
  txt2 = customtkinter.CTkLabel(load_frame,text="Load End Location").grid(row=0,column=2)
  loc2 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  loc2.grid(row=1,column=2)
  txt3 = customtkinter.CTkLabel(load_frame,text="Load Magnitude").grid(row=2,column=1)
  mag1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  mag1.grid(row=3,column=1)
  button1 = customtkinter.CTkButton(master=load_frame,text="Add To Graph", command=addForce, fg_color="#119149", hover_color="#45ba78").grid(row=4,column=1,pady=(20,10))

def lLoad():
  global loc1,loc2,mag1,mag2
  load_frame = customtkinter.CTkFrame(frame,width=200,height=500,corner_radius=5)
  load_frame.grid(row=5,column=1)
  txt1 = customtkinter.CTkLabel(load_frame,text="Load Start Location").grid(row=0,column=0)
  loc1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  loc1.grid(row=1,column=0)
  txt2 = customtkinter.CTkLabel(load_frame,text="Load End Location").grid(row=0,column=2)
  loc2 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  loc2.grid(row=1,column=2)
  txt3 = customtkinter.CTkLabel(load_frame,text="Load Start Magnitude").grid(row=2,column=0)
  mag1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  mag1.grid(row=3,column=0)
  txt4 = customtkinter.CTkLabel(load_frame,text="Load End Magnitude").grid(row=2,column=2)
  mag2 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  mag2.grid(row=3,column=2)
  button1 = customtkinter.CTkButton(master=load_frame,text="Add To Graph", command=addForce, fg_color="#119149", hover_color="#45ba78").grid(row=4,column=1,pady=(20,10))

def cMoment():
  load_frame = customtkinter.CTkFrame(frame,width=200,height=500,corner_radius=5)
  load_frame.grid(row=5,column=1)
  txt1 = customtkinter.CTkLabel(load_frame,text="Load Location").grid(row=0,column=0)
  loc1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  loc1.grid(row=1,column=0)
  txt2 = customtkinter.CTkLabel(load_frame,text="Load Magnitude").grid(row=0,column=2)
  mag1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  button1 = customtkinter.CTkButton(master=load_frame,text="Add To Graph", command=addMoment, fg_color="#119149", hover_color="#45ba78").grid(row=2,column=1,pady=(20,10))
  mag1.grid(row=1,column=2)

def cLoadUp():
  global addmultiplier
  addmultiplier = 1
  cLoad()

def cLoadDown():
  global addmultiplier
  addmultiplier = -1
  cLoad()

def uLoadUp():
  global addmultiplier
  addmultiplier = 1
  uLoad()

def uLoadDown():
  global addmultiplier
  addmultiplier = -1
  uLoad()

def lLoadUp():
  global addmultiplier
  addmultiplier = 1
  lLoad()

def lLoadDown():
  global addmultiplier
  addmultiplier = -1
  lLoad()

def cMomentCounter():
  global addmultiplier
  addmultiplier = -1
  cMoment()

def cMomentClock():
  global addmultiplier
  addmultiplier = -1
  cMoment()

# initialize graph
loc1 = 0
loc2 = 0
mag1 = 0
mag2 = 0
plt.style.use('dark_background')
# 3 graphs with matplotlib in the same window
fig, axs = plt.subplots(3,figsize=(12, 8))
x = list()
y = [0,0]
cleared = False

def openGraph():
    global length_input
    global left_input
    global right_input
    try:
      # using input values for graph class
      global graph1
      graph1 = Graph(float(length_input.get()), float(left_input.get()), float(right_input.get()))
    except:
      messagebox.showerror('Type Error', 'Error: Input values are not real numbers.')
    else:
      # all possible invalid input errors
      if float(length_input.get()) < 0 or float(left_input.get()) < 0 or float(right_input.get()) < 0:
        messagebox.showerror('Sign Error', 'Error: Input values cannot be negative numbers')
      elif float(left_input.get()) >= float(right_input.get()):
        messagebox.showerror('Supports Error', 'Error: Left support cannot be greater than or equal to the right one.')
      elif float(right_input.get()) > float(length_input.get()):
        messagebox.showerror('Supports/Length Mismatch', 'Error: Right support cannot be greater than the length of beam.')
      elif float(length_input.get()) == 0:
        messagebox.showerror('Length Error', 'Error: Length of beam cannot be zero.')
      else:
        buttons_frame = customtkinter.CTkFrame(frame,width=200,height=300,corner_radius=0)
        buttons_frame.grid(row=5,column=0)
        button1 = customtkinter.CTkButton(master=buttons_frame,text="Concetrated Load Up", command=cLoadUp, fg_color="#D35B58", hover_color="#C77C78").grid(row=0,column=0,pady=(20,10))
        button2 = customtkinter.CTkButton(master=buttons_frame,text="Concetrated Load Down", command=cLoadDown, fg_color="#D35B58", hover_color="#C77C78").grid(row=1,column=0,pady=(20,10))
        button3 = customtkinter.CTkButton(master=buttons_frame,text="Uniform Load Up", command=uLoadUp, fg_color="#D35B58", hover_color="#C77C78").grid(row=2,column=0,pady=(20,10))
        button4 = customtkinter.CTkButton(master=buttons_frame,text="Uniform Load Down", command=uLoadDown, fg_color="#D35B58", hover_color="#C77C78").grid(row=3,column=0,pady=(20,10))
        button5 = customtkinter.CTkButton(master=buttons_frame,text="Linear Load Up", command=lLoadUp, fg_color="#D35B58", hover_color="#C77C78").grid(row=4,column=0,pady=(20,10))
        button6 = customtkinter.CTkButton(master=buttons_frame,text="Linear Load Down", command=lLoadDown, fg_color="#D35B58", hover_color="#C77C78").grid(row=5,column=0,pady=(20,10))
        button7 = customtkinter.CTkButton(master=buttons_frame,text="Concetrated Moment CCW", command=cMomentCounter, fg_color="#D35B58", hover_color="#C77C78").grid(row=6,column=0,pady=(20,10))
        button8 = customtkinter.CTkButton(master=buttons_frame,text="Concetrated Moment CW", command=cMomentClock, fg_color="#D35B58", hover_color="#C77C78").grid(row=7,column=0,pady=(20,10))
        #graph1.add_force(3,3)
        #graph1.add_bi_load(1,4,6)
        #graph1.add_tri_load(3.5,4.5,2,1)
        #graph1.add_moment(2,1)
        graph1.update_graph()
        
        # plotting the points 
        plt.tight_layout()
        # function to show the plot
        plt.show()
        
# function used to switch between radio buttons and edit the current_unit variable
def switch_unit():
  print("toggled to ", current_unit.get())
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.geometry('600x650')
window.title("Determinate Beam Calculator")
#window.config(background='white')
#window.state('zoomed')
window.resizable(True,True)
frame = customtkinter.CTkFrame(master=window,width=200,height=200,corner_radius=10)
frame.pack(side=TOP,pady=(10,0))
title = customtkinter.CTkLabel(frame,text="Beam Length").grid(row=0,column=0)
length_input = customtkinter.CTkEntry(master=frame, placeholder_text = "0.0")
length_input.grid(row=1,column=0)
label1 = customtkinter.CTkLabel(frame,text="Left Support").grid(row=2,column=0)
left_input = customtkinter.CTkEntry(frame, placeholder_text = "0.0")
left_input.grid(row=3,column=0)
label1 = customtkinter.CTkLabel(frame,text="Right Support").grid(row=2,column=2)
right_input = customtkinter.CTkEntry(frame, placeholder_text = "0.0")
right_input.grid(row=3,column=2)

button = customtkinter.CTkButton(master=frame,text="Submit", command=openGraph).grid(row=4,column=1)
current_unit = tkinter.IntVar(value = 0)
  
# Set the default value of the variable
options = ["in", "ft", "m", "mm"]
options_frame = customtkinter.CTkFrame(frame,width=100,height=30,corner_radius=0)
options_frame.grid(row=1,column=1)
option1 = customtkinter.CTkRadioButton(options_frame,text="in",command=switch_unit, variable= current_unit, value=0).grid(row=0,column=0,padx=10)
option2 = customtkinter.CTkRadioButton(options_frame,text="ft",command=switch_unit, variable= current_unit, value=1).grid(row=0,column=1,padx=10)
option3 = customtkinter.CTkRadioButton(options_frame,text="m",command=switch_unit, variable= current_unit, value=2).grid(row=0,column=2,padx=10)
option4 = customtkinter.CTkRadioButton(options_frame,text="mm",command=switch_unit, variable= current_unit, value=3).grid(row=0,column=3,padx=10)

window.mainloop()





