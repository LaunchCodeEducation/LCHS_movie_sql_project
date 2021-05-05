from flask import Flask, request, redirect, render_template, session
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

def execute_query(query_string):
    db = sqlite3.connect('project.db')
    cursor = db.cursor()
    if "SELECT" in query_string:
        try:
            results = list(cursor.execute(query_string))
        except:
            results = 'error'
    else:
        cursor.execute(query_string)
        results = "Query successfully run."
    if "SELECT" not in query_string:
        db.commit()
    db.close()
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_type = '/' + request.form['query_type'].lower()
        session['table'] = request.form['table']
        if session['table'] == 'movies':
            session['columns'] = [['movie_id', 'number'], ['title', 'text'], ['year_released', 'number'], ['director', 'text']]
        else:
            session['columns'] = [['director_id', 'number'], ['last_name', 'text'], ['first_name', 'text'], ['country', 'text']]
        return redirect(query_type)

    query_types = ['INSERT', 'SELECT', 'UPDATE', 'DELETE']
    return render_template("index.html", tab_title = "Movie SQL Project", query_types = query_types)

@app.route('/display_results')
def display_results():
   return render_template("display_results.html", tab_title = "SELECT Results")

@app.route('/select', methods=['GET', 'POST'])
def select_query():
    if request.method == 'POST':
        session['checked_columns'] = request.form.getlist('columns')
        table = session['table']
        condition = request.form['condition']
        if len(session['checked_columns']) == 0:
            columns = '*'
        else:
            columns = ''
            for column in session['checked_columns']:
                columns += column.lower() + ', '
            columns = columns.strip()[:-1]
        sql_query = f"SELECT {columns} FROM {table}"
        if condition != '':
            sql_query += f" WHERE {condition}"
        results = execute_query(sql_query)
    else:
        sql_query = ''
        results = []

    return render_template("select.html", tab_title = "Movie SQL Project", sql_query = sql_query, results = results)

@app.route('/insert', methods=['GET', 'POST'])
def insert_query():
    if request.method == 'POST':
        table = session['table']
        columns = ''
        values = ''
        for column in session['columns']:
            value = request.form[column[0]]
            if value != '':
                values += value + ', '
                columns += column[0] + ', '
        values = values.strip()[:-1]
        columns = columns.strip()[:-1]
        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        # execute_query(sql_query)
    else:
        sql_query = ''

    return render_template("insert.html", tab_title = "Movie SQL Project", sql_query = sql_query)

if __name__ == '__main__':
    app.run()