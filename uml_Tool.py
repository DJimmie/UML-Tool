
# coding: utf-8

# # Dependancies


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
import webbrowser

try:
    import tkinter.ttk
    from tkinter import *
except:
    from tkinter import *

from tkinter import messagebox
from tkinter import filedialog

from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk

# import program_work_dir as pwd

from support_pkg import program_work_dir as pwd

import logging

import plantuml

# Create a custom logger
logger = logging.getLogger('GUI')
logger.setLevel(logging.DEBUG)

# logging file handler
f_handler = logging.FileHandler('workflow.log',mode='w')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
f_handler.setLevel(logging.DEBUG)
logger.addHandler(f_handler)


# Create program working folder and its subfolders
config_parameters={'uml_Tool.py':{'Purpose':'UML Tool using the plantuml library'}}
client=pwd.ClientFolder(os.path.basename(__file__),config_parameters)
ini_file=f'c:/my_python_programs/{client}/{client}.ini'
log_file=f'c:/my_python_programs/{client}/{client}_log.log'
uml_txt_file=f'c:/my_python_programs/{client}/{client}.txt'
uml_png_file=f'c:/my_python_programs/{client}/{client}.png'


logging.basicConfig(filename=log_file, level=logging.INFO, filemode='w', format=' %(asctime)s -%(levelname)s - %(message)s')


# # Classes


class UserInterface():
    """Parent class for the UI. Instantiates the composit Window"""
    logging.info('UserInterface()')
    def __init__(self):
        UI(None)
        mainloop()


class UI(Tk):
    """User Interface with fields for entering a new CSP item to the database. 
    Also, when the UI is launched, the UID and username is retrieved."""
    logging.info('UI()')
    
    now=dt.date.today().strftime('%B %d, %Y')
    time_of_day=dt.datetime.today().strftime('%I:%M:%S %p')
    
    my_test=None
    making_packages=False
    diagram_text_list=['list of txt files']
    txt_file_stack=None
    file_select_status=False
    selected_file_to_save=None
    
    # initialdir=os.getcwd()
    initialdir=None
    
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
        logging.info('Exit Program')
        self.destroy()
        
    def makeumlFields(self):
        """Generate the CSP fields"""
        logging.info('UserInterface.makeumlFields')
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
        
        self.uml_txt_file=ttk.Combobox(self.uml_txtbox_frame,font='Ariel 15 bold',width=30,textvariable=self.v1)
        self.uml_txt_file['background']='yellow'
        self.uml_txt_file.grid(row=3,column=0,sticky=E)
        self.uml_txt_file.bind("<<ComboboxSelected>>", lambda x: self.rapid_select(self.v1.get()))

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

        self.make_pdf=Button(self.uml_txtbox_frame, text="Make Pdf",bg='orange',fg='black',relief='raised',state='normal',command=self.pdf_the_diagram)
        self.make_pdf.grid(row=4,column=0,sticky=E,pady=15)

        self.open_pdf=Button(self.uml_txtbox_frame, text="Open\nProject Pdf",bg='blue',fg='yellow',relief='raised',
                             state='disabled',command=self.open_project_pdf)
        self.open_pdf.grid(row=5,column=0,sticky=E,pady=15)

        self.goto_plantuml_site=Button(self.uml_txtbox_frame, text="plantuml.com",bg='white',fg='blue',relief='raised',
                                       state='normal', command=lambda: webbrowser.open('https://plantuml.com/'))
        self.goto_plantuml_site.grid(row=6,column=0,sticky=W,pady=15)
        

   

    def pdf_the_diagram(self):
        logging.info('UI.pdf_the_diagram')

        # save the currently displayed png as a pdf
        file_name=self.v1.get()
        im1=self.load.convert('RGB')
        print(f'{UI.initialdir}\\{file_name}.pdf')
        im1.save(f'{UI.initialdir}\\{file_name}.pdf')

        # search for all pdf documents in the working directory

        l=os.listdir(path=UI.initialdir)
        png_files_only=[]
        for i in l:
            s=os.path.splitext(i)
            if (s[1]=='.png'):
                png_files_only.append(s[0])
        print(png_files_only)

        # loop thru the png list to get the image.open

        image_list=[]
        for j in png_files_only:
            the_png=f'{UI.initialdir}{j}.png'
            print(the_png)
            images = Image.open(the_png)
            image_list.append(images)
            
        # loop thru the image_list to convert
        converted_list=[]
        for k in image_list:
            image_convert_list=k.convert('RGB')
            converted_list.append(image_convert_list)

        # make the pdf book
        self.folder_name=UI.initialdir.split('/')[-2]
        k.save(f'{UI.initialdir}{self.folder_name}.pdf',save_all=True, append_images=converted_list)

        self.open_pdf['state']='normal'
            
##        print(folder_name)
    

    def open_project_pdf(self):
        """Open the pdf book"""
        logging.info('UI.open_project_pdf')


        
        print(f'doogy:{UI.initialdir}{self.folder_name}')
        os.startfile(f'{UI.initialdir}{self.folder_name}.pdf')
        
 

##    @staticmethod
    def rapid_select(self,b):
        """ Selection of txt file and associated diagram via drop down select event binding"""
        logging.info('UI.rapid_select')

        UI.file_select_status=True

        self.show_select_state()
    
        UI.selected_file_to_save=UI.txt_file_stack.pop(0).split(sep='/')[-1].split('.')[0]
        UI.txt_file_stack.append(f'{UI.initialdir}{b}')

