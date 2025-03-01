import customtkinter
import tkinter as tk
from tkinter import ttk
from db_connect import connect_to_database
from participant_event import open_participant_event_window

def open_participant_window(main_window):
    main_window.withdraw()

    # Create a top-level window
    participant_window = customtkinter.CTkToplevel()
    participant_window.title("Participant Management")
    width = 1200
    height = 700
    screen_width = participant_window.winfo_screenwidth()
    screen_height = participant_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    participant_window.geometry(f"{width}x{height}+{x}+{y}")

    # ===================== Left Panel (Input & Actions) ===================== #
    left_frame = customtkinter.CTkFrame(participant_window, width=250, corner_radius=0)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # --- Participant ID ---
    participant_id_label = customtkinter.CTkLabel(left_frame, text="Participant ID:")
    participant_id_label.pack(anchor="w", pady=5)
    participant_id_entry = customtkinter.CTkEntry(left_frame)
    participant_id_entry.pack(anchor="w", pady=5)

    # --- Name ---
    name_label = customtkinter.CTkLabel(left_frame, text="Name:")
    name_label.pack(anchor="w", pady=5)
    name_entry = customtkinter.CTkEntry(left_frame)
    name_entry.pack(anchor="w", pady=5)

    # --- Contact Information ---
    contact_info_label = customtkinter.CTkLabel(left_frame, text="Contact Information:")
    contact_info_label.pack(anchor="w", pady=5)
    contact_info_entry = customtkinter.CTkEntry(left_frame)
    contact_info_entry.pack(anchor="w", pady=5)

    # ----------------- Save Participant ----------------- #
    def save_participant():
        p_id_val = participant_id_entry.get()
        name_val = name_entry.get()
        contact_val = contact_info_entry.get()

        if not p_id_val:
            print("Participant ID cannot be empty!")
            return

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO participant (participant_id, name, contact_information)
                    VALUES (%s, %s, %s)
                """
                cur.execute(insert_query, (p_id_val, name_val, contact_val))
                conn.commit()
                print("Participant saved successfully!")
                load_participants()
            except Exception as e:
                print("Error inserting participant into database:", e)
            finally:
                cur.close()
                conn.close()
    save_button = customtkinter.CTkButton(left_frame, text="Save Participant", command=save_participant)
    save_button.pack(pady=10)

    # ----------------- Search Section ----------------- #
    search_label = customtkinter.CTkLabel(left_frame, text="Search by ID or Name:")
    search_label.pack(anchor="w", pady=5)
    search_entry = customtkinter.CTkEntry(left_frame)
    search_entry.pack(anchor="w", pady=5)

    def search_participant():
        search_val = search_entry.get()

        if not search_val:
            load_participants()
            return

        for row in participant_tree.get_children():
            participant_tree.delete(row)

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                search_query = """
                    SELECT participant_id, name, contact_information
                    FROM participant
                    WHERE CAST(participant_id AS TEXT) LIKE %s OR name ILIKE %s
                    ORDER BY participant_id
                """
                search_pattern = f'%{search_val}%'
                cur.execute(search_query, (search_pattern, search_pattern))
                rows = cur.fetchall()
                if not rows:
                    participant_tree.insert("", tk.END, values=("No results", f"found for '{search_val}'", ""))
                else:
                    for row in rows:
                        participant_tree.insert("", tk.END, values=row)
            except Exception as e:
                participant_tree.insert("", tk.END, values=("Error", "searching", str(e)))
            finally:
                cur.close()
                conn.close()

    search_button = customtkinter.CTkButton(left_frame, text="Search", command=search_participant)
    search_button.pack(pady=5)

        # ----------------- Refresh Participants ----------------- #
    refresh_button = customtkinter.CTkButton(left_frame, text="Show All", command=lambda: load_participants())
    refresh_button.pack(pady=5)

    # ----------------- Modify Participant ----------------- #
    def modify_participant():
        p_id_val = participant_id_entry.get()
        name_val = name_entry.get()
        contact_val = contact_info_entry.get()

        if not p_id_val:
            print("Participant ID cannot be empty!")
            return

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                update_query = """
                    UPDATE participant
                    SET name = %s, contact_information = %s
                    WHERE participant_id = %s
                """
                cur.execute(update_query, (name_val, contact_val, p_id_val))
                conn.commit()
                print("Participant modified successfully!")
                load_participants()
            except Exception as e:
                print("Error modifying participant:", e)
            finally:
                cur.close()
                conn.close()
    modify_button = customtkinter.CTkButton(left_frame, text="Update", command=modify_participant)
    modify_button.pack(pady=10)

    # ----------------- Delete Participant ----------------- #
    def delete_participant():
        selected_item = participant_tree.selection()
        if not selected_item:
            print("Please select a participant to delete!")
            return

        item = selected_item[0]
        values = participant_tree.item(item, "values")
        p_id_val = values[0]

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()

                delete_event_participant_query = """
                    DELETE FROM event_participant
                    WHERE participant_id = %s
                """
                cur.execute(delete_event_participant_query, (p_id_val,))

                delete_query = """
                    DELETE FROM participant
                    WHERE participant_id = %s
                """
                cur.execute(delete_query, (p_id_val,))
                conn.commit()

                print(f"Participant '{p_id_val}' has been deleted!")
                load_participants()
            except Exception as e:
                print("Error deleting participant from database:", e)
            finally:
                cur.close()
                conn.close()
    delete_button = customtkinter.CTkButton(left_frame, text="Delete Participant", command=delete_participant)
    delete_button.pack(pady=5)

    # ----------------- Assign Event Section ----------------- #
    assign_event_button = customtkinter.CTkButton(left_frame, text="Assign to Event", command=open_participant_event_window)
    assign_event_button.pack(pady=10)

    def go_back():
        participant_window.destroy()
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

    # ===================== Right Panel (Treeview) ===================== #
    right_frame = customtkinter.CTkFrame(participant_window, corner_radius=0)
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 16, "bold"), rowheight=50)
    style.configure("Treeview", font=("Helvetica", 15))

    tree_columns = ("participant_id", "name", "contact_information")
    participant_tree = ttk.Treeview(right_frame, columns=tree_columns, show="headings")
    participant_tree.heading("participant_id", text="Participant ID")
    participant_tree.heading("name", text="Name")
    participant_tree.heading("contact_information", text="Contact Information")
    participant_tree.pack(expand=True, fill="both")

    participant_tree.column("participant_id", width=50)
    participant_tree.column("name", width=80)
    participant_tree.column("contact_information", width=120)

    def load_participants():
        for row in participant_tree.get_children():
            participant_tree.delete(row)
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                # 增加 ORDER BY 使记录按 participant_id 升序排列
                select_query = """
                    SELECT participant_id, name, contact_information
                    FROM participant
                    ORDER BY participant_id ASC
                """
                cur.execute(select_query)
                rows = cur.fetchall()
                for row in rows:
                    participant_tree.insert("", tk.END, values=row)
            except Exception as e:
                print("Error fetching participants from database:", e)
            finally:
                cur.close()
                conn.close()
    load_participants()

    def populate_fields(event):
        selected_item = participant_tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = participant_tree.item(item, "values")
        participant_id_entry.delete(0, tk.END)
        participant_id_entry.insert(0, values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        contact_info_entry.delete(0, tk.END)
        contact_info_entry.insert(0, values[2])
    participant_tree.bind("<ButtonRelease-1>", populate_fields)

