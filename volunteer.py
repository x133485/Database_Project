import customtkinter
import tkinter as tk
from tkinter import ttk
from db_connect import connect_to_database  

from volunteer_event import open_assign_event_window

def open_volunteer_window(main_window):
    main_window.withdraw()

    volunteer_window = customtkinter.CTkToplevel()
    volunteer_window.title("Volunteer Management")
    width = 1200
    height = 700
    screen_width = volunteer_window.winfo_screenwidth()
    screen_height = volunteer_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    volunteer_window.geometry(f"{width}x{height}+{x}+{y}")

    # ===================== Left Frame (Input & Actions) ===================== #
    left_frame = customtkinter.CTkScrollableFrame(volunteer_window, width=150, corner_radius=0)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # --- Volunteer ID ---
    volun_id_label = customtkinter.CTkLabel(left_frame, text="Volunteer ID:")
    volun_id_label.pack(anchor="w", pady=5)
    volun_id_entry = customtkinter.CTkEntry(left_frame)
    volun_id_entry.pack(anchor="w", pady=5)

    # --- Name ---
    name_label = customtkinter.CTkLabel(left_frame, text="Name:")
    name_label.pack(anchor="w", pady=5)
    name_entry = customtkinter.CTkEntry(left_frame)
    name_entry.pack(anchor="w", pady=5)

    # --- Address ---
    address_label = customtkinter.CTkLabel(left_frame, text="Address:")
    address_label.pack(anchor="w", pady=5)
    address_entry = customtkinter.CTkEntry(left_frame)
    address_entry.pack(anchor="w", pady=5)

    # --- Phone Number ---
    phone_label = customtkinter.CTkLabel(left_frame, text="Phone Number:")
    phone_label.pack(anchor="w", pady=5)
    phone_entry = customtkinter.CTkEntry(left_frame)
    phone_entry.pack(anchor="w", pady=5)

    # ----------------- Save (Insert) Function ----------------- #
    def save_volunteer():
        volun_id_val = volun_id_entry.get()
        name_val = name_entry.get()
        address_val = address_entry.get()
        phone_val = phone_entry.get()

        if not volun_id_val:
            print("Volunteer ID can't be empty!")
            return

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO volunteers (volun_id, name, address, telephonenumber)
                    VALUES (%s, %s, %s, %s)
                """
                cur.execute(insert_query, (volun_id_val, name_val, address_val, phone_val))
                conn.commit()
                print("Volunteer stored successfully!")
                
                # Clear all input fields after successful save
                volun_id_entry.delete(0, 'end')
                name_entry.delete(0, 'end')
                address_entry.delete(0, 'end')
                phone_entry.delete(0, 'end')
                
                # Refresh the Treeview
                load_volunteers()
            except Exception as e:
                print("Error in inserting data:", e)
            finally:
                cur.close()
                conn.close()

    save_button = customtkinter.CTkButton(left_frame, text="Save", command=save_volunteer)
    save_button.pack(pady=10)

    # ----------------- Search Section ----------------- #
    search_label = customtkinter.CTkLabel(left_frame, text="Search by ID or Name:")
    search_label.pack(anchor="w", pady=5)
    search_entry = customtkinter.CTkEntry(left_frame)
    search_entry.pack(anchor="w", pady=5)

    def search_volunteer():
        search_val = search_entry.get()

        # If no search value is provided, load all volunteers
        if not search_val:
            load_volunteers()
            return

        # Clear the Treeview first
        for row in volunteer_tree.get_children():
            volunteer_tree.delete(row)

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                search_query = """
                    SELECT CAST(volun_id AS TEXT), name, address, telephonenumber
                    FROM volunteers
                    WHERE CAST(volun_id AS TEXT) LIKE %s OR name ILIKE %s
                    ORDER BY volun_id
                """
                # Using LIKE for ID and ILIKE for case-insensitive name search
                search_pattern = f'%{search_val}%'
                cur.execute(search_query, (search_pattern, search_pattern))
                rows = cur.fetchall()
                for row in rows:
                    volunteer_tree.insert("", tk.END, values=row)
                if not rows:
                    print("No volunteer found with the given ID or Name.")
            except Exception as e:
                print("Error in searching data:", e)
            finally:
                cur.close()
                conn.close()

    search_button = customtkinter.CTkButton(left_frame, text="Search", command=search_volunteer)
    search_button.pack(pady=5)

    refresh_button = customtkinter.CTkButton(left_frame, text="Show All", command=lambda: load_volunteers())
    refresh_button.pack(pady=5)


    # ----------------- Delete Section ----------------- #
    def delete_volunteer():

        selected_item = volunteer_tree.selection()
        if not selected_item:
            print("No row selected for deletion!")
            return

        # Get the first selected item
        item = selected_item[0]
        # Extract the volunteer ID from the row values (assuming ID is the first column)
        values = volunteer_tree.item(item, "values")
        volun_id_val = values[0]

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                delete_query = """
                    DELETE FROM volunteers
                    WHERE volun_id = %s
                """
                cur.execute(delete_query, (volun_id_val,))
                conn.commit()
                print("Volunteer deleted successfully!")
                load_volunteers()
            except Exception as e:
                print("Error in deleting data:", e)
            finally:
                cur.close()
                conn.close()

    delete_button = customtkinter.CTkButton(left_frame, text="Delete", command=delete_volunteer)
    delete_button.pack(pady=5)


    def load_for_update():
        """
        When user selects a row and clicks 'Update Event',
        fill the left panel entries with the selected row's data.
        """
        selected_item = volunteer_tree.selection()
        if not selected_item:
            print("Please select an event to Modify!")
            return
            
        values = volunteer_tree.item(selected_item[0])['values']
        # values[0] = zero-padded code from the Treeview
        volun_id_entry.delete(0, 'end')
        name_entry.delete(0, 'end')
        address_entry.delete(0, 'end')
        phone_entry.delete(0, 'end')
        
        
        volun_id_entry.insert(0, values[0])   
        name_entry.insert(0, values[1])
        address_entry.insert(0, values[2])
        phone_entry.insert(0, values[3])


    def update_volunteer():
        """
        Updates the selected volunteer's data in the database.
        """
        if not volun_id_entry.get():
            # If the user clicked 'Update Event' with nothing typed, let's load the data from selection
            load_for_update()
            return
        
        volun_id_val = volun_id_entry.get()
        name_val = name_entry.get()
        address_val = address_entry.get()
        phone_val = phone_entry.get()

        if not volun_id_val or not name_val or not address_val or not phone_val:
            print("All fields are required for updating!")
            return

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                update_query = """
                    UPDATE volunteers 
                    SET name = %s, address = %s, telephonenumber = %s
                    WHERE volun_id = %s
                """
                cur.execute(update_query, (name_val, address_val, phone_val, volun_id_val))
                conn.commit()
                print("Volunteer updated successfully!")
                
                # Clear the entries
                volun_id_entry.delete(0, 'end')
                name_entry.delete(0, 'end')
                address_entry.delete(0, 'end')
                phone_entry.delete(0, 'end')
                
                # Refresh the display
                load_volunteers()
            except Exception as e:
                print("Error updating volunteer:", e)
            finally:
                cur.close()
                conn.close()

    def clear_fields():
        """
        Clears the input fields in the left panel.
        """
        volun_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)

    # Update button remains the same but will now trigger the new two-step process
    update_button = customtkinter.CTkButton(left_frame, text="Update", command=update_volunteer)
    update_button.pack(pady=5)

    #---Assign Event ---
    assign_event_button = customtkinter.CTkButton(left_frame, text="Assign Event", command=open_assign_event_window)
    assign_event_button.pack(pady=10)

    def go_back():
        volunteer_window.destroy()
        main_window.deiconify()

    back_button = customtkinter.CTkButton(
        left_frame,
        text="Back",
        fg_color="#cc3333", 
        text_color="white",
        hover_color="#d94d4d",
        command=go_back
    )
    back_button.pack(side="bottom", pady=20)

    # ===================== Right Frame (Treeview) ===================== #
    right_frame = customtkinter.CTkFrame(volunteer_window, corner_radius=0)
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 16, "bold"))  # set character size 16 and bold.
    style.configure("Treeview", font=("Helvetica", 18), rowheight=30)  
    
    # Define Treeview columns
    tree_columns = ("volun_id", "name", "address", "telephonenumber")
    volunteer_tree = ttk.Treeview(right_frame, columns=tree_columns, show="headings")
    volunteer_tree.heading("volun_id", text="Volunteer ID")
    volunteer_tree.heading("name", text="Name")
    volunteer_tree.heading("address", text="Address")
    volunteer_tree.heading("telephonenumber", text="Phone Number")
    volunteer_tree.pack(expand=True, fill="both")

    def on_tree_select(event):
        """
        Populates the input fields with the selected row's data.
        """
        selected_item = volunteer_tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = volunteer_tree.item(item, "values")

        clear_fields()
        volun_id_entry.insert(0, str(values[0]))  # Convert to string to preserve leading zeros
        name_entry.insert(0, values[1])
        address_entry.insert(0, values[2])
        phone_entry.insert(0, values[3])

    # Bind tree select event
    volunteer_tree.bind("<ButtonRelease-1>", on_tree_select)

    def load_volunteers():
        """
        Loads and displays all volunteers from the database into the Treeview.
        """
        # Clear any existing rows in the Treeview
        for row in volunteer_tree.get_children():
            volunteer_tree.delete(row)

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                select_query = """
                    SELECT volun_id, name, address, telephonenumber
                    FROM volunteers
                    ORDER BY volun_id
                """
                cur.execute(select_query)
                rows = cur.fetchall()
                for row in rows:
                    volunteer_tree.insert("", tk.END, values=row)
            except Exception as e:
                print("Error in query:", e)
            finally:
                cur.close()
                conn.close()

    # Load all volunteers when the window opens
    load_volunteers()

