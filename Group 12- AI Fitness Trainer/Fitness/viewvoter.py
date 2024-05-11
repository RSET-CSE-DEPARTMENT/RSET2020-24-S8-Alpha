from tkinter import *
import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image,ImageTk
existing_root = None
con = sqlite3.connect(database="SecureVoteX.db")
cur = con.cursor()

# Enter Table Names here
v = "voter" 
  
def viewvote(): 
    global existing_root  # Declare the variable as global to modify it inside the function

    if existing_root and existing_root.winfo_exists():  # Check if the existing root exists and is not closed
        existing_root.destroy()
    root = tk.Toplevel(bg="#242424")
    root.title("Voters List")
    root.minsize(width=400,height=400)
    root.geometry("600x500")

    Canvas1 = Canvas(root) 
    Canvas1.config(bg="#242424")
    Canvas1.pack(expand=True,fill=BOTH)
        
        
    headingFrame1 = Frame(root, bg="#2b2b2b")
    headingFrame1.place(relx=0,rely=0,relwidth=1,relheight=0.23)
        
    headingLabel = Label(headingFrame1, text="Voters List", bg="#2b2b2b", fg='white', font=('Courier',15))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    
    labelFrame = Frame(root,bg="#2b2b2b")
    labelFrame.place(relx=0.1,rely=0.35,relwidth=0.8,relheight=0.52)
    y = 0.25
    labelFrame1 = Frame(root,bg='#1f69a6')
    labelFrame1.place(relx=0.1,rely=0.25,relwidth=0.8,relheight=0.1)
    t = Text(labelFrame1, bg='#1f69a6',fg='white')
    #text.insert("1.0","%-10s"%('UID')).place(relx=0.03,rely=0.08)
    t.tag_config('header', justify='left')
    t.insert("1.0", "%-10s" % ('UID') + "\t" + "%-30s" % ('NAME') + "\t" + "%-30s" % ('IMAGE') + "\n", 'header')
    t.insert("end", "--------------------------------------------------------------\n")
    t.pack()
    s = Scrollbar(labelFrame, orient=VERTICAL)
    s.pack(side=RIGHT, fill='y')
    text = Text(labelFrame,bg='#2b2b2b',fg='white',yscrollcommand=s.set)
    #text.insert("1.0","%-10s"%('UID')).place(relx=0.03,rely=0.08)
    text.tag_config('header', justify='left')
    text.tag_config('header', justify='left')
    text.insert("1.0", "", 'header')

    getv = "select * from "+v
    try:
        cur.execute(getv)
        con.commit()
        image_references = []
        for i in cur:
            text.insert("end", "%-10s" % (i[0]) + "\t" + "%-30s" % (i[1]) + "\t")
            print(i[0],i[1],i[2],i[3])
            #Label(labelFrame, text="%-30s"%(i[2]),bg='black',fg='white').place(relx=0.37,rely=y)
            ipath = str(i[2])
            print(ipath)
            try:
                image = Image.open(ipath)
                
                test = image.resize((50, 50)) 
                test = ImageTk.PhotoImage(test)
                text.image_create("end", image=test)
                image_references.append(test)
                #y += 0.3
                
            except Exception as e:
                messagebox.showerror("Error loading image",str(e),parent=root)
            
            text.insert("end", "\n")
            y += 1

    except Exception as e:
        messagebox.showinfo("Failed to fetch files from database",str(e))
    
    s.config(command=text.yview)
    text.pack()
    quitBtn = Button(root,text="Quit",bg='#1f69a6', fg='white', command=root.destroy)
    quitBtn.place(relx=0.4,rely=0.9, relwidth=0.18,relheight=0.08)
    root.protocol("WM_DELETE_root", on_close)

    existing_root = root  # Update the reference to the existing root

    root.mainloop()
def on_close():
    global existing_window  # Declare the variable as global to modify it inside the function
    if existing_window:
        existing_window.destroy()  # Destroy the existing window
    existing_window = None
#viewvote()