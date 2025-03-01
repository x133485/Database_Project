import customtkinter
import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import connect_to_database


def show_event_details(event_window):

    details_window = customtkinter.CTkToplevel()
    details_window.title("Event Details")
    width = 800
    height = 550
    screen_width = details_window.winfo_screenwidth()
    screen_height = details_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    details_window.geometry(f"{width}x{height}+{x}+{y}")
    details_window.transient(event_window)  # Make details_window a child of event_window
    details_window.grab_set()  # Ensure all events are directed to details_window
    details_text = tk.Text(details_window, wrap="word", font=("Helvetica", 12))
    details_text.pack(expand=True, fill="both")

    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            
            cur.execute("SELECT event_code, event_description FROM events ORDER BY event_code ASC")
            events = cur.fetchall()
            details_str = ""
            for event in events:
                event_code, event_desc = event
                details_str += f"Event Code: {event_code}, Event Name: {event_desc}\n"
                
                # use idx_event_participant_event_code 
                cur.execute("""
                    SELECT p.name
                    FROM event_participant ep
                    JOIN participant p ON ep.participant_id = p.participant_id
                    WHERE ep.event_code = %s
                """, (event_code,))
                participants = cur.fetchall()
                participant_names = [p[0] for p in participants]
                details_str += "  Participants: " + (", ".join(participant_names) if participant_names else "None") + "\n"
                
                # use idx_volunteer_event_event_code 
                cur.execute("""
                    SELECT v.name
                    FROM volunteer_event ve
                    JOIN volunteers v ON ve.volun_id = v.volun_id
                    WHERE ve.event_code = %s
                """, (event_code,))
                volunteers = cur.fetchall()
                volunteer_names = [v[0] for v in volunteers]
                details_str += "  Volunteers: " + (", ".join(volunteer_names) if volunteer_names else "None") + "\n\n"
            details_text.insert("1.0", details_str)
        except Exception as e:
            details_text.insert("1.0", f"Error fetching event details: {e}")
        finally:
            cur.close()
            conn.close()

