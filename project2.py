import os
import pandas as pd
import time

# File path
FILE_PATH = "data.xlsx"

# Create a sample DataFrame if the Excel file doesn't exist
try:
    df = pd.read_excel(FILE_PATH, engine="openpyxl")
except FileNotFoundError:
    # Sample data
    data = {
        "Price": [10, 20, 30],
        "Quantity": [1, 2, 3],
        "Total": [None, None, None]  # Empty Total for testing
    }
    df = pd.DataFrame(data)
    df.to_excel(FILE_PATH, index=False, engine="openpyxl")
    print("✅ Excel file 'data.xlsx' created successfully!")

# Infinite loop to check every minute
while True:
    # Reload the Excel file
    df = pd.read_excel(FILE_PATH, engine="openpyxl")

    # Check if "Total" column exists; if not, create it
    if "Total" not in df.columns:
        df["Total"] = None  # Create an empty column if missing

    # Find rows where "Total" is empty
    empty_totals = df["Total"].isna()

    if empty_totals.any():  # If there are empty totals
        # Ensure "Price" and "Quantity" columns exist
        if "Price" in df.columns and "Quantity" in df.columns:
            df.loc[empty_totals, "Total"] = df["Price"] * df["Quantity"]

            # Save the updated Excel file
            df.to_excel(FILE_PATH, index=False, engine="openpyxl")
            print("✅ Updated totals in the Excel file.")

            # Open the Excel file automatically
            os.startfile(FILE_PATH)

        else:
            print("❌ 'Price' or 'Quantity' columns are missing.")

    else:
        print("⏳ Waiting for new price and quantity values...")

    # Wait 1 minute before checking again
    time.sleep(60)
