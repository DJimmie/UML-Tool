
# coding: utf-8

# # Dependancies

# In[ ]:


import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
##import matplotlib
##import matplotlib.pyplot as plt

import re
import sqlite3
import os
import sys
import shutil
import subprocess
import time

try:
    import tkinter.ttk
    from tkinter import *
except:
    from tkinter import *

from tkinter import messagebox
from tkinter import filedialog

from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk

# # Classes


class UserInterface():
    """Parent class for the UI. Instantiates the composit Window"""
    def __init__(self):
        UI(None)
        mainloop()


class UI(Tk):
    """User Interface with fields for entering a new CSP item to the database. 
    Also, when the UI is launched, the UID and username is retrieved."""
    
    now=dt.date.today().strftime('%B %d, %Y')
    time_of_day=dt.datetime.today().strftime('%I:%M:%S %p')
    
    my_test=None
    
    making_packages=False
    
    initialdir=os.getcwd()
    
    def __init__(self,parent,*args,**kargs):
        """Create the UI Window"""
        Tk.__init__(self,parent,*args,**kargs)
        
        self.parent=parent
        self.initialize()
        self.banner=Label(self,text=f'UML Diagrams - {UI.now}',fg='white',bg='blue',font='Ariel 30 bold')
        self.banner.grid(row=0,column=0, columnspan=2)

#         self.uml_txtbox_frame1()
        self.makeumlFields()
#         self.userInstructions()
        
    def initialize(self):
        """Set-up and configure the UI window"""
        self.title('UML Project')
        the_window_width=self.winfo_screenwidth()
        the_window_height=self.winfo_screenheight()
#         self.configure(width=the_window_width,height=the_window_height)
#         the_window_width=1200
#         the_window_height=700
        self.geometry(f'{the_window_width}x{the_window_height}+0+0')
#         self.attributes('-fullscreen', True)
        self['borderwidth']=4
        self['bg']='blue'
        self.menubar=Menu(self)
        self.menubar.add_command(label="Exit",font='ariel',command=self.bye_bye)
        self.config(menu=self.menubar)
    
    def bye_bye(self):
        """Close the UI Window on menu Exit"""
        self.destroy()
        
    def makeumlFields(self):
        """Generate the CSP fields"""
        # make the frame
        self.uml_txtbox_frame=Frame(self.parent)
        self.uml_txtbox_frame['background']='green'
        self.uml_txtbox_frame['relief']='raised'
        self.uml_txtbox_frame['borderwidth']=10
        self.uml_txtbox_frame.grid(row=1,column=1)
        banner_text='PlantUML Code Here'
        frame_banner=Label(self.uml_txtbox_frame,text=banner_text,fg='white',bg='green',font='Ariel 15 bold')
        frame_banner.grid(row=0,column=0,columnspan=5,pady=15)
        self.v1=StringVar()
        self.uml_txt_file=Entry(self.uml_txtbox_frame,bg='yellow',font='Ariel 15 bold',width=30,textvariable=self.v1)
        self.uml_txt_file.grid(row=3,column=0,sticky=E)
        
        
        
        self.txt='COMMENTS'
        self.uml_txt_label=Label(self.uml_txtbox_frame,text=self.txt,bg='blue',fg='yellow',font='Ariel 12 bold')
        font='Ariel 14 bold'
        self.uml_txt=Text(self.uml_txtbox_frame,borderwidth=2,height=30,width=60,font=font,wrap=WORD)
        self.uml_txt.insert(INSERT, "@startuml\n\n\n@enduml")
        self.uml_txt.tag_add("here", "1.0", "1.4")
        self.uml_txt.tag_config("here", background="yellow", foreground="blue")
        self.uml_txt_label.grid(row=1,column=0,columnspan=1,pady=1,sticky=W)
        self.uml_txt.grid(row=2,column=0,columnspan=1,pady=1,sticky=W)
        
        
        # Buttons
        self.submit_button=Button(self.uml_txtbox_frame, text="SUBMIT UML Code",bg='black',fg='white',relief='raised',command=self.save_txt_file)
        self.submit_button.grid(row=3,column=0,sticky=W)

        self.run_uml=Button(self.uml_txtbox_frame, text="RUN UML Code",bg='black',fg='yellow',relief='raised',state='normal',command=self.getUMLCode)
        self.run_uml.grid(row=4,column=0,sticky=W,pady=15)

        self.access_dir=Button(self.uml_txtbox_frame, text="Open Directory",bg='blue',fg='yellow',relief='raised',state='normal',command=self.open_directory)
        self.access_dir.grid(row=5,column=0,sticky=W,pady=15)
        
        self.get_package=Button(self.uml_txtbox_frame, text="Get Package",bg='yellow',fg='blue',relief='raised',state='normal',command=self.open_packages)
        self.get_package.grid(row=6,column=0,sticky=E,pady=15)
        
    
    def getUMLCode(self):
        
        plantumlcode=self.uml_txt.get("1.0","end-1c")
    #         print(plantumlcode)

        makeRunFile(plantumlcode)

        runUmlFile()
        
        self.ImageUML()
        
        self.getImage()
        
        
    def ImageUML(self):
    
        """Display image of the UML diagram if available"""

        #Create Frame---------------------------------------------------------------
        self.imageFrame=Frame(self.parent)
        self.imageFrame['background']='red'
        self.imageFrame['relief']='sunken'
        self.imageFrame['borderwidth']=9
        self.imageFrame.grid(row=1,column=2,sticky=N,padx=0)
        banner_text='UML Diagram'
        self.imageFrame_banner=Label(self.imageFrame,text=banner_text,fg='white',bg='black',font='Ariel 15 bold')
        self.imageFrame_banner.grid(row=0,column=0,sticky=N)

            
    def getImage(self):
        

        self.the_image_path='uml_run.png'

        try:
            load = Image.open(self.the_image_path)
            render = PIL.ImageTk.PhotoImage(load)
        except:
            load = Image.open("No_Image.png")
            render = PIL.ImageTk.PhotoImage(load)
            

        hgt=render.height()
        wth=render.width()
        
        hgt=800
        wth=1000
        
        img_ref=Label(image=render)
        img_ref.image=render
        
        canvas = Canvas(self.imageFrame, width=wth, height=hgt,bg='blue')
        
