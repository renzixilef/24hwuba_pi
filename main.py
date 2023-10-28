import tkinter as tk
from tkinter import ttk
from threading import Thread
from datetime import datetime
from flask import Flask

global timer_placement
global current_happy_hour


def get_timedelta(end_time):
    time_left = (end_time - datetime.now()).total_seconds()
    hours_left = int(time_left/3600)
    minutes_left = int((time_left%3600)/60)
    seconds_left = int(((time_left%3600)%60))
    time_left_string = f"{hours_left:0>{2}}:{minutes_left:0>{2}}:{seconds_left:0>{2}}"
    return time_left_string

def update_happy_hour(end_time):
    current_happy_hour.configure(text=get_timedelta(end_time))
    wuba_timer.after(500, update_happy_hour, end_time)

def update():
    main_timer.configure(text=get_timedelta(datetime(2023, 11, 1, 12, 0, 0, 0)))
    timer_update = wuba_timer.after(500, update, datetime(2023, 11, 1, 12, 0, 0, 0))

def replace():
    main_timer.place(relx=0.5, rely=0.5, anchor="center")


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
    timer_placement = wuba_timer.after(3600*1000, replace)
    end_time = datetime.now() + datetime.timedelta(hours=1)
    current_happy_hour = tk.Label(wuba_timer, text=get_timedelta(end_time))
    current_happy_hour.place(relx=0.5, rely=0.2, anchor="center")
    wuba_timer.after(500, update_happy_hour, end_time)
    return "super",201

@webserver.route('/end_happy_hour/', methods=['PUT'])
def end_happy_hour():
    wuba_timer.after_cancel(replace)
    main_timer.place(relx=0.5, rely=0.5, anchor="center")
    



#create Timer-GUI
wuba_timer = tk.Tk()
wuba_timer.geometry("1000x1000")
#wuba_timer.attributes("-fullscreen", True)
wuba_timer["bg"] = "black"
main_timer = tk.Label(wuba_timer, text=get_timedelta(datetime(2023, 11, 1, 12, 0, 0, 0)), font=("Verve", 100), fg="white", bg="black")
main_timer.place(relx=0.5, rely=0.5, anchor="center")
timer_update = wuba_timer.after(500, update)
wuba_timer.mainloop()