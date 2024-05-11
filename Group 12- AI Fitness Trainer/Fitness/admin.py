from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from newvote import *
from delvot import *
from addcand import *
from viewcand import *
from viewvoter import *
from delcand import *
from view_result import *
import sqlite3

admin_window = None
class VideoPlayer:
    def __init__(self, master, video_source):
        self.master = master
        self.video_source = video_source

        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()

        self.cap = cv2.VideoCapture(self.video_source)
        self.display_video()

    def display_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.master.after(10, self.display_video)

# def delete():
#     global existing_root  # Declare the variable as global to modify it inside the function

#     if existing_root and existing_root.winfo_exists():  # Check if the existing root exists and is not closed
#         existing_root.destroy()
#     global root
    
#     root = tk.Toplevel()
#     root.title("Video Player")
#     file_path = filedialog.askopenfilename()
#     if file_path:
#         print("Selected file:", file_path)
#     video_source = file_path  # Change this to the path of your video file

#     VideoPlayer(root, video_source)
#     root.protocol("WM_DELETE_root", on_close)

#     existing_root = root  

#     root.mainloop()
def on_admin_window_close():
    global admin_window
    admin_window.destroy()
    admin_window = None

def stop_voting():
    conn = sqlite3.connect('SecureVoteX.db')
    cursor = conn.cursor()

    # Update the voting status to False
    cursor.execute("UPDATE settings SET value = ? WHERE key = ?", (0, 'voting_enabled'))
    conn.commit()

    cursor.close()
    conn.close()

    messagebox.showinfo("Voting Stopped", "Voting has been stopped. No further votes will be accepted.",parent=admin_window)

def start_voting():
    conn = sqlite3.connect('SecureVoteX.db')
    cursor = conn.cursor()

    # Update the voting status to True
    cursor.execute("UPDATE settings SET value = ? WHERE key = ?", (1, 'voting_enabled'))
    conn.commit()

    cursor.close()
    conn.close()

    messagebox.showinfo("Voting Started", "Voting has been started. Votes can now be cast.",parent=admin_window)

def view_results():
    conn = sqlite3.connect('SecureVoteX.db')
    cursor = conn.cursor()

    # Retrieve the voting status
    cursor.execute("SELECT value FROM settings WHERE key = 'voting_enabled'")
    result = cursor.fetchone()
    print(result)
    # Check if voting is enabled or disabled
    if result is None or result[0] == 1:
        messagebox.showerror("Voting in Progress", "Voting is currently in progress. Results cannot be viewed at the moment.",parent=admin_window)
    else:
        # Open the results window
        viewResult()

    cursor.close()
    conn.close()
def Admin():
    global admin_window

    if admin_window is None:
        admin_window = Toplevel()
        admin_window.protocol("WM_DELETE_WINDOW", on_admin_window_close)
        admin_window.lift()
        admin_window.title("ADMIN")
        admin_window.minsize(width=600, height=500)
        admin_window.geometry("400x400")

        Canvas1 = Canvas(admin_window)
        Canvas1.config(bg="#2b2b2b")
        Canvas1.pack(expand=True, fill=BOTH)

        headingFrame1 = Frame(admin_window, bg="#242424", bd=0.5)
        headingFrame1.place(relx=0, rely=0, relwidth=1, relheight=0.23)

        headingLabel = Label(headingFrame1, text="ADMIN", bg='#242424', fg='white',font=('Comic Sans MS', 20, 'bold'))
        headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

        # btn1 = Button(admin_window, text="NEW VOTER", bg='#1f69a6', fg='white', command=newvote)
        # btn1.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.1)

        btn4 = Button(admin_window, text="Browse Video", bg='#1f69a6', fg='Black', command=delete)
        btn4.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1)

        # btn2 = Button(admin_window, text="VIEW CANDIDATES", bg='#1f69a6', fg='white', command=viewcand)
        # btn2.place(relx=0.7, rely=0.6, relwidth=0.2, relheight=0.1)

        # btn5 = Button(admin_window, text="NEW CANDIDATE", bg='#1f69a6', fg='white', command=addCand)
        # btn5.place(relx=0.1, rely=0.6, relwidth=0.2, relheight=0.1)

        # btn6 = Button(admin_window, text="DELETE CANDIDATE", bg='#1f69a6', fg='white', command=delc)
        # btn6.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.1)

        # btn3 = Button(admin_window, text="VIEW VOTERS", bg='#1f69a6', fg='white', command=viewvote)
        # btn3.place(relx=0.7, rely=0.4, relwidth=0.2, relheight=0.1)

        # stopBtn = Button(admin_window, text="STOP VOTING", bg='RED', fg='white', command=stop_voting)
        # stopBtn.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

        # startBtn = Button(admin_window, text="START VOTING", bg='GREEN', fg='white', command=start_voting)
        # startBtn.place(relx=0.1, rely=0.8, relwidth=0.2, relheight=0.1)

        # viewResultsBtn = Button(admin_window, text="VIEW RESULTS", bg='#1f69a6', fg='white', command=view_results)
        # viewResultsBtn.place(relx=0.7, rely=0.8, relwidth=0.2, relheight=0.1)

        admin_window.mainloop()
    else:
        admin_window.lift()
# Admin()
