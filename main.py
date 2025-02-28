from db_connect import connect_to_database
import customtkinter
from PIL import Image

def main_menu():
    conn = connect_to_database()
    if conn is None:
        print("Can't connected to database.\n")

    from volunteer import open_volunteer_window
    from event import open_event_window
    from participant import open_participant_window
    from coaching import open_coaching_window
    from equipment import open_equipment_window

    app = customtkinter.CTk()
    app.title("Global Sports Volunteers Management System")
    width = 1200
    height = 700
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    app.geometry(f"{width}x{height}+{x}+{y}")
    
    # Sidebar
    sidebar_frame = customtkinter.CTkFrame(
        app,
        width=80,
        corner_radius=0,
        fg_color="#2b2b2b"  
    )
    sidebar_frame.pack(side="left", fill="y")
    
    # Some Buttons
    add_event_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="Event",
        fg_color="#3c3c3c",
        text_color="white",
        hover_color="#4d4d4d",
        command=lambda: open_event_window(app)  # Pass the main window to the function
    )
    add_event_btn.pack(pady=20, padx=10)
    
    volunteer_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="Volunteer",
        fg_color="#3c3c3c",
        text_color="white",
        hover_color="#4d4d4d",
        command=lambda: open_volunteer_window(app)
    )
    volunteer_btn.pack(pady=10, padx=10)
    
    participant_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="Participant",
        fg_color="#3c3c3c",
        text_color="white",
        hover_color="#4d4d4d",
        command=lambda: open_participant_window(app)
    )
    participant_btn.pack(pady=10, padx=10)

    participant_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="Coaching",
        fg_color="#3c3c3c",
        text_color="white",
        hover_color="#4d4d4d",
        command= lambda: open_coaching_window(app)
    )
    participant_btn.pack(pady=10, padx=10)

    volunteer_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="Equipment",
        fg_color="#3c3c3c",
        text_color="white",
        hover_color="#4d4d4d",
        command=lambda: open_equipment_window(app)
    )
    volunteer_btn.pack(pady=10, padx=10)
    
    def logout_and_login():
        app.destroy()
        from login import show_login
        show_login()

    exit_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="Logout",
        fg_color="#cc3333",
        text_color="white",
        hover_color="#d94d4d",
        command=logout_and_login # Call the logout_and_login function
    )
    exit_btn.pack(side="bottom", pady=20, padx=10)
    
    # --------------------Right Side------------------------------------------------

    content_frame = customtkinter.CTkFrame(app, corner_radius=0, fg_color="#2cd1b6")
    content_frame.pack(side="right", expand=True, fill="both")
    
    bg_image = customtkinter.CTkImage(Image.open("background1.jpg"), size=(1050, 700))
    bg_label = customtkinter.CTkLabel(content_frame, text="", image=bg_image)
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    welcome_label = customtkinter.CTkLabel(
        content_frame,
        text="Welcome to Global Sports Volunteers System!",
        font=("Helvetica", 24, "bold"),
        text_color="#333333"
    )
    welcome_label.place(relx=0.5, rely=0.3, anchor="center")
    
    desc_label = customtkinter.CTkLabel(
        content_frame,
        text="Empower your sports initiatives with a comprehensive, all-in-one solution!\nThe Global Sports Volunteers (GSV) Database Management System\n is designed to streamline operations for nonprofit organizations\n dedicated to promoting sports and physical activity in underserved communities worldwide.",
        font=("Helvetica", 14),
        text_color="#555555",
        wraplength=600  
    )
    desc_label.place(relx=0.5, rely=0.4, anchor="center")
    

    def on_closing():
        if conn:
            conn.close()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    
    app.mainloop()

if __name__ == "__main__":
    #main_menu() #  we may remove this line and call it from login.py as shown below
    from login import show_login
    show_login()

