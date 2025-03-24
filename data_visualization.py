import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker



# Load the cleaned dataset
df = pd.read_csv("car_data_cleaned.csv")

# Check if the required columns exist
print(df.columns)  # Debugging step

# Ensure 'car_age' is present
if "car_age" not in df.columns:
    print("Error: 'car_age' column is missing! Check data_analysis.py.")
    exit()

# Ensure 'depreciation_rate' is present
if "depreciation_rate" not in df.columns:
    print("Error: 'depreciation_rate' column is missing! Check data_analysis.py.")
    exit()

# Plot scatter plot
plt.figure(figsize=(10,5))
plt.scatter(df["car_age"], df["depreciation_rate"])
plt.xlabel("Car Age (years)")
plt.ylabel("Depreciation Rate (%)")
plt.title("Car Age vs Depreciation Rate")
plt.grid()


# Fix y-axis formatting
ax = plt.gca()
ax.yaxis.set_major_formatter(mticker.PercentFormatter())


plt.show()
