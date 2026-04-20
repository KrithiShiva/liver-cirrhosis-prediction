import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from data_preprocessing import load_and_preprocess_data  # Import fixed preprocessing
import joblib

# Load preprocessed data.
df, scaler = load_and_preprocess_data()

# Ensure 'Prediction' is the target variable
X = df.drop(columns=["Prediction"])  # Features
y = df["Prediction"]  # Target



# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save Model & Scaler
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("scaler.pkl", "wb") as file:
    pickle.dump(scaler, file)


# Save the trained model
joblib.dump(model, "liver_cirrhosis_model.pkl")

# Save the scaler (used for data preprocessing)
joblib.dump(scaler, "scaler.pkl")


print("Model and scaler saved successfully!")

print("Number of Features Used for Training:", X_train.shape[1])


