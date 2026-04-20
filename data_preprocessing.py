import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
excel_file = "test_record.xlsx"

def load_and_preprocess_data():
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Age', 'Alcohol Intake', 'Hepatitis B ', 'Hepatitis C ', 'Obesity',
    'Diabetes Result', 'Family history of cirrhosis/ hereditary', 'Neutrophils',
    'Lymphocytes', 'Monocytes', 'Eosinophils', 'Basophils', 'Hemoglobin', 'PCV',
    'MCV', 'Platelet Count', 'Total Bilirubin', 'Direct  Bilirubin',
    'Indirect  Bilirubin', 'AST /SGOT ', 'ALT/SGPT', 'Alkaline Phosphatase',
    'Total Protein', 'Albumin', 'Globulin', 'Prediction'])
                                                                   

    # Handle missing values
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Encode categorical columns
    encoder = LabelEncoder()
    categorical_columns = ['Alcohol Intake', 'Hepatitis B ', 'Hepatitis C ', 'Obesity',
 'Diabetes Result', 'Family history of cirrhosis/ hereditary','Prediction']  # Include 'Prediction'

    for col in categorical_columns:
        if col in df.columns:
            df[col] = encoder.fit_transform(df[col].astype(str))  # Convert to numerical

    # Scale numerical features
    scaler = StandardScaler()
    numeric_columns = df.select_dtypes(include=['number']).columns.difference(["Prediction"])
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df, scaler

df, scaler = load_and_preprocess_data()
df.dropna(inplace=True)  # Remove any remaining NaN values
