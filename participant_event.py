import customtkinter
import tkinter as tk
from db_connect import connect_to_database

def open_participant_event_window():
    assign_window = customtkinter.CTkToplevel()
    assign_window.title("Assign Participant to Event")
    assign_window.geometry("400x300")
    assign_window.attributes('-topmost', True)
    assign_window.lift()
    assign_window.focus_force()
    assign_window.grab_set()

    # Fetch available participants for the dropdown（同时显示 participant_id 和 name，并按 participant_id 升序排序）
    participant_options = []
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT participant_id, name FROM participant ORDER BY participant_id ASC")
            rows = cur.fetchall()
            participant_options = [f"{row[0]} - {row[1]}" for row in rows]
        except Exception as e:
            print("Error fetching participants for dropdown:", e)
        finally:
            cur.close()
            conn.close()
    participant_options = ["None - No Participant"] + participant_options
    participant_dropdown = customtkinter.CTkOptionMenu(assign_window, values=participant_options)
    participant_dropdown.set(participant_options[0])
    participant_dropdown.pack(anchor="w", padx=10, pady=5)

    # Fetch available events for the dropdown（同时显示 event_code 和 event_description，并按 event_code 升序排序）
    event_options = []
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT event_code, event_description FROM events ORDER BY event_code ASC")
            rows = cur.fetchall()
            event_options = [f"{row[0]} - {row[1]}" for row in rows]
        except Exception as e:
            print("Error fetching events for dropdown:", e)
        finally:
            cur.close()
            conn.close()
    event_options = ["None - No Event"] + event_options
    event_dropdown = customtkinter.CTkOptionMenu(assign_window, values=event_options)
    event_dropdown.set(event_options[0])
    event_dropdown.pack(anchor="w", padx=10, pady=5)

    def assign_participant_to_event():
        participant_selection = participant_dropdown.get()
        event_selection = event_dropdown.get()
        participant_id = None if participant_selection.startswith("None") else participant_selection.split(" - ")[0]
        event_code = None if event_selection.startswith("None") else event_selection.split(" - ")[0]
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO event_participant (participant_id, event_code)
                    VALUES (%s, %s)
                """
                cur.execute(insert_query, (participant_id, event_code))
                conn.commit()
                print("Participant assigned to event successfully!")
                assign_window.destroy()
            except Exception as e:
                print("Error assigning participant to event:", e)
            finally:
                cur.close()
                conn.close()

    assign_button = customtkinter.CTkButton(assign_window, text="Assign Participant to Event", command=assign_participant_to_event)
    assign_button.pack(padx=10, pady=10)
