import joblib
import pandas as pd

# Load the trained model and scaler
model = joblib.load("liver_cirrhosis_model.pkl")
scaler = joblib.load("scaler.pkl")

# Ensure input has the correct feature names (26 features)
feature_columns = [
    'Age', 'Alcohol Intake', 'Hepatitis B ', 'Hepatitis C ', 'Obesity',
    'Diabetes Result', 'Family history of cirrhosis/ hereditary', 'Neutrophils',
    'Lymphocytes', 'Monocytes', 'Eosinophils', 'Basophils', 'Hemoglobin', 'PCV',
    'MCV', 'Platelet Count', 'Total Bilirubin', 'Direct  Bilirubin',
    'Indirect  Bilirubin', 'AST /SGOT ', 'ALT/SGPT', 'Alkaline Phosphatase',
    'Total Protein', 'Albumin', 'Globulin'
]

import numpy as np
import joblib

# Load trained model and scaler
model = joblib.load("liver_cirrhosis_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_liver_cirrhosis(input_data):
    try:
        # Ensure input is a NumPy array
        input_array = np.array(input_data, dtype=np.float64)  
        print("Step 1 - Array Shape Before Reshape:", input_array.shape) 

        # FIX: If input is (1, 1, 25), squeeze to remove extra dimension
        input_array = np.squeeze(input_array)
        print("Step 2 - Shape After Squeeze:", input_array.shape) 

        #  Ensure input is (1, 25)
        if input_array.ndim == 1:
            input_array = input_array.reshape(1, -1)  

        print(" Step 3 - Final Input Shape for Model:", input_array.shape)

        # Scale input data
        input_data_scaled = scaler.transform(input_array)
        print(" Step 4 - Shape After Scaling:", input_data_scaled.shape)

        # Make prediction
        prediction = model.predict(input_data_scaled)

        return "Your test results indicate that you are suffering from liver cirrhosis. " 
        "This means your liver has developed significant scarring, which can affect its normal function over time." 
        "It is crucial to take immediate steps, such as following a healthy diet, avoiding alcoholand consulting a healthcare professional for proper management and treatment." if prediction[0] == 1 else "Your test results indicate no signs of liver cirrhosis. Continue healthy habits!"

    except Exception as e:
        print(" Error:", e)
        return f"Prediction Error: {e}"