#         image_canvas=Frame(canvas)
        
        hbar=Scrollbar(self.imageFrame,orient=HORIZONTAL)
        hbar.config(command=canvas.xview)
        hbar.grid(row=3,column=0,sticky='we')
        
        vbar=Scrollbar(self.imageFrame,orient=VERTICAL)
        vbar.config(command=canvas.yview)
        vbar.grid(row=2,column=1,sticky='ns')
        
        
#         canvas.config(width=600,height=600)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.grid(row=2,column=0,sticky=W)

        canvas.create_image((0,0),image=img_ref.image,anchor=NW)
        
        canvas.config(scrollregion=canvas.bbox('all'))
    
    
    def save_txt_file(self):
        
        file_name=self.v1.get()
        plantumlcode=self.uml_txt.get("1.0","end-1c")
        if (file_name==''):
            messagebox.showwarning(title='FILE NAME REQUIRED',message='FILE NAME REQUIRED')
            return None
        else:
            f= open(f'{UI.initialdir}{file_name}.txt',"w+")
            print(f'UI.initialdir{file_name}.txt')
            f.write(plantumlcode)
            f.close
            
        shutil.copy2(self.the_image_path,f'{UI.initialdir}{file_name}.png')
        
    def plantumlrunerror(self):
        
        messagebox.showwarning(title='RUN ERROR',message='RUN ERROR. VERIFY YOUR CODE')
    
    
    def open_directory(self):
        """Opens the directory folder for user to access"""
        
        UI.making_packages=False
        
        x=filedialog.askopenfilename(initialdir = UI.initialdir,title = "Directory",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
        
        print(x)
        
        self.set_directory(x)
        
        self.uml_txt.delete(1.0, END)
        
        f= open(x,"r")
    
        for line in f:
            self.uml_txt.insert(INSERT, line)
        
        f.close
        
        the_file_name=x.split(sep='/')[-1].split('.')[0]
        self.v1.set(the_file_name)
        
        
    def set_directory(self,selectedFile):
        """Changes the initialdir for the filedialog window and uses the same directory for files saved."""
        
        filename=selectedFile.split(sep='/')[-1]
        
        the_dir=selectedFile.split(sep=filename)
        
        UI.initialdir=the_dir[0]
        
        
    def open_packages(self):
        
        x=filedialog.askopenfilename(initialdir = UI.initialdir,title = "Package Directory",filetypes = (("package files","package*"),("all files","*.*")))
        print(x)
        
        if (UI.making_packages==False):
            self.uml_txt.delete(2.0, END)
            UI.making_packages=True
                                                         
        f= open(x,"r")
    
        for line in f:
            a=line.strip()
            if (a!='@startuml' and a!='@enduml'):
                self.uml_txt.insert(INSERT, line)
#                 print(line,len(line))
        
        f.close
        

# # Functions


def makeRunFile(code):
    
    f= open("uml_run.txt","w+")
    
    f.write(code)
    
    f.close


def runUmlFile():
    
    try:
        subprocess.run('python -m plantuml uml_run.txt',shell=True)
    except:
        UI.plantumlrunerror()
        
    
#     displayUML()



def displayUML():
    
    os.startfile("uml_run.png",operation='open')


#
# # Main


if __name__ == '__main__':
    UserInterface()


