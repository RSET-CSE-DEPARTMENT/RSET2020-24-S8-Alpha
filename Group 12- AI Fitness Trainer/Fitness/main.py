from tkinter import *
import PIL.Image
from PIL import *
import sqlite3
from tkinter.ttk import Progressbar
# from fcon import loading_window,sign_in_success
from admin import *
from shared import uid
import shared
from user import *
# from next import next
#from admin1 import *
# global password,username,user_id
shared.uid=None
img=None
def next():
        global next_window,img
        next_window= Tk()
        next_window.title("AI Fitness Trainer")
        next_window.minsize(width=600,height=500)
        next_window.geometry("600x500")

        # Adding a background image
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
        btn2 = Button(next_window,text="Video Enhancement",bg='#1f69a6', fg='black',command=adminPage)
        btn2.place(relx=0.4,rely=0.55, relwidth=0.2,relheight=0.1)

        btn5 = Button(next_window,text="Report",bg='#1f69a6', fg='black',command=userPage)
        btn5.place(relx=0.4,rely=0.7, relwidth=0.2,relheight=0.1)

        next_window.mainloop()

def create_database():
    # Create a connection to the database (or open it if it already exists)
    # con = sqlite3.connect(database="SecureVoteX.db")

    # # Create a cursor object to execute SQL commands
    # cursor = con.cursor()

    # # Create tables if they don't exist
    # cursor.execute('''CREATE TABLE IF NOT EXISTS encryptTable (
    #                     encryptid varchar(100) primary key,
    #                     count number
    #                     )''')
    # cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value INTEGER)")
    # cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('voting_enabled', 1)")
    # cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
    #                     uid varchar(30) primary key,
    #                     name varchar(30),
    #                     img varchar(100)
    #                 )''')
    # cursor.execute('''CREATE TABLE IF NOT EXISTS voter (
    #                     uid varchar(30) primary key,
    #                     name varchar(30),
    #                     img varchar(100),
    #                     fid varchar(30) 
    #                 )''')

    # con.commit()
    # con.close()
    con = sqlite3.connect(database="Fitness.db")

    # Create a cursor object to execute SQL commands
    cursor = con.cursor()

    # Create a table to store user information if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                        uid INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')

    con.commit()
    con.close()

# def loading_window():
#     loading_window = Tk()
#     loading_window.title("Loading...")
#     loading_window.geometry("600x500")
#     loading_window.configure(bg="#242424")

#     # Resizing the logo image
#     logo_image = Image.open("Front_load.png")
#     logo_image = logo_image.resize((200, 200), Image.LANCZOS)
#     logo_photo = ImageTk.PhotoImage(logo_image)

#     logo_label = Label(loading_window, image=logo_photo, bg="#242424")
#     logo_label.place(relx=0.51, rely=0.4, anchor=CENTER)

#     # Loading bar
#     progress_var = DoubleVar()
#     progress_bar = Progressbar(loading_window, variable=progress_var, length=300, mode='indeterminate')
#     progress_bar.place(relx=0.5, rely=0.8, anchor=CENTER)

#     def start_loading():
#         for i in range(1, 101):
#             progress_var.set(i)
#             loading_window.update_idletasks()
#             time.sleep(0.03)
#         loading_window.destroy()
#         open_sign_in()

#     # Start the loading process
#     progress_bar.start(7000)  # Change the value inside start() to adjust the speed of the loading bar
#     loading_window.after(1, start_loading)  # Change the value inside after() to adjust the duration before starting the main window
#     loading_window.mainloop()

