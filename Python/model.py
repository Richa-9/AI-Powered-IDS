import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import pickle

# Load the existing dataset from CSV
df = pd.read_csv("CSV/ids_dataset.csv")

# Ensure the dataset is correctly loaded
print(df.head())

# Preprocessing
# Drop columns that are not needed for model training
df = df.drop(columns=["Source IP", "Destination IP", "Attack Type"])

# One-hot encode the 'Protocol' column
df = pd.get_dummies(df, columns=["Protocol"])

# Separate features (X) and target (y)
X = df.drop(columns=["Is Attack"])
y = df["Is Attack"]

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the XGBoost model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy (XGBoost): {accuracy:.4f}")
print(classification_report(y_test, y_pred))

# Save the trained model to a .pkl file
with open("ids_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model saved as 'ids_model.pkl'")
