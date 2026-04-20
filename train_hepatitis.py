import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Simulated dataset with assumed values
data = {
    "Age": np.random.randint(20, 80, 200),
    "Bilirubin": np.random.uniform(0.1, 3.5, 200),
    "ALT": np.random.randint(10, 100, 200),
    "AST": np.random.randint(15, 120, 200),
    "Albumin": np.random.uniform(3.0, 5.5, 200),
    "Total_Protein": np.random.uniform(6.0, 8.5, 200),
    "Hepatitis_Status": np.random.randint(0, 2, 200)  # 0 = No Hepatitis, 1 = Hepatitis detected
}

df = pd.DataFrame(data)

# Splitting dataset
X = df.drop("Hepatitis_Status", axis=1)
y = df["Hepatitis_Status"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Training model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
with open("hepatitis_model.pkl", "wb") as model_file:
    pickle.dump((scaler, model), model_file)

print("Model trained and saved as hepatitis_model.pkl")
