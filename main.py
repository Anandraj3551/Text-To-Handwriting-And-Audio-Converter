from turtle import bgcolor
from PIL import ImageTk
import PIL.Image
import tkinter as tk
import pywhatkit as kit
from tkinter import *
from tkinter import colorchooser
from tkinter.ttk import Progressbar
import time
import datetime
from threading import *
from pathlib import Path
import os
from tkinter import filedialog
from tkinter.ttk import Combobox
import os
import pyttsx3
repn = Path('results')
if repn.is_dir():
    pass
else:
    os.mkdir('results')

root = Tk()
root.title("Text To Handwritten and Audio")
width1  = root.winfo_screenwidth()
height1 = root.winfo_screenheight()
root.geometry(f'{width1}x{height1}')
root.configure(bg="black")
color_result_rgb = [0,0,0]
engine = pyttsx3.init()
def speaknow():
    text1 = txt2.get(1.0,END)
    gender = gen_Combo.get()
    speed = speed_combo.get()
    voices = engine.getProperty("voices")
    def setvoice():
        if(gender == "Male"):
            engine.setProperty("voice",voices[0].id)
            engine.say(text1)
            engine.runAndWait()
        else:
            engine.setProperty("voice",voices[1].id)
            engine.say(text1)
            engine.runAndWait()
    if(text1):
        if(speed =="Fast"):
            engine.setProperty("rate",250)
            setvoice()
        elif(speed =="Normal"):
            engine.setProperty("rate",150)
            setvoice()
        else:
            engine.setProperty("rate",70)
            setvoice()
            
def download():
    text1 = txt2.get(1.0,END)
    gender = gen_Combo.get()
    speed = speed_combo.get()
    voices = engine.getProperty("voices")
    def setvoice():
        if(gender == "Male"):
            engine.setProperty("voice",voices[0].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text1,"text.mp3")
            engine.runAndWait()
        else:
            engine.setProperty("voice",voices[1].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text1,"text.mp3")
            engine.runAndWait()
    if(text1):
        if(speed =="Fast"):
            engine.setProperty("rate",250)
            setvoice()
        
        elif(speed =="Normal"):
            engine.setProperty("rate",150)
            setvoice()
        else:
            engine.setProperty("rate",70)
            setvoice()

def threading():
    t1=Thread(target=convert_txt_to_HW)
    t1.start()
def convert_txt_to_HW():
    text = txt2.get("1.0",END)
    ts = time.time()
    dat = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStam = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStam.split(":")
    fileN = "./results/" + dat + "_" + Hour + "-" + Minute + "-" + Second + ".png"
    img_txt = kit.text_to_handwriting(text,fileN,rgb = color_result_rgb)

    def bar():
        progress['value'] = 100
        root.update_idletasks()
        progress.destroy()

    progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
    progress.place(x=770, y=652)
    bar()

    conv_text_lbl.config(text="Handwritten Text", width=15, height=2, fg="gold", bg="black", font=('segou UI', 16, ' bold'))
    conv_text_lbl.place(x=990, y=100)

    im2 = PIL.Image.open(fileN)
    im2 = im2.resize((887, 402), PIL.Image.ANTIALIAS)
    sp_img2 = ImageTk.PhotoImage(im2)
    panel6.config(image=sp_img2)
    panel6.image = sp_img2
    panel6.pack()
    panel6.place(x=1005, y=155)

def destroy_widget(widget):
    widget.destroy()

def clear_txt():
    txt2.delete("1.0",END)

def color_choose():
    global color_result_rgb
    color_code = colorchooser.askcolor(title ="Choose color")
    color_result_rgb = ' '.join(str(int(x)) for x in color_code[0])
    color_result_rgb = color_result_rgb.split(' ')
    color_tup = [int(item) for item in color_result_rgb]
    color_tup = tuple(color_tup)
    print(color_tup)
    colordis_lbl.configure(bg = _from_rgb(color_tup))
    colordis_lbl.place(x=680, y=652)

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb
image_icon = PhotoImage(file ="assets/speak.png")
root.iconphoto(False,image_icon)

Top_frame = Frame(root, bg="black", width=width1, height=100)
Top_frame.place(x=0,y=0)
Logo1 = PhotoImage(file ="assets/speaker logo.png")
Label(Top_frame,image = Logo1, bg= "black").place(x=10,y=5)

im1 = PIL.Image.open('assets/writing.png')
im1 =im1.resize((120,100), PIL.Image.LANCZOS)
sp_img = ImageTk.PhotoImage(im1)
panel5 = Label(root,borderwidth=0, image=sp_img,bg = 'black')
panel5.pack()
panel5.place(x=1050, y=10)

Label(Top_frame, text= "Text To Handwritten and Audio", font = "arial 40 bold",bg ="black", fg = "gold").place(x=120, y = 30)

enter_text_lbl = tk.Label(root, text="Enter your text", width=15, height=2, fg="gold",bg="black",font=('segou UI', 16, ' bold'))
enter_text_lbl.place(x=30, y=100)

# Text area
txt2_border = Frame(root,borderwidth = 3, background="gold")
txt2 = Text(txt2_border,borderwidth = 1, width=60,height=13, bg='black', fg="gold", font=('times', 20))
txt2.pack()
txt2_border.place(x=30, y=155)

# Convert Text Button
conv_border = Frame(root,borderwidth = 2, background="gold")
conv= Button(conv_border,text='Convert Text',command = threading, bg='black', fg="gold", font=('times', 15, ' bold '),activebackground = "#00FF89")
conv.pack(padx=1, pady=1)
conv_border.place(x=30, y=570)

# Clear Border Buttton
clear_border = Frame(root,borderwidth = 2, background="gold")
clear = Button(clear_border,text='Clear Text',command = clear_txt, bg='black', fg="gold", font=('times', 15, ' bold '),activebackground = "#00FF89")
clear.pack(padx=1, pady=1)
clear_border.place(x=205, y=570)

# Choose Color Button
color_border = Frame(root,borderwidth = 2, background="gold")
color = Button(color_border,text='Choose Color',command = color_choose, bg='black', fg="gold", font=('times', 15, ' bold '),activebackground = "#00FF89")
color.pack(padx=1, pady=1)
color_border.place(x=355, y=570)

# Don't know
colordis_lbl = tk.Label(root, width=6, height=2, fg="#00FF89",bg="green")
panel6 = Label(root,borderwidth=0)
conv_text_lbl = Label(root, text="Enter your text", width=15, height=2, fg="gold",bg="black",font=('times', 15, ' bold'))

# Audio Button
gen_Combo = Combobox(root, values=["Male", "Female"], font="times 20 bold", state="r",width = 10 )
gen_Combo.place(x = 155, y =670 )
gen_Combo.set("Male")

speed_combo = Combobox(root, values=["Fast","Normal","Slow"], font="times 20 bold", state="r",width=10)
speed_combo.place(x= 355,y=670)
speed_combo.set("Normal")

Label(root,text = "Voice",font="times 20 bold", bg ="#305065",fg= "white" ).place(x=155,y=630)
Label(root,text = "Speed",font="times 20 bold", bg ="#305065",fg= "white" ).place(x=355,y=630)

imageicon = PhotoImage(file="assets/speak.png")
btn = Button(root,text="Speak",compound = LEFT, image = imageicon, width=130,font="arial 15 bold", command= speaknow,bg= "gold")
btn.place(x=155,y=750)

imageicon2 = PhotoImage(file="assets/download.png")
btn = Button(root,text="Save",compound = LEFT, image = imageicon2, width=130,font="arial 15 bold", command= download, bg="gold")
btn.place(x=355,y=750)

root.mainloop()