from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    roll = request.form['roll']
    marks = [int(request.form[f"sub{i}"]) for i in range(1, 6)]
    total = sum(marks)
    avg = total / 5
    grade = 'A' if avg >= 90 else 'B' if avg >= 75 else 'C' if avg >= 60 else 'D' if avg >= 40 else 'F'

    with open('results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, roll] + marks + [total, avg, grade])

    return redirect('/')

@app.route('/view')
def view():
    records = []
    try:
        with open('results.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                records.append(row)
    except FileNotFoundError:
        pass
    return render_template('view.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)