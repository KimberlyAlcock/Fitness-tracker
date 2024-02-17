import json
import pandas as pd

# Read Excel file into a pandas DataFrame
tracker_data_df = pd.read_excel('./data/practice-tracker.xlsx', sheet_name='active')

# Convert DataFrame to JSON
json_data = tracker_data_df.to_json(orient='records', date_format='iso')

# Write JSON data to a file

with open('./static/src/data.json', 'w') as f:
    f.write(json_data)

# Print JSON results to console
print('Excel Sheet convered to JSON', json_data)

