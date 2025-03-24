import pandas as pd

# Load the dataset
df = pd.read_csv("car_data.csv")

# Convert New_Price to numeric after replacing 'Lakh' and other text
def convert_price(value):
    if isinstance(value, str):
        value = value.replace('Lakh', '').replace(',', '').strip()
        try:
            return float(value) * 100000  # Convert Lakh to actual value
        except ValueError:
            return None
    return value

df["New_Price"] = df["New_Price"].apply(convert_price)
df["New_Price"] = pd.to_numeric(df["New_Price"], errors='coerce')

df["Price"] = pd.to_numeric(df["Price"], errors='coerce')

# Drop rows where New_Price or Price is missing to prevent incorrect calculations
df.dropna(subset=["New_Price", "Price"], inplace=True)

# Calculate depreciation rate
df["depreciation_rate"] = ((df["New_Price"] - df["Price"]) / df["New_Price"]) * 100

# Ensure no NaN or negative depreciation rates
df["depreciation_rate"] = df["depreciation_rate"].fillna(0)

df["depreciation_rate"] = df["depreciation_rate"].clip(lower=0)


# Function to extract numeric mileage values
def extract_mileage(value):
    try:
        return float(value.split()[0]) if isinstance(value, str) else None
    except:
        return None

# Apply function to convert 'Mileage' to numeric
df["Mileage"] = df["Mileage"].apply(extract_mileage)

# Drop rows where 'Mileage' is NaN (optional, if needed)
df.dropna(subset=["Mileage"], inplace=True)


current_year = 2025
df["car_age"] = current_year - df["Year"]

# Save the cleaned dataset
df.to_csv("car_data_cleaned.csv", index=False)

# Print overview
print("Final Processed Data Overview:")
print(df.head())
