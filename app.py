import pyodbc
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Establish connection to Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=./data/practice-tracker.accdb;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('planks.html')

@app.route('/get_data')
def get_data():
    # Fetch data from the Access database
    cursor.execute('SELECT * FROM skills-practice')
    rows = cursor.fetchall()

    # Convert data to list of dictionaries
    data = []
    for row in rows:
        data.append(dict(zip([column[0] for column in cursor.description], row)))

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)