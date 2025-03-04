import customtkinter
import tkinter as tk
from db_connect import connect_to_database

def open_coaching_event_window():
    assign_window = customtkinter.CTkToplevel()
    assign_window.title("Assign Coach to Event")
    assign_window.geometry("400x300")
    assign_window.attributes('-topmost', True)
    assign_window.lift()
    assign_window.focus_force()
    assign_window.grab_set()

    # Fetch available coaches for the dropdown，显示 "coach_id - name"，并按 coach_id 排序
    coach_options = []
    conn = connect_to_database()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT coach_id, name FROM coaching ORDER BY coach_id ASC")
            rows = cur.fetchall()
            coach_options = [f"{row[0]} - {row[1]}" for row in rows]
        except Exception as e:
            print("Error fetching coaches for dropdown:", e)
        finally:
            cur.close()
            conn.close()
    coach_options = ["None - No Coach"] + coach_options
    coach_dropdown = customtkinter.CTkOptionMenu(assign_window, values=coach_options)
    coach_dropdown.set(coach_options[0])
    coach_dropdown.pack(anchor="w", padx=10, pady=5)

    # Fetch available events for the dropdown，显示 "event_code - event_description"，并按 event_code 排序
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

    def assign_coach_to_event():
        coach_selection = coach_dropdown.get()
        event_selection = event_dropdown.get()
        coach_id = None if coach_selection.startswith("None") else coach_selection.split(" - ")[0]
        event_code = None if event_selection.startswith("None") else event_selection.split(" - ")[0]
        conn = connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                insert_query = """
                    INSERT INTO coaching_event (coach_id, event_code)
                    VALUES (%s, %s)
                """
                cur.execute(insert_query, (coach_id, event_code))
                conn.commit()
                print("Coach assigned to event successfully!")
                assign_window.destroy()
            except Exception as e:
                print("Error assigning coach to event:", e)
            finally:
                cur.close()
                conn.close()

    assign_button = customtkinter.CTkButton(assign_window, text="Assign Coach to Event", command=assign_coach_to_event)
    assign_button.pack(padx=10, pady=10)
