from flask import Flask, request, redirect, render_template, session
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

# db = sqlite3.connect('project.db')
# cursor = db.cursor()

# sql_query = """
#     CREATE TABLE IF NOT EXISTS directors 
#     (director_id INTEGER PRIMARY KEY, last_name TEXT, first_name TEXT, country TEXT)
#     """
# cursor.execute(sql_query)
# sql_query = """
#     CREATE TABLE IF NOT EXISTS movies 
#     (movie_id INTEGER PRIMARY KEY, title TEXT, year_released INT, director INT,
#     FOREIGN KEY (director) REFERENCES directors(director_id))
#     """
# cursor.execute(sql_query)
# db.close()

def execute_query(query_string):
    db = sqlite3.connect('project.db')
    cursor = db.cursor()
    if "SELECT" in query_string:
        results = list(cursor.execute(query_string))
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
        return redirect(query_type)

    query_types = ['INSERT', 'SELECT', 'UPDATE', 'DELETE']
    return render_template("index.html", tab_title = "Movie SQL Project", query_types = query_types)

@app.route('/display_results')
def display_results():
   return render_template("display_results.html", tab_title = "SELECT Results")

@app.route('/select', methods=['GET', 'POST'])
def select_query():
    if request.method == 'POST':
        columns = request.form['columns']
        table = session['table']
        condition = request.form['condition']
        sql_query = f"SELECT {columns} FROM {table}"
        if condition != '':
            sql_query += f" WHERE {condition}"
    else:
        if session['table'] == 'movies':
            columns = [['Title', 'text'], ['Year Released', 'number'], ['Director', 'text']]
        elif session['table'] == 'directors':
            columns = [['Last Name', 'text'], ['First Name', 'text'], ['Country', 'text']]
        else:
            columns = [['Last Name', 'text'], ['First Name', 'text']]
        sql_query = ''

    return render_template("select.html", tab_title = "Movie SQL Project", sql_query = sql_query, columns = columns)

@app.route('/insert', methods=['GET', 'POST'])
def insert_query():
    if request.method == 'POST':
        columns = request.form['columns']
        table = request.form['table']
        values = request.form['values']
        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    else:
        if session['table'] == 'movies':
            columns = [['Title', 'text'], ['Year Released', 'number'], ['Director', 'text']]
        elif session['table'] == 'directors':
            columns = [['Last Name', 'text'], ['First Name', 'text'], ['Country', 'text']]
        else:
            columns = []
        sql_query = ''

    return render_template("insert.html", tab_title = "Movie SQL Project", sql_query = sql_query, columns = columns)

if __name__ == '__main__':
    app.run()