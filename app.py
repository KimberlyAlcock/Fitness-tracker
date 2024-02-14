from flask import Flask, render_template, request
import openpyxl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['data']

    # Open the Excel file
    wb = openpyxl.load_workbook('./data/practice-tracker.xlsx')
    ws = wb.active

    # Append data to the next empty row
    row = (data,)
    ws.append(row)

    # Save the changes
    wb.save('data.xlsx')

    return 'Data submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)