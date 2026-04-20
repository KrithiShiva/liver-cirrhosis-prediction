import customtkinter as ctk
import pickle
import numpy as np
import pandas as pd
import subprocess
from tkinter import messagebox

# Load the trained model
with open("hepatitis_model.pkl", "rb") as model_file:
    scaler, model = pickle.load(model_file)

# Function to predict Hepatitis
def predict_hepatitis(age, bilirubin, alt, ast, albumin, total_protein):
    input_data = pd.DataFrame([[age, bilirubin, alt, ast, albumin, total_protein]],
                              columns=["Age", "Bilirubin", "ALT", "AST", "Albumin", "Total_Protein"])
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    return "Hepatitis Detected" if prediction[0] == 1 else "No Hepatitis Detected"

# Function to handle user input and prediction
def get_user_input():
    try:
        age = float(entry_age.get())
        bilirubin = float(entry_bilirubin.get())
        alt = float(entry_alt.get())
        ast = float(entry_ast.get())
        albumin = float(entry_albumin.get())
        total_protein = float(entry_total_protein.get())
    
        result = predict_hepatitis(age, bilirubin, alt, ast, albumin, total_protein)
        messagebox.showinfo("Prediction Result", result)
        
        # Automatically open Liver Cirrhosis Prediction UI
        subprocess.Popen(["python", "input.py"])
        root.destroy()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Initialize UI
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.geometry("500x600")
root.title("Hepatitis Prediction")

# Main Frame
frame = ctk.CTkFrame(root, corner_radius=10)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Hepatitis Prediction", font=("Arial", 24, "bold"), text_color="#F39C12").pack(pady=10)

# Input Fields
fields = ["Age", "Bilirubin", "ALT", "AST", "Albumin", "Total Protein"]
entries = {}
for field in fields:
    ctk.CTkLabel(frame, text=field + ":", font=("Arial", 14)).pack(pady=5)
    entry = ctk.CTkEntry(frame, width=250)
    entry.pack(pady=5)
    entries[field] = entry

entry_age = entries["Age"]
entry_bilirubin = entries["Bilirubin"]
entry_alt = entries["ALT"]
entry_ast = entries["AST"]
entry_albumin = entries["Albumin"]
entry_total_protein = entries["Total Protein"]

# Predict Button
predict_btn = ctk.CTkButton(frame, text="Predict Hepatitis", fg_color="#1C2833", hover_color="#2E86C1", 
                             text_color="white", width=200, command=get_user_input)
predict_btn.pack(pady=20)

root.mainloop()
