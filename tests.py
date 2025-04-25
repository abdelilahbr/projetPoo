import pandas as pd
import numpy as np

data = {
    "Name": ["Aya", "Omar", "Sara", "None"],
    "Age": [23, 24, 25, 30],
    "Score": [85, 90, None, 75]
}

df = pd.DataFrame(data)
print(df.isna().any())  # Check if any column has NaN values

df["Passed"] = [False, False, False, False]
print(df.any(axis=1))  # Check if any value in each row is True
