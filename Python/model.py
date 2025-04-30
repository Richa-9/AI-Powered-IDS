import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# Load the existing dataset from CSV
df = pd.read_csv("CSV/ids_dataset.csv")

# Ensure the dataset is correctly loaded
print("Sample Data:")
print(df.head())

# Preprocessing
# Drop unnecessary columns
df = df.drop(columns=["Source IP", "Destination IP", "Attack Type"])

# One-hot encode categorical 'Protocol' column
df = pd.get_dummies(df, columns=["Protocol"])

# Separate features (X) and target labels (y)
X = df.drop(columns=["Is Attack"])
y = df["Is Attack"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the XGBoost classifier
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_train, y_train)

# Model evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy (XGBoost): {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model using XGBoost's native method (safer than pickle)
model.save_model("ids_model.json")
print("\nModel saved as 'ids_model.json'")
