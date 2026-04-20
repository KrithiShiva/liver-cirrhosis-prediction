import customtkinter as ctk
import numpy as np
import pickle
import requests
import tkinter as tk
import predict 
from tkinter import messagebox
import pandas as pd
import numpy as np
import os
import time  


def get_numeric_entry(entry_widget, default_value=0.0):
    """Convert entry field input to a float, default to 0.0 if empty."""
    value = entry_widget.get().strip()
    try:
        return float(value)  # Convert input to float
    except ValueError:
        return default_value  # If empty or invalid, return 0.0

# Flask chatbot API endpoint
FLASK_CHATBOT_URL =  "http://127.0.0.1:8000/chat"


# Initialize the main window
ctk.set_appearance_mode("light")  # Light or dark theme
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Liver Cirrhosis Prediction & AI Chatbot")
root.geometry("900x600")

# Glassmorphism Styling
def apply_glassmorphism(widget):
    widget.configure(fg_color=("#ffffff", "#1c1c1c"), corner_radius=20, border_width=2, border_color="#ffffff")

# Main Frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Left Section - Input Form with Tabs
input_frame = ctk.CTkFrame(main_frame, width=400)
input_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(input_frame, text="Liver Cirrhosis Prediction", font=("Arial", 25)).pack(pady=10)

# Tabs for Input Sections
tabview = ctk.CTkTabview(input_frame)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

# Create Tabs
tab1 = tabview.add("General Info")
tab2 = tabview.add("Blood Test")  # Define tab2 properly
tab3 = tabview.add("Liver Function")  # Define tab3 properly


# Tab 1: General Information

age_frame = ctk.CTkFrame(tab1)
age_frame.pack(fill='x', padx=10, pady=5)
ctk.CTkLabel(age_frame, text="Age:").pack(side="left", padx=10)
age_entry = ctk.CTkEntry(age_frame, width=150)
age_entry.pack(side="right", padx=10)

# Radio buttons for conditions with proper alignment
conditions = [
    ("Alcohol Intake", ["Yes", "No"]),
    ("Hepatitis B ", ["Positive", "Negative"]),
    ("Hepatitis C ", ["Positive", "Negative"]),
    ("Obesity", ["Yes", "No"]),
    ("Diabetes Result", ["Yes", "No"]),
    ("Family history of cirrhosis/ hereditary", ["Yes", "No"])
]

for condition, options in conditions:
    frame = ctk.CTkFrame(tab1)
    frame.pack(fill='x', padx=10, pady=5)
    ctk.CTkLabel(frame, text=condition, width=20).pack(side="left", padx=10)
    for option in options:
        ctk.CTkRadioButton(frame, text=option).pack(side="left", padx=10)

# Dictionary to store entry fields
blood_test_entries = {}

# Blood Test Inputs
for test in [ 'Neutrophils', 'Lymphocytes', 'Monocytes', 'Eosinophils', 'Basophils', 'Hemoglobin', 'PCV',
 'MCV', 'Platelet Count']:
    frame = ctk.CTkFrame(tab2)
    frame.pack(fill='x', padx=10, pady=5)
    ctk.CTkLabel(frame, text=test).pack(side="left", padx=10)
    
    # Create an entry and store it in dictionary
    blood_test_entries[test] = ctk.CTkEntry(frame, width=150)
    blood_test_entries[test].pack(side="right", padx=10)


# Dictionary to store liver function test entries
liver_test_entries = {}

# Liver Function Test Inputs
for test in ['Total Bilirubin', 'Direct  Bilirubin', 'Indirect  Bilirubin','AST /SGOT ', 'ALT/SGPT', 
             'Alkaline Phosphatase', 'Total Protein', 'Albumin', 'Globulin']:
    frame = ctk.CTkFrame(tab3)
    frame.pack(fill='x', padx=10, pady=5)
    ctk.CTkLabel(frame, text=test).pack(side="left", padx=10)
    
    # Create an entry and store it in dictionary
    liver_test_entries[test] = ctk.CTkEntry(frame, width=150)
    liver_test_entries[test].pack(side="right", padx=10)

# Define StringVar variables for conditions
hep_b_var = ctk.StringVar(value="Negative")
hep_c_var = ctk.StringVar(value="Negative")
obesity_var = ctk.StringVar(value="No")
diabetes_var = ctk.StringVar(value="No")
alcohol_var = ctk.StringVar(value="No")
family_history_var = ctk.StringVar(value="No")

 #Ensure the feature order exactly matches the trained model