def open_sign_in():
    global user_id_entry
    # Define the sign-in window
    sign_in_window = Tk()
    sign_in_window.title("Sign In")
    sign_in_window.geometry("400x300")
    sign_in_window.configure(bg="#242424")
    user_id_label = Label(sign_in_window, text="User ID:", bg="#242424", fg="white")
    user_id_label.pack()

    user_id_entry = Entry(sign_in_window)
    user_id_entry.pack()

    # Create sign-in widgets
    username_label = Label(sign_in_window, text="Username:", bg="#242424", fg="white")
    username_label.pack()
    username_entry = Entry(sign_in_window)
    username_entry.pack()

    password_label = Label(sign_in_window, text="Password:", bg="#242424", fg="white")
    password_label.pack()
    password_entry = Entry(sign_in_window, show="*")
    password_entry.pack()

    # Define sign-in function
    def sign_in():
        global sign_in_success
        correct_username = "admin"
        correct_password = "password"
        user_id = user_id_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        try:
            con = sqlite3.connect("Fitness.db")
            cursor = con.cursor()
            print("e")
            cursor.execute("SELECT password FROM user WHERE uid=?", (user_id))
            stored_password_row = cursor.fetchone()
            print("P")
            if stored_password_row is not None:
                stored_password = stored_password_row[0]  # Extract the password from the fetched row
                if stored_password == password:
                    # print(stored_password,password)
                    messagebox.showinfo("Sign In", "Sign-in successful!")
                    shared.uid=user_id
                    print(shared.uid)
                    sign_in_window.destroy()
                    print("Proceed to next page")
                    print(shared.uid)
                    next()
                else:
                    messagebox.showerror("Sign In Error", "Incorrect password for the provided User ID.")
                    sign_in_window.destroy()
                    open_sign_in()
            else:
                # If no row was fetched for the provided user ID
                messagebox.showerror("Sign In Error", "User ID not found.")
                sign_in_window.destroy()
                open_sign_in()

            con.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error during sign-in: {e}")

    sign_in_button = Button(sign_in_window, text="Sign In", command=sign_in)
    sign_in_button.pack()

    # Create a "Create New Account" button
    def create_account():
        sign_in_window.destroy()  # Close the sign-in window
        open_create_account()  # Open the create account window

    create_account_button = Button(sign_in_window, text="Create New Account", command=create_account)
    create_account_button.pack()
    sign_in_window.mainloop()

def open_create_account():
    global username_entry, password_entry, confirm_password_entry
    # Define the create account window
    create_account_window = Tk()
    create_account_window.title("Create New Account")
    create_account_window.geometry("400x300")
    create_account_window.configure(bg="#242424")


    # Create labels and entry fields for username and password
    username_label = Label(create_account_window, text="Username:", bg="#242424", fg="white")
    username_label.pack()

    username_entry = Entry(create_account_window)
    username_entry.pack()

    password_label = Label(create_account_window, text="Password:", bg="#242424", fg="white")
    password_label.pack()

    password_entry = Entry(create_account_window, show="*")
    password_entry.pack()

    confirm_password_label = Label(create_account_window, text="Confirm Password:", bg="#242424", fg="white")
    confirm_password_label.pack()

    confirm_password_entry = Entry(create_account_window, show="*")
    confirm_password_entry.pack()

    # Define function to create a new account
    def create_new_account():
        # Retrieve the username and passwords entered by the user
        

        # Retrieve the username and passwords entered by the user
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Validate if the passwords match
        if password == confirm_password:
            # Add logic to create a new account in the database
            try:
                con = sqlite3.connect("Fitness.db")
                cursor = con.cursor()

                # Insert the user into the database
                cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
                con.commit()

                # Retrieve the UID of the newly created user
                cursor.execute("SELECT uid FROM user WHERE username=?", (username,))
                uid = cursor.fetchone()[0]
                shared.uid=uid
                messagebox.showinfo("New Account", f"Account created successfully! Your User ID is: {uid}")
                con.close()
                create_account_window.destroy()
                next()# Close the window after successful account creation
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error creating account: {e}")
        else:
            # If passwords do not match, show an error message
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please try again.")

    create_account_button = Button(create_account_window, text="Create Account", command=create_new_account)
    create_account_button.pack()
    create_account_window.mainloop()
    # Add other widgets as needed for account creation


    # Add other widgets as needed for account creation

# Main program flow
create_database()  # Ensure the database is created
# loading_window()  # Show loading window
open_sign_in()
