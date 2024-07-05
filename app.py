from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ensure the data folder exists
if not os.path.exists('data'):
    os.makedirs('data')

DATABASE = 'data/students.db'

# Connect to SQLite database (or create it if it doesn't exist)
def init_sqlite_db():
    conn = sqlite3.connect(DATABASE)
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, phone TEXT, department TEXT, academic_year INTEGER, payment_method TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('student_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            department = request.form['department']
            academic_year = request.form['academicYear']
            payment_method = request.form['Payment Method']

            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, phone, department, academic_year, payment_method) VALUES (?, ?, ?, ?, ?)", 
                            (name, phone, department, academic_year, payment_method))
                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            return redirect(url_for('index'))
            con.close()

@app.route('/view')
def view():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    con.close()
    return render_template('view_students.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
