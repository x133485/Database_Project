from customtkinter import *
from PIL import Image
from tkinter import messagebox
from main import main_menu  # Import the main_menu function

def login():
    if UsernameEntry.get() == '' or PasswordEntry.get() == '':
        messagebox.showerror('Error', 'All fields must be entered')
    elif UsernameEntry.get() == '1' and PasswordEntry.get() == '1':
        app.destroy()
        main_menu()  # Call the main_menu function upon successful login
    else:
        messagebox.showerror('Error', 'Invalid credentials')

def show_login():
    global app, UsernameEntry, PasswordEntry
    app = CTk()
    width = 1200
    height = 700
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    app.geometry(f"{width}x{height}+{x}+{y}")
    
    image = CTkImage(Image.open('cover.jpg'), size=(1200, 700))
    imageLablel = CTkLabel(app, image=image, text='')
    imageLablel.place(x=0, y=0)
    
    headingLabel = CTkLabel(app, text='GSV Management System', bg_color='black', 
                           font=('poppins', 30, 'bold'), text_color='white')
    headingLabel.place(relx=0.5, rely=0.3, anchor='center')
    
    UsernameEntry = CTkEntry(app, placeholder_text="Enter Your Username", width=220)
    UsernameEntry.place(relx=0.5, rely=0.45, anchor='center')
    
    PasswordEntry = CTkEntry(app, placeholder_text="Enter Your Password", width=220, show='*')
    PasswordEntry.place(relx=0.5, rely=0.52, anchor='center')
    
    LoginButton = CTkButton(app, text='Login', cursor='hand2', command=login)
    LoginButton.place(relx=0.5, rely=0.6, anchor='center')
    
    app.mainloop()

if __name__ == "__main__":
    show_login()