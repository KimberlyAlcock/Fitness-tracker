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


##################################################################

# Receive Tracker form input
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('planks.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data from request
    form_data = request.form.to_dict()

    # Convert form data to JSON
    with open('./static/src/data.json', 'w') as g:
        json.dump(form_data, g)

    return jsonify({'message': 'Data saved to data.json'})

if __name__ == '__main__':
    app.run(debug=True)
    