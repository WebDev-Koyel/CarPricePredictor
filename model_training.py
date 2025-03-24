import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

# Load the cleaned dataset
df = pd.read_csv("car_data_cleaned.csv")

# Drop unnecessary columns
df.drop(columns=["S.No.", "Name", "Location"], inplace=True, errors="ignore")

# Fix 'Engine' and 'Power' conversion errors
df["Engine"] = df["Engine"].str.replace(" CC", "", regex=True).astype(float)
df["Power"] = df["Power"].str.replace(" bhp", "", regex=True).astype(float)

# Handle missing values (fill numeric columns with mean)
df.fillna(df.mean(), inplace=True)

# Define Features (X) and Target (y)
X = df.drop(columns=["Price"])  # Drop target column
y = df["Price"]

# Identify categorical & numerical columns
categorical_cols = ["Fuel_Type", "Transmission", "Owner_Ty"]
numerical_cols = [col for col in X.columns if col not in categorical_cols]

# One-Hot Encoding for categorical features
preprocessor = ColumnTransformer([
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)
], remainder="passthrough")

# Create a pipeline
model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(n_estimators=200, random_state=42))
])

# Split dataset into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model_pipeline.fit(X_train, y_train)

# Make predictions
preds = model_pipeline.predict(X_test)

# Evaluate performance
mae = mean_absolute_error(y_test, preds)
mse = mean_squared_error(y_test, preds)

print(f"🔥 Model Results:\nMAE: {mae:.2f}, MSE: {mse:.2f}")

# Save the preprocessor and model
joblib.dump(preprocessor, "preprocessor.pkl")
joblib.dump(model_pipeline, "best_model.pkl")

print("✅ Model and preprocessor saved successfully!")
