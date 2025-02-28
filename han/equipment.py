import customtkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from db_connect import connect_to_database

def open_equipment_window(main_window):
    main_window.withdraw()

    equip_window = customtkinter.CTkToplevel()
    equip_window.title("Manage Equipment")
    width = 1200
    height = 700
    screen_width = equip_window.winfo_screenwidth()
    screen_height = equip_window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    equip_window.geometry(f"{width}x{height}+{x}+{y}")
    

    
    # ------------------- Left Panel: Input & Actions ------------------- #
    left_frame = customtkinter.CTkScrollableFrame(equip_window, width=150, corner_radius=0)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)
    
    # Equipment ID input (manually entered)
    id_label = customtkinter.CTkLabel(left_frame, text="Equipment ID:")
    id_label.pack(anchor="w", pady=5)
    id_entry = customtkinter.CTkEntry(left_frame)
    id_entry.pack(anchor="w", pady=5)
    
    # Equipment Description input
    desc_label = customtkinter.CTkLabel(left_frame, text="Description:")
    desc_label.pack(anchor="w", pady=5)
    desc_entry = customtkinter.CTkEntry(left_frame)
    desc_entry.pack(anchor="w", pady=5)
    
    # Equipment Value input
    value_label = customtkinter.CTkLabel(left_frame, text="Value:")
    value_label.pack(anchor="w", pady=5)
    value_entry = customtkinter.CTkEntry(left_frame)
    value_entry.pack(anchor="w", pady=5)
    
    # Equipment Quantity input
    quantity_label = customtkinter.CTkLabel(left_frame, text="Quantity:")
    quantity_label.pack(anchor="w", pady=5)
    quantity_entry = customtkinter.CTkEntry(left_frame)
    quantity_entry.pack(anchor="w", pady=5)
    
    # Event dropdown (showing event_code and event_description)
    event_label = customtkinter.CTkLabel(left_frame, text="Select Event:")
    event_label.pack(anchor="w", pady=5)
    
    event_options = []
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT event_code, event_description FROM events ORDER BY event_code")
            rows = cur.fetchall()
            event_options = [f"{row[0]} - {row[1]}" for row in rows]
        except Exception as e:
            print("Error fetching events for dropdown:", e)
        finally:
            cur.close()
            conn.close()
    # Add a "None" option at the beginning
    event_options = ["None - No Event"] + event_options
    
    event_dropdown = customtkinter.CTkOptionMenu(left_frame, values=event_options)
    event_dropdown.set(event_options[0])
    event_dropdown.pack(anchor="w", pady=5)
    
    # Save Equipment Button
    def save_equipment():
        description = desc_entry.get()
        value_text = value_entry.get()
        quantity_text = quantity_entry.get()
        selected_event = event_dropdown.get()

        if not description or not value_text or not quantity_text or not selected_event:
            print("All fields are required!")
            return

        try:
            value = float(value_text)
        except ValueError:
            print("Value must be a number!")
            return

        try:
            quantity = int(quantity_text)
        except ValueError:
            print("Quantity must be an integer!")
            return

        # Extract event_code from the dropdown if a valid event is selected.
        event_code = None
        if not selected_event.startswith("None"):
            event_code = selected_event.split(" - ")[0]

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO equipment (description, value, quantity, event_code)
                    VALUES (%s, %s, %s, %s)
                """
                cur.execute(insert_query, (description, value, quantity, event_code))
                conn.commit()
                print("Equipment added successfully!")
                load_equipment()
                # Clear input fields
                desc_entry.delete(0, tk.END)
                value_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                event_dropdown.set(event_options[0])
            except Exception as e:
                print("Error saving equipment:", e)
            finally:
                cur.close()
                conn.close()
    
    save_button = customtkinter.CTkButton(left_frame, text="Save Equipment", command=save_equipment)
    save_button.pack(pady=10)

    # ----------------- Search Section ----------------- #
    search_label = customtkinter.CTkLabel(left_frame, text="Search by ID or Desc. :")
    search_label.pack(anchor="w", pady=5)
    search_entry = customtkinter.CTkEntry(left_frame)
    search_entry.pack(anchor="w", pady=5)

    def search_equipment():
        search_val = search_entry.get()

        if not search_val:
            load_equipment()
            return

        for row in equipment_tree.get_children():
            equipment_tree.delete(row)

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                search_query = """
                    SELECT equipment_id, description, value, quantity, event_code
                    FROM equipment
                    WHERE CAST(equipment_id AS TEXT) LIKE %s OR description ILIKE %s
                    ORDER BY equipment_id
                """
                search_pattern = f'%{search_val}%'
                cur.execute(search_query, (search_pattern, search_pattern))
                rows = cur.fetchall()
                if not rows:
                    equipment_tree.insert("", tk.END, values=("No results", f"found for '{search_val}'", "", "", ""))
                else:
                    for row in rows:
                        equipment_tree.insert("", tk.END, values=row)
            except Exception as e:
                equipment_tree.insert("", tk.END, values=("Error", "searching", str(e), "", ""))
            finally:
                cur.close()
                conn.close()

    search_button = customtkinter.CTkButton(left_frame, text="Search", command=search_equipment)
    search_button.pack(pady=5)
    
    # ----------------- Refresh (Show All) Section ----------------- #
    refresh_button = customtkinter.CTkButton(left_frame, text="Show All", command=lambda: load_equipment())
    refresh_button.pack(pady=5)
    
    # Delete Equipment Button
    def delete_equipment():
        selected_item = equipment_tree.selection()
        if not selected_item:
            print("Please select an equipment to delete!")
            return
        item = selected_item[0]
        values = equipment_tree.item(item, "values")
        equipment_id = values[0]
        
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                delete_query = "DELETE FROM equipment WHERE equipment_id = %s"
                cur.execute(delete_query, (equipment_id,))
                conn.commit()
                print(f"Equipment {equipment_id} deleted successfully!")
                load_equipment()
            except Exception as e:
                print("Error deleting equipment:", e)
            finally:
                cur.close()
                conn.close()
    
    delete_button = customtkinter.CTkButton(left_frame, text="Delete Equipment", command=delete_equipment)
    delete_button.pack(pady=10)
    
    # Modify Equipment Button
    def modify_equipment():
        equipment_id = id_entry.get()
        description = desc_entry.get()
        value_text = value_entry.get()
        quantity_text = quantity_entry.get()
        selected_event = event_dropdown.get()
        
        if not equipment_id or not description or not value_text or not quantity_text or not selected_event:
            print("All fields are required for modification!")
            return
        
        try:
            value = float(value_text)
        except ValueError:
            print("Value must be a number!")
            return
        
        try:
            quantity = int(quantity_text)
        except ValueError:
            print("Quantity must be an integer!")
            return
        
        event_code = None
        if not selected_event.startswith("None"):
            event_code = selected_event.split(" - ")[0]
        
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                update_query = """
                    UPDATE equipment
                    SET description = %s, value = %s, quantity = %s, event_code = %s
                    WHERE equipment_id = %s
                """
                cur.execute(update_query, (description, value, quantity, event_code, equipment_id))
                conn.commit()
                print("Equipment modified successfully!")
                load_equipment()
                # Clear input fields after modification
                id_entry.delete(0, tk.END)
                desc_entry.delete(0, tk.END)
                value_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                event_dropdown.set(event_options[0])
            except Exception as e:
                print("Error modifying equipment:", e)
            finally:
                cur.close()
                conn.close()
    
    modify_button = customtkinter.CTkButton(left_frame, text="Update", command=modify_equipment)
    modify_button.pack(pady=10)
    
    # Check Equipment Button
    def check_equipment():
        conn = connect_to_database()
        events_without_equipment = []
        if conn:
            try:
                cur = conn.cursor()
                check_query = """
                    SELECT e.event_code, e.event_description
                    FROM events e
                    LEFT JOIN equipment eq ON e.event_code = eq.event_code
                    WHERE eq.equipment_id IS NULL
                    ORDER BY eq.event_code
                """
                cur.execute(check_query)
                events_without_equipment = cur.fetchall()
            except Exception as e:
                print("Error checking equipment for events:", e)
            finally:
                cur.close()
                conn.close()
        
        if events_without_equipment:
            msg = "The following events have no equipment assigned:\n"
            msg += "\n".join([f"{row[0]} - {row[1]}" for row in events_without_equipment])
            msg += "\n\nPlease add equipment for these events."
            messagebox.showinfo("Missing Equipment", msg, parent=equip_window)
        else:
            messagebox.showinfo("All Good", "All events have equipment assigned.", parent=equip_window)
    
    check_button = customtkinter.CTkButton(left_frame, text="Check Equipment", command=check_equipment)
    check_button.pack(pady=10)

    def show_event_equipment_summary():
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                # Query the view
                summary_query = "SELECT * FROM event_equipment_summary"
                cur.execute(summary_query)
                summary_data = cur.fetchall()

                # Display the data in a new window
                summary_window = customtkinter.CTkToplevel()
                summary_window.title("Event Equipment Summary")
                width = 600
                height = 400
                screen_width = summary_window.winfo_screenwidth()
                screen_height = summary_window.winfo_screenheight()
                x = (screen_width - width) // 2
                y = (screen_height - height) // 2
                summary_window.geometry(f"{width}x{height}+{x}+{y}")

                # Create a Treeview to display the summary
                summary_tree = ttk.Treeview(summary_window, columns=("event_code", "event_description", "total_value", "total_quantity"), show="headings")
                summary_tree.heading("event_code", text="Event Code", anchor="center")
                summary_tree.heading("event_description", text="Event Description", anchor="center")
                summary_tree.heading("total_value", text="Total Value", anchor="center")
                summary_tree.heading("total_quantity", text="Total Quantity", anchor="center")
                summary_tree.pack(expand=True, fill="both", padx=10, pady=10)

                # Insert data into the Treeview
                for row in summary_data:
                    summary_tree.insert("", tk.END, values=row)

            except Exception as e:
                print("Error fetching event equipment summary:", e)
                messagebox.showerror("Error", f"Error fetching event equipment summary: {e}", parent=equip_window)
            finally:
                cur.close()
                conn.close()
                
    summary_button = customtkinter.CTkButton(left_frame, text="Show Event Equipment Summary", command=show_event_equipment_summary)
    summary_button.pack(pady=10)

    def go_back():
        equip_window.destroy()
        main_window.deiconify()

    back_button = customtkinter.CTkButton(
        left_frame,
        text="Back",
        fg_color="#cc3333",  
        text_color="white",
        hover_color="#d94d4d",
        command=go_back
    )
    back_button.pack(side="bottom", pady=10)
    
    # ------------------- Right Panel: Equipment List (Treeview) ------------------- #
    right_frame = customtkinter.CTkFrame(equip_window, corner_radius=0)
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), anchor="center")
    style.configure("Treeview", font=("Helvetica", 12), rowheight=30)
    
    tree_columns = ("equipment_id", "description", "value", "quantity", "event_code")
    equipment_tree = ttk.Treeview(right_frame, columns=tree_columns, show="headings")
    equipment_tree.heading("equipment_id", text="ID", anchor="center")
    equipment_tree.heading("description", text="Description", anchor="center")
    equipment_tree.heading("value", text="Value", anchor="center")
    equipment_tree.heading("quantity", text="Quantity", anchor="center")
    equipment_tree.heading("event_code", text="Event Code", anchor="center")
    
    equipment_tree.column("equipment_id", anchor="center")
    equipment_tree.column("description", anchor="center")
    equipment_tree.column("value", anchor="center")
    equipment_tree.column("quantity", anchor="center")
    equipment_tree.column("event_code", anchor="center")
    
    equipment_tree.pack(expand=True, fill="both")
    
    # Load equipment from the database, ordered by equipment_id ascending
    def load_equipment():
        for row in equipment_tree.get_children():
            equipment_tree.delete(row)
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                select_query = """
                    SELECT equipment_id, description, value, quantity, event_code 
                    FROM equipment 
                    ORDER BY equipment_id
                """
                cur.execute(select_query)
                rows = cur.fetchall()
                for row in rows:
                    equipment_tree.insert("", tk.END, values=row)
            except Exception as e:
                print("Error fetching equipment data:", e)
            finally:
                cur.close()
                conn.close()
    
    load_equipment()
    
    # When a row is selected, populate the left panel fields with that row's data
    def populate_fields(event):
        selected_item = equipment_tree.selection()
        if not selected_item:
            return
        item = selected_item[0]
        values = equipment_tree.item(item, "values")
        id_entry.delete(0, tk.END)
        id_entry.insert(0, values[0])
        desc_entry.delete(0, tk.END)
        desc_entry.insert(0, values[1])
        value_entry.delete(0, tk.END)
        value_entry.insert(0, values[2])
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[3])
        if values[4] is None:
            event_dropdown.set("None - No Event")
        else:
            for option in event_options:
                if option.startswith(str(values[4])):
                    event_dropdown.set(option)
                    break
    
    equipment_tree.bind("<ButtonRelease-1>", populate_fields)


