import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("car_data.csv")

# Print initial overview
print("Before Processing:\n", df.info())

# Convert 'New_Price' from Lakh format to numeric if needed
def convert_price(price):
    if isinstance(price, str):
        price = price.strip()
        if 'Lakh' in price:
            return float(price.replace('Lakh', '').strip()) * 100000  # Convert lakh to actual value
        elif 'Cr' in price:
            return float(price.replace('Cr', '').strip()) * 10000000  # Convert crore to actual value
        else:
            try:
                return float(price)
            except ValueError:
                return None  # Convert errors to NaN instead of removing
    return price  # Return as is if already numeric

df["New_Price"] = df["New_Price"].apply(convert_price)
df["Price"] = df["Price"].apply(convert_price)

# Print after conversion
print("\nAfter Conversion:\n", df[["New_Price", "Price"]].head())

# Fill missing values in New_Price with median (only if median exists)
if df["New_Price"].notna().sum() > 0:  # Check if any valid data exists
    df["New_Price"] = df["New_Price"].fillna(df["New_Price"].median())

# Drop rows where Price is missing
df.dropna(subset=["Price"], inplace=True)

# Print after filling missing values
print("\nAfter Filling Missing Values:\n", df[["New_Price", "Price"]].head())

# Calculate car age
current_year = 2025
df["car_age"] = current_year - df["Year"]

# Calculate depreciation rate
df["depreciation_rate"] = ((df["New_Price"] - df["Price"]) / df["New_Price"]) * 100

# Calculate mileage efficiency score (Unique Feature)
def mileage_efficiency(mileage):
    try:
        return float(mileage.split()[0])  # Extract numerical part of mileage
    except:
        return None

df["Mileage_Score"] = df["Mileage"].apply(mileage_efficiency)

df.dropna(subset=["Mileage_Score"], inplace=True)

# Print after full processing
print("\nFinal Processed Data Overview:\n", df.info())

# Save the modified dataset
df.to_csv("car_data_modified.csv", index=False)

# Display the first few rows to verify
print(df.head())
