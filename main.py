from flask import Flask, request, redirect, render_template, session
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

def execute_query(query_string):
    db = sqlite3.connect('project.db')
    cursor = db.cursor()
    if "select" in query_string.lower():
        try:
            results = list(cursor.execute(query_string))
        except:
            results = 'error'
    else:
        try:
            cursor.execute(query_string)
            db.commit()
            results = "Query successfully run."
        except:
            results = 'error'
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
            session['columns'] = [['director_id', 'number'], ['last_name', 'text'], ['first_name', 'text']]
        return redirect(query_type)

    query_types = ['INSERT', 'SELECT', 'UPDATE', 'DELETE']
    return render_template("index.html", tab_title = "Movie SQL Project", query_types = query_types)

@app.route('/select', methods=['GET', 'POST'])
def select_query():
    if request.method == 'POST':
        table = session['table']
        columns = request.form['columns']
        condition = request.form['condition']
        if len(columns) == 0 or '*' in columns:
            columns = '*'
            if table == 'movies':
                session['selected_columns'] = ['movie_id', 'title', 'year_released', 'director']
            else:
                session['selected_columns'] = ['director_id', 'last_name', 'first_name']
        else:
            session['selected_columns'] = columns.split(',')
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
        columns = request.form['columns']
        values = request.form['values']
        to_enter = values.split(',')
        for index in range(len(to_enter)):
            to_enter[index] = to_enter[index].strip()
            if to_enter[index].isdigit():
                to_enter[index] = int(to_enter[index])

        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        results = execute_query(sql_query)
    else:
        sql_query = ''
        results = []

    return render_template("insert.html", tab_title = "Movie SQL Project", sql_query = sql_query, results = results)

@app.route('/delete', methods=['GET', 'POST'])
def delete_query():
    if request.method == 'POST':
        table = session['table']
        condition = request.form['condition']
        sql_query = f"DELETE FROM {table} WHERE {condition}"
        results = execute_query(sql_query)
    else:
        sql_query = ''
        results = []

    return render_template("delete.html", tab_title = "Movie SQL Project", sql_query = sql_query, results = results)

if __name__ == '__main__':
    app.run()