##        print(f'pop item that is saved={UI.selected_file_to_save}')
##        print(f'file stack:{UI.txt_file_stack}')

        self.save_txt_file()

        self.uml_txt.delete(1.0, END)
        x=f'{UI.initialdir}\\{b}.txt'
        x=f'{UI.txt_file_stack[0]}.txt'
        f= open(x,"r")
        for line in f:
            self.uml_txt.insert(INSERT, line)
        f.close

        self.getUMLCode()

        UI.file_select_status=False

        self.show_select_state()

    def show_select_state(self):
        """This is a diagnosis function. Remove it when ready"""
##        print(f'the selct state is:{UI.file_select_status}')
        pass


        
    @staticmethod
    def list_of_diagram_files():
        """generate list of the diagram's text files for selection on the GUI"""
        logging.info('UI.list_of_diagram_files')

        l=os.listdir(path=UI.initialdir)
        txt_files_only=[]
        for i in l:
            s=os.path.splitext(i)
            if (s[1]=='.txt'):
                txt_files_only.append(s[0])
        print(txt_files_only)
        
        UI.diagram_text_list=txt_files_only


        
    
    def getUMLCode(self):
        logging.info('UI.getUMLCode')
        
        plantumlcode=self.uml_txt.get("1.0","end-1c")
    #         print(plantumlcode)

        makeRunFile(plantumlcode)

        runUmlFile()
        
        self.ImageUML()
        
        self.getImage()
        
        
    def ImageUML(self):
        """Display image of the UML diagram if available"""
        logging.info('UI.ImageUML')

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
        logging.info('UI.getImage')
        
        self.the_image_path=uml_png_file

        try:
            self.load=load = Image.open(self.the_image_path)
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
        logging.info('UI.save_txt_file')

        if (UI.file_select_status==False):
            self.file_name=file_name=self.v1.get()
            shutil.copy2(self.the_image_path,f'{UI.initialdir}\\{file_name}.png')
        else:
            self.file_name=file_name=UI.selected_file_to_save
            self.load.save(f'{UI.initialdir}\\{file_name}.png')   

        
        plantumlcode=self.uml_txt.get("1.0","end-1c")
        if (file_name==''):
            messagebox.showwarning(title='FILE NAME REQUIRED',message='FILE NAME REQUIRED')
            return None
        else:
            f= open(f'{UI.initialdir}\\{file_name}.txt',"w+")
            print(f' should be saving this file={UI.initialdir}\\{file_name}.txt')
            f.write(plantumlcode)
            f.close
            
        
    def plantumlrunerror(self):
        logging.info('UI.plantumlrunerror')
        
        messagebox.showwarning(title='RUN ERROR',message='RUN ERROR. VERIFY YOUR CODE')
    
    
    def open_directory(self):
        """Opens the directory folder for user to access"""
        logging.info('UI.open_directory')

        self.show_select_state()
        
        UI.making_packages=False

        self.file_select_status=False
        
        x=filedialog.askopenfilename(initialdir = UI.initialdir,title = "Directory",filetypes = (("all files","*.*"),("jpeg files","*.jpg")))
        
##        print(f'x={x}')
        
        logging.info(f'file selected = {x}')

        self.set_directory(x)
        
        self.uml_txt.delete(1.0, END)
        
        f= open(x,"r")
    
        for line in f:
            self.uml_txt.insert(INSERT, line)
        
        f.close
        
        the_file_name=x.split(sep='/')[-1].split('.')[0]
        self.v1.set(the_file_name)

        self.getUMLCode()
        
        UI.txt_file_stack=[]
        UI.txt_file_stack.append(f'{UI.initialdir}\\{the_file_name}.txt')
        
        
    def set_directory(self,selectedFile):
        """Changes the initialdir for the filedialog window and uses the same directory for files saved."""
        logging.info('UI.set_directory')
        
        filename=selectedFile.split(sep='/')[-1]

        logging.info(f'filename is {filename}')
        
        the_dir=selectedFile.split(sep=filename)
        
        UI.initialdir=the_dir[0]

        
##        print(f'mofo dir={UI.initialdir}')

        UI.list_of_diagram_files()
        self.uml_txt_file['values']=UI.diagram_text_list
        
        
    def open_packages(self):
        logging.info('UI.open_packages')
        
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
        

# # Functions------------------Functions----------------------------Functions


def makeRunFile(code):
    logging.info('makeRunFile()')
    
    f= open(uml_txt_file,"w+")
    f.write(code)
    f.close

def runUmlFile():
    logging.info('runUmlFile')

    print('\n'.join(sys.path))
    
    try:
        subprocess.run(f'python -m plantuml {uml_txt_file}',shell=True)
        # plantuml.main(filename=uml_txt_file)

    except:
        UI.plantumlrunerror()
        
    
#     displayUML()



def displayUML():
    logging.info('displayUML')

    os.startfile(uml_png_file,operation='open')


#
# # Main


if __name__ == '__main__':
    logging.info('Start')

    diagrams_folder=pwd.WorkDirectory('diagrams_folder',client_folder=client)

    UI.initialdir=diagrams_folder_path=f'C:\\my_python_programs\\{diagrams_folder.client_folder}\\{diagrams_folder.client_sub_folder}'
    
    UserInterface()


