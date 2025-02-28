import customtkinter
import tkinter as tk
from tkcalendar import DateEntry
from db_connect import connect_to_database

def open_assign_event_window():
    assign_window = customtkinter.CTkToplevel()
    assign_window.title("Assign Event to Volunteer")
    assign_window.geometry("400x400")
    assign_window.attributes('-topmost', True)
    assign_window.lift()         
    assign_window.focus_force()  
    assign_window.grab_set()     

    # Volunteer Dropdown: 查询 volunteer_id 和 name，并生成 "ID - Name" 格式
    volunteer_label = customtkinter.CTkLabel(assign_window, text="Select Volunteer:")
    volunteer_label.pack(anchor="w", padx=10, pady=5)
    volunteer_options = []
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT volun_id, name FROM volunteers ORDER BY volun_id ASC")
            rows = cur.fetchall()
            volunteer_options = [f"{row[0]} - {row[1]}" for row in rows]
        except Exception as e:
            print("Error fetching volunteer options:", e)
        finally:
            cur.close()
            conn.close()

    volunteer_options = ["None - No Volunteer"] + volunteer_options
    volun_dropdown = customtkinter.CTkOptionMenu(assign_window, values=volunteer_options)
    volun_dropdown.set(volunteer_options[0])
    volun_dropdown.pack(anchor="w", padx=10, pady=5)


    event_label = customtkinter.CTkLabel(assign_window, text="Select Event:")
    event_label.pack(anchor="w", padx=10, pady=5)
    event_options = []
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT event_code, event_description FROM events ORDER BY event_code ASC")
            rows = cur.fetchall()
            event_options = [f"{row[0]} - {row[1]}" for row in rows]
        except Exception as e:
            print("Error fetching event options:", e)
        finally:
            cur.close()
            conn.close()
    event_options = ["None - No Event"] + event_options
    event_dropdown = customtkinter.CTkOptionMenu(assign_window, values=event_options)
    event_dropdown.set(event_options[0])
    event_dropdown.pack(anchor="w", padx=10, pady=5)

    # Start Date selection using DateEntry
    start_date_label = customtkinter.CTkLabel(assign_window, text="Start Date:")
    start_date_label.pack(anchor="w", padx=10, pady=5)
    start_date_entry = DateEntry(assign_window, date_pattern='yyyy-mm-dd')
    start_date_entry.pack(anchor="w", padx=10, pady=5)

    # End Date selection using DateEntry
    end_date_label = customtkinter.CTkLabel(assign_window, text="End Date:")
    end_date_label.pack(anchor="w", padx=10, pady=5)
    end_date_entry = DateEntry(assign_window, date_pattern='yyyy-mm-dd')
    end_date_entry.pack(anchor="w", padx=10, pady=5)

    def assign_event():
        selected_volun = volun_dropdown.get()
        selected_event = event_dropdown.get()

        volunteer_id = None if selected_volun.startswith("None") else selected_volun.split(" - ")[0]
        event_code = None if selected_event.startswith("None") else selected_event.split(" - ")[0]
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()


        if volunteer_id is None and event_code is None:
            print("At least one of volunteer or event must be selected!")
            return

        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO volunteer_event (volun_id, event_code, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                """
                cur.execute(insert_query, (volunteer_id, event_code, start_date, end_date))
                conn.commit()
                print("Volunteer assigned to event successfully!")
                assign_window.destroy()
            except Exception as e:
                print("Error assigning event to volunteer:", e)
            finally:
                cur.close()
                conn.close()

    assign_button = customtkinter.CTkButton(assign_window, text="Assign", command=assign_event)
    assign_button.pack(padx=10, pady=10)

