import customtkinter as ctk
import tkinter.messagebox as messagebox
import time
import os
import pandas as pd

def show_login_successful(admin_window):
    # Close the admin login window first
    admin_window.destroy()

    # Create a new success window
    success_window = ctk.CTkToplevel()
    success_window.title("LOGIN SUCCESSFUL")
    success_window.geometry("400x300")

    # Centre the window
    success_window.update_idletasks()
    window_width = 400
    window_height = 300
    screen_width = success_window.winfo_screenwidth()
    screen_height = success_window.winfo_screenheight()
    
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    success_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    success_window.resizable(False, False)

    # Success message
    success_label = ctk.CTkLabel(success_window, text="LOGIN SUCCESSFUL", font=("Arial", 20, "bold"), text_color="green")
    success_label.place(relx=0.5, rely=0.4, anchor="center")

    # Update the window to show the message
    success_window.update()
    
    # Wait for 2 seconds before showing report options
    success_window.after(2000, lambda: show_report_options(success_window))

def show_report_options(success_window):
    # Destroy success window
    success_window.destroy()

    # Create report selection window
    report_window = ctk.CTkToplevel()
    report_window.title("Select Report Type")
    report_window.geometry("400x300")

    # Centre the window
    report_window.update_idletasks()
    window_width = 400
    window_height = 300
    screen_width = report_window.winfo_screenwidth()
    screen_height = report_window.winfo_screenheight()
    
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    report_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    report_window.resizable(False, False)

    # Title
    report_label = ctk.CTkLabel(report_window, text="Select Report Type", font=("Arial", 20, "bold"))
    report_label.place(relx=0.5, rely=0.3, anchor="center")

    # Open Excel Button
    excel_btn = ctk.CTkButton(report_window, text="Open Report in Excel", command=open_excel_file)
    excel_btn.place(relx=0.5, rely=0.5, anchor="center")

    # Open Power BI Button
    powerbi_btn = ctk.CTkButton(report_window, text="Open Report in Power BI", command=open_power_bi)
    powerbi_btn.place(relx=0.5, rely=0.7, anchor="center")

    report_window.grab_set()

def open_excel_file():
    # Create a sample Excel file (if it doesn’t exist)
    file_path = "test_record.xlsx"
    if not os.path.exists(file_path):
        data = {
            "ID": [1, 2, 3],
            "Name": ["Admin1", "Admin2", "Admin3"],
            "Role": ["Manager", "Supervisor", "Clerk"]
        }
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)  # Save as Excel

    # Open the Excel file
    os.startfile(file_path)  # Opens in default Excel program

def open_power_bi():
    # Path to Power BI Desktop
    power_bi_report = r"C:\\Users\\ADMIN\Documents\\REPORT.pbix"  # Change this to the actual file name

    if os.path.exists(power_bi_report):
        os.startfile(power_bi_report)  # Open Power BI with the report
    else:
        print(f"Error: File not found at {power_bi_report}")  # Debugging output
        
   
def show_admin_login():
    admin_window = ctk.CTkToplevel()
    admin_window.title("Admin Login")
    admin_window.geometry("400x500")

    # Center the window
    admin_window.update_idletasks()
    window_width = 400
    window_height = 500
    screen_width = admin_window.winfo_screenwidth()
    screen_height = admin_window.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    admin_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    admin_window.resizable(False, False)

    # Admin Login Label
    admin_label = ctk.CTkLabel(admin_window, text="Admin Login", font=("Arial", 24, "bold"), text_color="blue")
    admin_label.place(relx=0.5, rely=0.2, anchor="center")

    # Username Entry
    username_entry = ctk.CTkEntry(admin_window, placeholder_text="Username", width=250)
    username_entry.place(relx=0.5, rely=0.4, anchor="center")

    # Password Entry
    password_entry = ctk.CTkEntry(admin_window, placeholder_text="Password", show="*", width=250)
    password_entry.place(relx=0.5, rely=0.55, anchor="center")

    # Function for login button action
    def on_login_button_click():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "password":  # Example credentials
            show_login_successful(admin_window)
        else:
            messagebox.showwarning("Invalid Login", "Invalid username or password!")  # Show error message

    # Login Button
    login_btn = ctk.CTkButton(admin_window, text="Login", fg_color="blue", text_color="white", corner_radius=10, command=on_login_button_click)
    login_btn.place(relx=0.5, rely=0.7, anchor="center")

    admin_window.grab_set()
