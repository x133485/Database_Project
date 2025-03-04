import customtkinter
import tkinter as tk
from tkinter import ttk
from PIL import Image
from db_connect import connect_to_database
from coaching_event import open_coaching_event_window  # 导入分配窗口

def open_coaching_window(main_window):
    main_window.withdraw()
    coaching_window = customtkinter.CTkToplevel()
    coaching_window.title("Coaching Management")
    width = 1200
    height = 700
    screen_width = coaching_window.winfo_screenwidth()
    screen_height = coaching_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    coaching_window.geometry(f"{width}x{height}+{x}+{y}")

    # ===================== Left Panel (Input & Actions) ===================== #
    left_frame = customtkinter.CTkFrame(coaching_window, width=250, corner_radius=0)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Coach ID input
    coach_id_label = customtkinter.CTkLabel(left_frame, text="Coach ID:")
    coach_id_label.pack(anchor="w", pady=5)
    coach_id_entry = customtkinter.CTkEntry(left_frame)
    coach_id_entry.pack(anchor="w", pady=5)

    # Name input
    name_label = customtkinter.CTkLabel(left_frame, text="Name:")
    name_label.pack(anchor="w", pady=5)
    name_entry = customtkinter.CTkEntry(left_frame)
    name_entry.pack(anchor="w", pady=5)

    # Expertise input
    expertise_label = customtkinter.CTkLabel(left_frame, text="Expertise:")
    expertise_label.pack(anchor="w", pady=5)
    expertise_entry = customtkinter.CTkEntry(left_frame)
    expertise_entry.pack(anchor="w", pady=5)

    # Button to add a coach
    def add_coach():
        c_id = coach_id_entry.get()
        name_val = name_entry.get()
        exp_val = expertise_entry.get()
        if not c_id:
            print("Coach ID cannot be empty!")
            return
        if exp_val == "":
            exp_val = None
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO coaching (coach_id, name, expertise)
                    VALUES (%s, %s, %s)
                """
                cur.execute(insert_query, (c_id, name_val, exp_val))
                conn.commit()
                print("Coach added successfully!")
                load_coaches()
            except Exception as e:
                print("Error adding coach:", e)
            finally:
                cur.close()
                conn.close()
    add_button = customtkinter.CTkButton(left_frame, text="Add Coach", command=add_coach)
    add_button.pack(pady=10)

    # ----------------- Search Section ----------------- #
    search_label = customtkinter.CTkLabel(left_frame, text="Search by ID or Name:")
    search_label.pack(anchor="w", pady=5)
    search_entry = customtkinter.CTkEntry(left_frame)
    search_entry.pack(anchor="w", pady=5)

    def search_coach():
        search_val = search_entry.get()

        if not search_val:
            load_coaches()
            return

        for row in coach_tree.get_children():
            coach_tree.delete(row)

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                search_query = """
                    SELECT coach_id, name, expertise
                    FROM coaching
                    WHERE CAST(coach_id AS TEXT) LIKE %s OR name ILIKE %s
                    ORDER BY coach_id
                """
                search_pattern = f'%{search_val}%'
                cur.execute(search_query, (search_pattern, search_pattern))
                rows = cur.fetchall()
                if not rows:
                    coach_tree.insert("", tk.END, values=("No results", f"found for '{search_val}'", ""))
                else:
                    for row in rows:
                        coach_tree.insert("", tk.END, values=row)
            except Exception as e:
                coach_tree.insert("", tk.END, values=("Error", "searching", str(e), ""))
            finally:
                cur.close()
                conn.close()

    search_button = customtkinter.CTkButton(left_frame, text="Search", command=search_coach)
    search_button.pack(pady=5)

    # ----------------- Refresh (Show All) Section ----------------- #
    refresh_button = customtkinter.CTkButton(left_frame, text="Show All", command=lambda: load_coaches())
    refresh_button.pack(pady=5)

    # Button to modify a coach
    def modify_coach():
        c_id = coach_id_entry.get()
        name_val = name_entry.get()
        exp_val = expertise_entry.get()
        if not c_id:
            print("Coach ID cannot be empty!")
            return
        if exp_val == "":
            exp_val = None
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                update_query = """
                    UPDATE coaching
                    SET name = %s, expertise = %s
                    WHERE coach_id = %s
                """
                cur.execute(update_query, (name_val, exp_val, c_id))
                conn.commit()
                print("Coach modified successfully!")
                load_coaches()
            except Exception as e:
                print("Error modifying coach:", e)
            finally:
                cur.close()
                conn.close()
    modify_button = customtkinter.CTkButton(left_frame, text="Update", command=modify_coach)
    modify_button.pack(pady=10)

    # Button to delete a coach
    def delete_coach():
        selected = coach_tree.selection()
        if not selected:
            print("Please select a coach to delete!")
            return
        item = selected[0]
        values = coach_tree.item(item, "values")
        coach_id_val = values[0]
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()

                delete_coaching_query = """
                    DELETE FROM coaching
                    WHERE coach_id = %s
                """
                cur.execute(delete_coaching_query, (coach_id_val,))

                delete_coaching_event_query = """
                    DELETE FROM coaching_event
                    WHERE coach_id = %s
                """
                cur.execute(delete_coaching_event_query, (coach_id_val,))

                conn.commit()
                print(f"Coach {coach_id_val} deleted!")
                load_coaches()
            except Exception as e:
                print("Error deleting coach:", e)
            finally:
                cur.close()
                conn.close()
    delete_button = customtkinter.CTkButton(left_frame, text="Delete Coach", command=delete_coach)
    delete_button.pack(pady=10)

    # Button to assign a coach to an event
    assign_event_button = customtkinter.CTkButton(left_frame, text="Assign to Event", command=open_coaching_event_window)
    assign_event_button.pack(pady=10)

    def go_back():
        coaching_window.destroy()
        main_window.deiconify()

    back_button = customtkinter.CTkButton(
        left_frame,
        text="Back",
        fg_color="#cc3333",  # Red color
        text_color="white",
        hover_color="#d94d4d",
        command=go_back
    )
    back_button.pack(side="bottom", pady=20)

    # ===================== Middle Panel (Coach Photo) ===================== #
    middle_frame = customtkinter.CTkFrame(coaching_window, width=300, corner_radius=0)
    middle_frame.pack(side="left", fill="both", padx=10, pady=10)
    try:
        photo_image = customtkinter.CTkImage(Image.open("coach_photo.jpg"), size=(300, 300))
    except Exception as e:
        print("Error loading coach photo:", e)
        photo_image = None
    if photo_image:
        photo_label = customtkinter.CTkLabel(middle_frame, text="", image=photo_image)
    else:
        photo_label = customtkinter.CTkLabel(middle_frame, text="No Image")
    photo_label.pack(expand=True)

    # ===================== Right Panel (Treeview) ===================== #
    right_frame = customtkinter.CTkFrame(coaching_window, corner_radius=0)
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), anchor="center")
    style.configure("Treeview", font=("Helvetica", 12), rowheight=30)
    tree_columns = ("coach_id", "name", "expertise")
    coach_tree = ttk.Treeview(right_frame, columns=tree_columns, show="headings")
    coach_tree.heading("coach_id", text="Coach ID", anchor="center")
    coach_tree.heading("name", text="Name", anchor="center")
    coach_tree.heading("expertise", text="Expertise", anchor="center")
    coach_tree.column("coach_id", anchor="center")
    coach_tree.column("name", anchor="center")
    coach_tree.column("expertise", anchor="center")
    coach_tree.pack(expand=True, fill="both")

    def load_coaches():
        for row in coach_tree.get_children():
            coach_tree.delete(row)
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                select_query = """
                    SELECT coach_id, name, expertise
                    FROM coaching
                    ORDER BY coach_id ASC
                """
                cur.execute(select_query)
                rows = cur.fetchall()
                for row in rows:
                    coach_tree.insert("", tk.END, values=row)
            except Exception as e:
                print("Error fetching coaches:", e)
            finally:
                cur.close()
                conn.close()
    load_coaches()

    def populate_fields(event):
        selected_item = coach_tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = coach_tree.item(item, "values")
        coach_id_entry.delete(0, tk.END)
        coach_id_entry.insert(0, values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        expertise_entry.delete(0, tk.END)
        expertise_entry.insert(0, values[2])
    coach_tree.bind("<ButtonRelease-1>", populate_fields)