def open_event_window(main_window):
    # Hide main window
    main_window.withdraw()

    event_window = customtkinter.CTkToplevel()
    event_window.title("Event Management")
    width = 1200
    height = 700
    screen_width = event_window.winfo_screenwidth()
    screen_height = event_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    event_window.geometry(f"{width}x{height}+{x}+{y}")

    # ===================== Left Panel (Input & Actions) ===================== #
    left_frame = customtkinter.CTkFrame(event_window, width=250, corner_radius=0)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # --- Event Code ---
    event_code_label = customtkinter.CTkLabel(left_frame, text="Event Code:")
    event_code_label.pack(anchor="w", pady=5)
    event_code_entry = customtkinter.CTkEntry(left_frame)
    event_code_entry.pack(anchor="w", pady=5)

    # --- Event Description ---
    event_desc_label = customtkinter.CTkLabel(left_frame, text="Event Description:")
    event_desc_label.pack(anchor="w", pady=5)
    event_desc_entry = customtkinter.CTkEntry(left_frame)
    event_desc_entry.pack(anchor="w", pady=5)

    # --- Event Type ---
    event_type_label = customtkinter.CTkLabel(left_frame, text="Event Type:")
    event_type_label.pack(anchor="w", pady=5)
    event_type_entry = customtkinter.CTkEntry(left_frame)
    event_type_entry.pack(anchor="w", pady=5)

    # --- Event Status ---
    event_status_label = customtkinter.CTkLabel(left_frame, text="Event Status:")
    event_status_label.pack(anchor="w", pady=5)
    event_status_entry = customtkinter.CTkEntry(left_frame)
    event_status_entry.pack(anchor="w", pady=5)

    # ------------------ Functions ------------------ #

    def load_events():
        # Clear existing rows
        for row in event_tree.get_children():
            event_tree.delete(row)

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                select_query = """
                    SELECT 
                        e.event_code,
                        e.event_description,
                        e.event_type,
                        e.event_status,
                        (SELECT COUNT(*) 
                         FROM event_participant ep 
                         WHERE ep.event_code = e.event_code) AS participant_count,
                        (SELECT COUNT(*) 
                         FROM volunteer_event ve
                         WHERE ve.event_code = e.event_code) AS volunteer_count
                    FROM events e
                    ORDER BY e.event_code ASC
                """
                cur.execute(select_query)
                rows = cur.fetchall()
                for row_data in rows:
                    # row[0] is the numeric event_code from DB
                    event_tree.insert("", tk.END, values=row_data)
            except Exception as e:
                print("Error fetching events from database:", e)
            finally:
                cur.close()
                conn.close()

    def save_event():
        """Insert new event into the DB, converting event_code to an integer."""
        code_val = event_code_entry.get()
        desc_val = event_desc_entry.get()
        type_val = event_type_entry.get()
        status_val = event_status_entry.get()

        # Simple validation: Event Code must not be empty
        if not code_val:
            messagebox.showerror("Error", "Event Code cannot be empty!")
            return

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO events (event_code, event_description, event_type, event_status)
                    VALUES (%s, %s, %s, %s)
                """
                cur.execute(insert_query, (code_val, desc_val, type_val, status_val))
                conn.commit()
                print("Event saved successfully!")
                load_events()
                clear_fields()
            except Exception as e:
                conn.rollback()  # Rollback the transaction on error || part of transaction management
                messagebox.showerror("Error", f"Error inserting event into database: {e}")
            finally:
                cur.close()
                conn.close()

    def delete_event():
        selected_item = event_tree.selection()
        if not selected_item:
            print("Please select an event to delete!")
            return

        # Get the first selected item
        item = selected_item[0]
        # Retrieve column values from the selected row; event_code is index 0
        values = event_tree.item(item, "values")
        code_val = values[0] 


        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                # Start a transaction
                conn.autocommit = False

                # 1. Delete from coaching_event
                delete_coaching_event_query = """
                    DELETE FROM coaching_event
                    WHERE event_code = %s
                """
                cur.execute(delete_coaching_event_query, (code_val,))

                # 2. Delete from equipment
                delete_equipment_query = """
                    DELETE FROM equipment
                    WHERE event_code = %s
                """
                cur.execute(delete_equipment_query, (code_val,))

                # 3. Delete from event_participant
                delete_event_participant_query = """
                    DELETE FROM event_participant
                    WHERE event_code = %s
                """
                cur.execute(delete_event_participant_query, (code_val,))

                # 4. Delete from volunteer_event
                delete_volunteer_event_query = """
                    DELETE FROM volunteer_event
                    WHERE event_code = %s
                """
                cur.execute(delete_volunteer_event_query, (code_val,))

                # 5. Finally, delete from events
                delete_query = """
                    DELETE FROM events
                    WHERE event_code = %s
                """
                cur.execute(delete_query, (code_val,))
                conn.commit()
                print(f"Event '{code_val}' has been deleted!")
                load_events()
                clear_fields()
            except Exception as e:
                conn.rollback()  # Rollback the transaction on error
                print("Error deleting event from database:", e)
            finally:
                cur.close()
                conn.close()

    def load_for_update():
        """
        When user selects a row and clicks 'Update Event',
        fill the left panel entries with the selected row's data.
        """
        selected_item = event_tree.selection()
        if not selected_item:
            print("Please select an event to Modify!")
            return
            
        values = event_tree.item(selected_item[0])['values']
        # values[0] = zero-padded code from the Treeview
        event_code_entry.delete(0, 'end')
        event_desc_entry.delete(0, 'end')
        event_type_entry.delete(0, 'end')
        event_status_entry.delete(0, 'end')
        
        event_code_entry.insert(0, values[0])   
        event_desc_entry.insert(0, values[1])
        event_type_entry.insert(0, values[2])
        event_status_entry.insert(0, values[3])

    def update_event():
        """
        If an event is selected, update the DB with the new data.
        If nothing is in event_code_entry, we call load_for_update() to populate fields.
        """
        if not event_code_entry.get():
            # If the user clicked 'Update Event' with nothing typed, let's load the data from selection
            load_for_update()
            return

        code_val = event_code_entry.get()
        desc_val = event_desc_entry.get()
        type_val = event_type_entry.get()
        status_val = event_status_entry.get()

        if not code_val or not desc_val or not type_val or not status_val:
            print("All fields are required for modification!")
            return

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                update_query = """
                    UPDATE events
                    SET event_description = %s,
                        event_type = %s,
                        event_status = %s
                    WHERE event_code = %s
                """
                cur.execute(update_query, (desc_val, type_val, status_val, code_val))
                conn.commit()
                print(f"Event {code_val} updated successfully!")
                
                load_events()
                clear_fields()
            except Exception as e:
                print("Error updating event:", e)
            finally:
                cur.close()
                conn.close()

    def clear_fields():
        """
        Clears the input fields in the left panel.
        """
        event_code_entry.delete(0, tk.END)
        event_desc_entry.delete(0, tk.END)
        event_type_entry.delete(0, tk.END)
        event_status_entry.delete(0, tk.END)

    # ------------------ Buttons ------------------ #
    save_button = customtkinter.CTkButton(left_frame, text="Save Event", command=save_event)
    save_button.pack(pady=10)

    # ----------------- Search Section ----------------- #
    search_label = customtkinter.CTkLabel(left_frame, text="Search by Code or Desc. :")
    search_label.pack(anchor="w", pady=5)
    search_entry = customtkinter.CTkEntry(left_frame)
    search_entry.pack(anchor="w", pady=5)

    def search_event():
        search_val = search_entry.get()

        if not search_val:
            load_events()
            return

        for row in event_tree.get_children():
            event_tree.delete(row)

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                search_query = """
                    SELECT 
                        e.event_code,
                        e.event_description,
                        e.event_type,
                        e.event_status,
                        (SELECT COUNT(*) FROM event_participant ep WHERE ep.event_code = e.event_code),
                        (SELECT COUNT(*) FROM volunteer_event ve WHERE ve.event_code = e.event_code)
                    FROM events e
                    WHERE CAST(e.event_code AS TEXT) LIKE %s OR e.event_description ILIKE %s
                    ORDER BY e.event_code
                """
                search_pattern = f'%{search_val}%'
                cur.execute(search_query, (search_pattern, search_pattern))
                rows = cur.fetchall()
                if not rows:
                    event_tree.insert("", tk.END, values=("No results", f"found for '{search_val}'", "", "", "", ""))
                else:
                    for row in rows:
                        event_tree.insert("", tk.END, values=row)
            except Exception as e:
                event_tree.insert("", tk.END, values=("Error", "searching", str(e), "", "", ""))
            finally:
                cur.close()
                conn.close()

    search_button = customtkinter.CTkButton(left_frame, text="Search", command=search_event)
    search_button.pack(pady=5)

    refresh_button = customtkinter.CTkButton(left_frame, text="Show All", command=lambda: load_events())
    refresh_button.pack(pady=5)

    delete_button = customtkinter.CTkButton(left_frame, text="Delete Event", command=delete_event)
    delete_button.pack(pady=5)

    update_button = customtkinter.CTkButton(left_frame, text="Update", command=update_event)
    update_button.pack(pady=5)

    details_button = customtkinter.CTkButton(left_frame, text="Show Event Details", command=lambda: show_event_details(event_window))
    details_button.pack(pady=5)

    def go_back():
        event_window.destroy()
        main_window.deiconify()

    back_button = customtkinter.CTkButton(
        left_frame,
        text="Back",
        fg_color="#cc3333", 
        text_color="white",
        hover_color="#d94d4d",
        command=go_back
    )
    back_button.pack(side="bottom", pady=5)

    # ===================== Right Panel (Treeview) ===================== #
    right_frame = customtkinter.CTkFrame(event_window, corner_radius=0)
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 15, "bold"))
    style.configure("Treeview", font=("Helvetica", 15), rowheight=30)

    # Define the columns for the Treeview
    tree_columns = (
        "event_code",
        "event_description",
        "event_type",
        "event_status",
        "participant_count",
        "volunteer_count"
    )
    event_tree = ttk.Treeview(right_frame, columns=tree_columns, show="headings")
    event_tree.heading("event_code", text="Event Code")
    event_tree.heading("event_description", text="Description")
    event_tree.heading("event_type", text="Type")
    event_tree.heading("event_status", text="Status")
    event_tree.heading("participant_count", text="Participants")
    event_tree.heading("volunteer_count", text="Volunteers")

    event_tree.column("event_code", width=80, anchor="center")
    event_tree.column("event_description", width=160, anchor="center")
    event_tree.column("event_type", width=150, anchor="center")
    event_tree.column("event_status", width=100, anchor="center")
    event_tree.column("participant_count", width=120, anchor="center")
    event_tree.column("volunteer_count", width=120, anchor="center")
    event_tree.pack(expand=True, fill="both")
    

    def populate_fields(event):
        """
        Populates the left panel's input fields with the selected row's data.
        Ignores participant_count and volunteer_count (the last two columns).
        """
        selected_item = event_tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = event_tree.item(item, "values")
        # values = [event_code, event_description, event_type, event_status, participant_count, volunteer_count]

        clear_fields()
        event_code_entry.insert(0, values[0])
        event_desc_entry.insert(0, values[1])
        event_type_entry.insert(0, values[2])
        event_status_entry.insert(0, values[3])

    event_tree.bind("<ButtonRelease-1>", populate_fields)

    # Load all existing events when the window opens
    load_events()



#going to remove this line so that it only starts running from the main
#if __name__ == "__main__":
#    main_window = customtkinter.CTk()
 #   open_event_window(main_window)
  #  main_window.mainloop()