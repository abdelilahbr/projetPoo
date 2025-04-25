import schedule
import time
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("google-sheets-credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

# Google Sheets ID and sheet name
SPREADSHEET_ID = "12xaCDUaTwnMPmY2WLseQ5Lru1S8rFRFMxD9aupesvgI"  
SHEET_NAME = "supermarket_sales - Sheet1"  

def update_total_column():
    """Check Google Sheets, calculate total if needed, and update it."""
    try:
        # Open sheet
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

        # Read data from Google Sheets      
        data = sheet.get_all_values()

        if not data:  # If the sheet is empty, do nothing
            print("🔍 Sheet is empty. Waiting for data...")
            return

        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])  # Skip headers

        # Ensure required columns exist
        required_columns = {"Price", "Quantity", "Total", "Tax 5%"}
        if not required_columns.issubset(df.columns):
            print(f"❌ Missing columns: {required_columns - set(df.columns)}")
            return

        # Convert to numeric, keeping NaN for missing values
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
        df["Tax 5%"] = pd.to_numeric(df["Tax 5%"], errors="coerce")
        df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

        # Identify rows needing updates
        rows_tax = df["Tax 5%"].isna()
        rows_total = df["Total"].isna()

        if rows_tax.any() or rows_total.any():
            # Update missing "Tax 5%" values
            df.loc[rows_tax, "Tax 5%"] = (df.loc[rows_tax, "Price"] / 100) * 5 * df.loc[rows_tax, "Quantity"]

            # Update missing "Total" values
            df.loc[rows_total, "Total"] = df.loc[rows_total, "Price"] * df.loc[rows_total, "Quantity"] + df.loc[rows_total, "Tax 5%"]

            # Prepare updates (only modified cells)
            updates = []
            for i in df.index:
                if rows_tax[i]:
                    updates.append({
                        "range": f"D{i+2}",  # Assuming "Tax 5%" is in column D
                        "values": [[df.at[i, "Tax 5%"]]]
                    })
                if rows_total[i]:
                    updates.append({
                        "range": f"E{i+2}",  # Assuming "Total" is in column E
                        "values": [[df.at[i, "Total"]]]
                    })

            # Send batch updates
            if updates:
                sheet.batch_update(updates)
                print("✅ Total and Tax updated successfully!")

        else:
            print("⏳ No new calculations needed. Waiting for updates...")

    except Exception as e:
        print(f"❌ Error: {e}")

# Schedule the task to run every 10s
schedule.every(1).seconds.do(update_total_column)

print("⏳ Automation started... Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(2)