feature_columns = [
    'Age', 'Alcohol Intake', 'Hepatitis B ', 'Hepatitis C ', 'Obesity',
    'Diabetes Result', 'Family history of cirrhosis/ hereditary', 'Neutrophils',
    'Lymphocytes', 'Monocytes', 'Eosinophils', 'Basophils', 'Hemoglobin', 'PCV',
    'MCV', 'Platelet Count', 'Total Bilirubin', 'Direct  Bilirubin',
    'Indirect  Bilirubin', 'AST /SGOT ', 'ALT/SGPT', 'Alkaline Phosphatase',
    'Total Protein', 'Albumin', 'Globulin'
]

def get_numeric_entry(entry_widget, default_value=0.0):
    """Convert entry field input to a float, default to 0.0 if empty."""
    value = entry_widget.get().strip()  # Remove leading/trailing spaces
    try:
        return float(value)  # Convert input to float
    except ValueError:
        return default_value  # If empty or invalid, return default (0.0)


def save_data_to_excel(input_dict):
    file_path = "test_record.xlsx"
    df = pd.DataFrame([input_dict], columns=feature_columns)
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        updated_df = df
    updated_df.to_excel(file_path, index=False)
    print("Data saved successfully to", file_path)

def predict_and_display():
    try:
        # Ensure data collection follows the expected order
        input_dict = {
            'Age': int(age_entry.get().strip()) if age_entry.get().strip() else 0,
            'Alcohol Intake': 1 if alcohol_var.get() == "Yes" else 0,
            'Hepatitis B ': 1 if hep_b_var.get() == "Positive" else 0,  
            'Hepatitis C ': 1 if hep_c_var.get() == "Positive" else 0,  
            'Obesity': 1 if obesity_var.get() == "Yes" else 0,
            'Diabetes Result': 1 if diabetes_var.get() == "Yes" else 0,
            'Family history of cirrhosis/ hereditary': 1 if family_history_var.get() == "Yes" else 0,
            'Neutrophils': get_numeric_entry(blood_test_entries['Neutrophils']),
            'Lymphocytes': get_numeric_entry(blood_test_entries['Lymphocytes']),
            'Monocytes': get_numeric_entry(blood_test_entries['Monocytes']),
            'Eosinophils': get_numeric_entry(blood_test_entries['Eosinophils']),
            'Basophils': get_numeric_entry(blood_test_entries['Basophils']),
            'Hemoglobin': get_numeric_entry(blood_test_entries['Hemoglobin']),
            'PCV': get_numeric_entry(blood_test_entries['PCV']),
            'MCV': get_numeric_entry(blood_test_entries['MCV']),
            'Platelet Count': get_numeric_entry(blood_test_entries['Platelet Count']),
            'Total Bilirubin': get_numeric_entry(liver_test_entries['Total Bilirubin']),
            'Direct  Bilirubin': get_numeric_entry(liver_test_entries['Direct  Bilirubin']),  
            'Indirect  Bilirubin': get_numeric_entry(liver_test_entries['Indirect  Bilirubin']),
            'AST /SGOT ': get_numeric_entry(liver_test_entries['AST /SGOT ']),
            'ALT/SGPT': get_numeric_entry(liver_test_entries['ALT/SGPT']),
            'Alkaline Phosphatase': get_numeric_entry(liver_test_entries['Alkaline Phosphatase']),
            'Total Protein': get_numeric_entry(liver_test_entries['Total Protein']),
            'Albumin': get_numeric_entry(liver_test_entries['Albumin']),
            'Globulin': get_numeric_entry(liver_test_entries['Globulin'])
        }

        # Convert dictionary to DataFrame (Ensure correct column order)
        input_df = pd.DataFrame([input_dict], columns=feature_columns)

        # Debugging Print - Step 1: DataFrame shape
        print("Step 1 - Input DataFrame Shape:", input_df.shape)

        # Convert DataFrame to NumPy array
        input_array = np.array(input_df, dtype=np.float64)

        # Debugging Print - Step 2: Array shape before reshape
        print("Step 2 - Array Shape Before Reshape:", input_array.shape)

        # FIX: Remove any unnecessary dimension if present
        input_array = input_array.squeeze()  # Remove extra dimension if needed

        # Debugging Print - Step 3: Array shape after squeeze
        print("Step 3- Array Shape After Squeeze:", input_array.shape)

        # Ensure it's exactly (1, 25)
        if input_array.ndim == 1:
            input_array = input_array.reshape(1, -1)

        # Debugging Print - Step 4: Final Array shape
        print("Step 4 Final Input Shape for Model:", input_array.shape)
    
        print(" Raw Input Data:", input_dict)
        print(" Step 1 - Input DataFrame Shape:", input_df.shape)
        print(" Step 2 - Array Shape Before Reshape:", input_array.shape)
  


        # If input shape is incorrect, raise an error
        if input_array.shape != (1, 25):
            raise ValueError(f" Incorrect input shape: {input_array.shape}. Expected (1, 25).")
        
        # Ensure input has the correct shape (1, 25)
        if input_array.ndim == 3:
              input_array = input_array.squeeze(axis=0)  # Remove unnecessary dimension if (1, 1, 25)
        elif input_array.ndim == 1:
             input_array = input_array.reshape(1, -1)  # Ensure (1, 25)

        # Print for debugging
        print(" Final Shape Before Model:", input_array.shape)

        

        # Pass the correctly shaped input to the model
        prediction_result = predict.predict_liver_cirrhosis(input_array)
        
         # Create a result window with Glassmorphism effect
        result_window = ctk.CTkToplevel()
        result_window.geometry("600x300")
        result_window.title("Prediction Result")
        
        if prediction_result == "Affected":
            result_window.configure(bg="red")
            result_text = "We have analyzed your health data, and based on the results, there are strong indications that you may be suffering from liver cirrhosis."
            "It is extremely important that you consult a doctor as soon as possible. Early medical intervention can help prevent further complications. A specialist, such as a hepatologist, "
            "can guide you through the next steps, including further tests and treatment options"
        else:
            result_window.configure(bg="green")
            result_text = "You are not at risk. Maintain a healthy lifestyle."

        # Smooth Fade-In Effect
        for i in range(0, 101, 5):  
            result_window.attributes("-alpha", i / 100)
            result_window.update()
            time.sleep(0.03)

       
         # Display Result
        result_label = ctk.CTkLabel(result_window, text=result_text, font=("Arial", 18, "bold"), text_color="black")
        result_label.pack(pady=50)

        close_btn = ctk.CTkButton(result_window, text="CLOSE", fg_color="black", command=result_window.destroy)
        close_btn.pack(pady=20)

    except Exception as e:
        print(" Error:", e)
        messagebox.showerror("Prediction Error", f"An error occurred: {e}")



