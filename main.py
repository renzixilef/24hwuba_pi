import tkinter as tk
from tkinter import ttk
from threading import Thread
from datetime import datetime
from datetime import timedelta
from flask import Flask
from PIL import Image, ImageTk

global timer_placement
global current_happy_hour
global wuba_timer 
global current_happy_hour_end_time
current_happy_hour_end_time = None
global happy_hour_timer
wuba_timer = tk.Tk()


def get_timedelta(end_time):
    time_left = (end_time - datetime.now()).total_seconds()
    hours_left = int(time_left/3600)
    minutes_left = int((time_left%3600)/60)
    seconds_left = int(((time_left%3600)%60))
    time_left_string = f"{hours_left:0>{2}}:{minutes_left:0>{2}}:{seconds_left:0>{2}}"
    return time_left_string


def update():
    main_timer.configure(text=get_timedelta(datetime(2023, 11, 1, 12, 0, 0, 0)))
    if current_happy_hour_end_time != None:
        happy_hour_timer.configure(text=get_timedelta(current_happy_hour_end_time))
    wuba_timer.after(500, update)

def replace():
    main_timer.place(relx=0.5, rely=0.5, anchor="center")
    main_timer.configure(font=("Verve", 100))
    current_happy_hour.destroy()
    global current_happy_hour_end_time
    current_happy_hour_end_time = None

def happy_hour_container(end_time):
    container = tk.Frame(wuba_timer, bg="black", )

    tk.Label(container, text="Happy Hour", font=("GFS Didot", 50), fg="white", bg="black").grid(row=0, column=1)

    left_image = ImageTk.PhotoImage(Image.open("Kerze.png").resize((500, 742.8)))
    left_image_label = tk.Label(container, image=left_image, bg="black")
    left_image_label.photo = left_image
    left_image_label.grid(row=0, column=0, rowspan=3)
    
    global happy_hour_timer
    happy_hour_timer = tk.Label(container, text=get_timedelta(end_time), font=("GFS Didot", 80), fg="white", bg="black")
    happy_hour_timer.grid(row=1, column=1)

    tk.Label(container, text="Longdrinks und WuBawasser 1€ billiger!", font=("GFS Didot", 30), fg="white", bg="black").grid(row=2, column=1)

    right_image = ImageTk.PhotoImage(Image.open("Wubawasser.png").resize((500, 742.8)))
    right_image_label = tk.Label(container, image=right_image, bg="black")
    right_image_label.photo = right_image
    right_image_label.grid(row=0, column=2, rowspan=3)

    return container



#create Webserver
webserver = Flask(__name__)
webserver.debug = False
#webserver.run(host="0.0.0.0", port=10000)
webserver_thread = Thread(target=webserver.run, kwargs={'host': "0.0.0.0", 'port': 9873})
webserver_thread.start()

@webserver.route('/start_happy_hour/', methods=['PUT'])
def launch_happy_hour():
    wuba_timer.after_cancel(replace)
    main_timer.place(relx=0.5, rely=0.8, anchor="center")
    main_timer.configure(font=("Verve", 60))
    wuba_timer.after(3600*1000, replace)
    global current_happy_hour_end_time
    current_happy_hour_end_time = datetime.now() + timedelta(hours=1)
    global current_happy_hour
    current_happy_hour.place(relx=0.5, rely=0.5, anchor="center")
    return "super",201

@webserver.route('/end_happy_hour/', methods=['PUT'])
def end_happy_hour():
    if type(current_happy_hour) == tk.Frame:  
        wuba_timer.after_cancel(replace)
        replace()
    return "super",201
    



#create Timer-GUI

# wuba_timer.geometry("1000x1000")
wuba_timer.attributes("-fullscreen", True)
wuba_timer["bg"] = "black"
main_timer = tk.Label(wuba_timer, text=get_timedelta(datetime(2024, 11, 1, 12, 0, 0, 0)), font=("Verve", 100), fg="white", bg="black")
#print(type(main_timer))
main_timer.place(relx=0.5, rely=0.5, anchor="center")
timer_update = wuba_timer.after(500, update)
wuba_timer.mainloop()

