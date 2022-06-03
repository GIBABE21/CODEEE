import os
from tkinter import *
from tkinter import messagebox
import tkinter
import customtkinter
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import cv2
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

script_dir = os.path.dirname(__file__)
img1_path = "img/aside.png"
img2_path = "img/bside.png"

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
      #self.ay_total = 0
      #self.by_total = 0
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
      #print(bi_value)
      #self.add_force(location1, value)
      #self.add_force(location2, value)
      self.add_force(midpoint, bi_value)
 # adding an increasing/decreasing distributed load
  def add_tri_load(self, location1, location2, value1, value2):
      midpoint = (1 / 2) * (location1 + location2)
      #print(midpoint)
      bi_value = value1 * (location2 - location1)
      #print(bi_value)
      self.add_force(midpoint, bi_value)
      midpoint = (2 / 3) * (location2 - location1) + location1
      #print(midpoint)
      tri_value = (1 / 2) * (location2 - location1) * (value2 - value1)
      #print(tri_value)
      self.add_force(midpoint, tri_value)
      #self.add_force(location1, value1)
      #self.add_force(location2, value2)

  def add_moment(self, location, value):
    if location in self.moments:
      self.moments[location] += value
    else:
      self.moments[location] = value
      self.seperators.append(location)
  # goes through all the forces and returns outputs that are used to display the middle graph

  def update_moments(self):
    for k,v in self.moments.items():
      #self.ay_total += v
      #self.by_total += v
      self.total +=v

  def update_forces(self):
    for i in self.seperators:
        if i == self.begin:
            #ay = 0
            #total = 0
            jump = 0
            for k,v in self.forces.items():
                if self.end - k < 0:
                    #total += v * (abs(self.end - k))
                    #self.ay_total += v * (abs(self.end - k))
                    self.total += v * (abs(self.end - k))
                else:
                    #total -= v * (self.end - k)
                    #self.ay_total -= v * (self.end - k)
                    self.total -= v * (self.end - k)
            #ay = (total / (self.end - self.begin))
            #self.ay = (total / (self.end - self.begin))
            #self.ay = (self.ay_total / (self.end - self.begin))
            self.ay = (self.total / (self.end - self.begin))
            print("AY HERE:")
            print(self.ay)
            #print(ay)
            if len(self.outputs) > 0:
              #jump = self.outputs[-1] + ay
              jump = self.outputs[-1] + self.ay
              self.outputs.append(jump)
            else:
              #self.outputs.append(ay)
              self.outputs.append(self.ay)
        elif i == self.end:
            #by = 0
            #total = 0
            jump = 0
            for k,v in self.forces.items():
                if self.begin - k < 0:
                    #total -= v * (abs(self.begin - k))
                    #self.by_total -= v * (abs(self.begin - k))
                    self.total -= v * (abs(self.begin - k))
                else:
                    #total += v * (self.begin - k)
                    #self.by_total += v * (self.begin - k)
                    self.total += v * (self.begin - k)
            #by = (total / (self.end - self.begin))
            #self.by = (total / (self.end - self.begin))
            #self.by = (self.by_total / (self.end - self.begin))
            self.by = (self.total / (self.end - self.begin))
            print("BY HERE:")
            print(self.by)
            #print(by)
            if len(self.outputs) > 0:
              #jump = self.outputs[-1] + by
              jump = self.outputs[-1] + self.by
              self.outputs.append(jump)
            else:
              #self.outputs.append(ay)
              self.outputs.append(self.ay)
        else:
            print(self.forces, 'lol')
            print(i,'lol')
            if len(self.outputs) == 0:
                self.outputs.append(self.forces[i])
            else:
                self.outputs.append(self.forces[i] + self.outputs[-1])
