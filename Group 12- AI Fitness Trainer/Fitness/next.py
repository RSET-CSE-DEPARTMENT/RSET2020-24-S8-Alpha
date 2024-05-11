from tkinter import *
import PIL.Image
from PIL import *
import sqlite3
from tkinter.ttk import Progressbar
# from Fingers.hh import loading_window,sign_in_success
from admin import *
from user import *
#from admin1 import *
global password,username
def next():
        global next_window
        next_window= Toplevel(root)
        next_window.title("AI Fitness Trainer")
        next_window.minsize(width=600,height=500)
        next_window.geometry("600x500")

        # Adding a background image
        # background_image =PIL.Image.open("finger.jpg")
        # [imageSizeWidth, imageSizeHeight] = background_image.size

        # img = ImageTk.PhotoImage(background_image)
        Canvas1 = Canvas(next_window)
        # Canvas1.create_image(300,340,image = img)      
        # Canvas1.config(bg="#11262b",width = imageSizeWidth, height = imageSizeHeight)
        Canvas1.config(bg="#11262b",width = 600, height = 500)
        Canvas1.pack(expand=True,fill=BOTH)

        headingFrame1 = Frame(next_window,bg="#FFFFFF",bd=0.5)
        headingFrame1.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)

        headingLabel = Label(headingFrame1, text="AI FITNESS TRAINER", bg='#2b2b2b', fg='white', font=('Comic Sans MS',20,'bold'))
        headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
        def adminPage():
                ## Tries to initialize the fingerprint sensor
                
                        Admin()
                        '''admin_window = None  # Global variable to track admin window instance
                        def open_admin_window():
                            global admin_window

                            if admin_window is None:
                                admin_window = Admin()
                            else:
                                admin_window.focus_set()
                        open_admin_window()'''

        btn2 = Button(next_window,text="Upload Video",bg='#1f69a6', fg='black',command=adminPage)
        btn2.place(relx=0.4,rely=0.4, relwidth=0.2,relheight=0.1)
        btn2 = Button(next_window,text="Upload Video",bg='#1f69a6', fg='black',command=adminPage)
        btn2.place(relx=0.4,rely=0.55, relwidth=0.2,relheight=0.1)

        btn5 = Button(next_window,text="Report",bg='#1f69a6', fg='black',command=userPage)
        btn5.place(relx=0.4,rely=0.7, relwidth=0.2,relheight=0.1)

        next_window.mainloop()
