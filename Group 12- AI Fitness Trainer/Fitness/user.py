from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from candidates import cand
import sqlite3

def userPage():
    conn = sqlite3.connect('SecureVoteX.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = 'voting_enabled'")
    voting_enabled = bool(cursor.fetchone()[0])
    conn.close()

    if not voting_enabled:
        messagebox.showerror('Voting Stopped', 'Voting has been stopped by the admin.')
        return


    dup=open('dup.txt','a+')
    dup.seek(0)
        ## Tries to initialize the fingerprint sensor

    cand()
                    