# Update the Predict button
submit_button = ctk.CTkButton(input_frame, text="Predict", command=predict_and_display)
submit_button.pack(pady=10)

# Prediction Result Label
result_label = ctk.CTkLabel(input_frame, text="", font=("Arial", 14))
result_label.pack(pady=10)

# Right Section - AI Chatbot
chat_frame = ctk.CTkFrame(main_frame, width=400)
chat_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(chat_frame, text="AI Chatbot", font=("Arial", 16)).pack(pady=10)
chat_display = ctk.CTkTextbox(chat_frame, height=200)
chat_display.pack(pady=5, fill='both', padx=10, expand=True)

chat_input = ctk.CTkEntry(chat_frame, placeholder_text="Ask a question...")
chat_input.pack(pady=5, fill='x', padx=10)


def send_message():
    user_input = chat_input.get()
    if not user_input.strip():
        return  # Ignore empty messages

    # Display user message (right-aligned)
    chat_display.insert("end", f"\nYou: {user_input}\n", "user_msg")
    chat_input.delete(0, "end")

    try:
        # Send user input to Flask chatbot API
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": user_input},
            timeout=20
        )
        response_data = response.json()

        # Extract chatbot response
        chatbot_reply = response_data.get("response", "No response from bot")

        # Display chatbot message (left-aligned)
        chat_display.insert("end", f"\nBot: {chatbot_reply}\n", "bot_msg")

    except requests.exceptions.RequestException as e:
        chat_display.insert("end", f"\nError: {str(e)}\n", "error_msg")

    # Auto-scroll to the latest message
    chat_display.yview("end")

# Apply text formatting styles
chat_display.tag_config("user_msg", justify="right", foreground="white", background="#25D366")  # Green for user
chat_display.tag_config("bot_msg", justify="left", foreground="black", background="#E5E5EA")  # Gray for bot
chat_display.tag_config("error_msg", justify="left", foreground="red")  # Red for errors

# Send Button - Fixed functionality issue
send_button = ctk.CTkButton(chat_frame, text="Send", command=send_message)
send_button.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()