addmultiplier = 1
def cLoadUp():
  global load_frame, txt1,txt2,inp1,inp2
  load_frame = customtkinter.CTkFrame(frame,width=200,height=500,corner_radius=5)
  load_frame.grid(row=5,column=1)
  txt1 = customtkinter.CTkLabel(load_frame,text="Moment Location").grid(row=0,column=0)
  inp1 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  inp1.grid(row=1,column=0)
  txt2 = customtkinter.CTkLabel(load_frame,text="Moment Magnitude").grid(row=0,column=2)
  inp2 = customtkinter.CTkEntry(load_frame, placeholder_text = "0.0")
  button1 = customtkinter.CTkButton(master=load_frame,text="Add To Graph", command=addToGraph, fg_color="#119149", hover_color="#45ba78").grid(row=2,column=1,pady=(20,10))
  inp2.grid(row=1,column=2)

def cLoadDown():
  global addmultiplier
  addmultiplier = -1
  cLoadUp()


def uLoadUp():
  print('u load up')
def uLoadDown():
  print('u load down')
def lLoadUp():
  print('new force5')
def lLoadDown():
  print('new force6')
def cMomentCounter():
  print('new force7')
def cMomentClock():
  print('new force8')

def addToGraph():
  #try:
  graph1.outputs = []
  graph1.add_force(float(inp1.get()),float(inp2.get())*addmultiplier)
  graph1.seperators = sorted(graph1.seperators) 
  print(graph1.seperators,graph1.forces,graph1.outputs)
  graph1.update_forces()
  #except:
  #print('error')
# 10 2 6
def openGraph():
    global length_input
    global left_input
    global right_input
    #print(value_inside.get())
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
        global button1,button2,button3,button4,button5,button6,button7,button8
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
        print(button1)
        #graph1.add_force(0,0)
        #graph1.add_force(1,4)
        #graph1.add_force(2,6)
        #graph1.add_force(4.5,-4)
        #graph1.add_force(8,10)
        #graph1.add_force(9.5,1)
        #graph1.add_bi_load(1,4,6)
        #graph1.add_force(2.5,18)
        #graph1.add_tri_load(2,4,1,2)
        #graph1.add_tri_load(3.5,4.5,2,1)
        graph1.add_moment(2,1)
        graph1.seperators = sorted(graph1.seperators) 
        graph1.update_moments()
        graph1.update_forces()

        # duplicating x for the graph
        x = list()
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
        print(x)
        print(y)
        plt.style.use('dark_background')
        # 3 graphs with matplotlib in the same window
        fig, axs = plt.subplots(3,figsize=(12, 8))
        fig.suptitle('')
        axs[0].axes.yaxis.set_visible(False)
        axs[0].plot([0,float(length_input.get())],[0,10],color='gray', linestyle='None', linewidth = 3, markerfacecolor='white', markersize=5)
        axs[0].set_title('Load Diagram')
        axs[0].add_patch(Rectangle((0,4),float(length_input.get()),2,color = 'grey'))
        for key,value in graph1.forces.items():
            if value < 0:
              axs[0].arrow(key,10,0,-4,head_width = 0.1,head_length = 0.3,width = 0.05,color='blue')
            else:
              axs[0].arrow(key,6,0,4,head_width = 0.1,head_length = 0.3,width = 0.05,color='blue')
        print(graph1.seperators,'bruh')
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
#window.config(background='black')
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
#current_unit.set("in")
options = ["in", "ft", "m", "mm"]
options_frame = customtkinter.CTkFrame(frame,width=100,height=30,corner_radius=0)
options_frame.grid(row=1,column=1)
option1 = customtkinter.CTkRadioButton(options_frame,text="in",command=switch_unit, variable= current_unit, value=0).grid(row=0,column=0,padx=10)
option2 = customtkinter.CTkRadioButton(options_frame,text="ft",command=switch_unit, variable= current_unit, value=1).grid(row=0,column=1,padx=10)
option3 = customtkinter.CTkRadioButton(options_frame,text="m",command=switch_unit, variable= current_unit, value=2).grid(row=0,column=2,padx=10)
option4 = customtkinter.CTkRadioButton(options_frame,text="mm",command=switch_unit, variable= current_unit, value=3).grid(row=0,column=3,padx=10)
#def task():
    
    #print(graph1.outputs)
#   window.after(1000, task)  # reschedule event in 2 seconds

#window.after(2000, task)



window.mainloop()
# testing





