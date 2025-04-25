import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# Set up credentials and access to Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file('google-sheets-credentials.json', scopes=scopes)
client = gspread.authorize(creds)

# Open the Google Sheet
SPREADSHEET_ID = '1Nq25OXNiYXAsFBvbjdPnW44Cq2GAvifSqIZjnbXwrnA'  
sheet = client.open_by_key(SPREADSHEET_ID).sheet1  

# Read data into Pandas DataFrame (set header to first row)
df = get_as_dataframe(sheet, evaluate_formulas=True, header=0)

# Print column names to check if 'Price' exists
print("Columns in DataFrame:", df.columns)


# Ensure correct column names before processing
if "Price" in df.columns and "Quantity" in df.columns:
    df["Total"] = df["Price"] * df["Quantity"]  # Perform calculation
    print(df.head())  # Show updated data
else:
    print("Error: 'Price' or 'Quantity' column not found in Google Sheets!")

# Write updated DataFrame back to Google Sheets
set_with_dataframe(sheet, df)
print("Updated data successfully!")
spreadsheet = client.open_by_key(SPREADSHEET_ID)
sheet_names = [sheet.title for sheet in spreadsheet.worksheets()]
print("✅ Available Sheets:", sheet_names)

