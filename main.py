from flask import Flask, request, redirect, render_template, session
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_type = '/' + request.form['query_type'].lower()
        session['table'] = request.form['table']
        if session['table'] == 'movies':
            session['columns'] = ['movie_id', 'title', 'year_released', 'director']
        else:
            session['columns'] = ['director_id', 'last_name', 'first_name']
        return redirect(query_type)
    else:
        query_types = ['INSERT', 'SELECT', 'UPDATE', 'DELETE']
    return render_template("index.html", tab_title = "Movie SQL Project", query_types = query_types, home=True)

@app.route('/insert', methods=['GET', 'POST'])
def insert_query():
    return render_template("insert.html", tab_title = "INSERT query", home=False)

@app.route('/select', methods=['GET', 'POST'])
def select_query():
    return render_template("select.html", tab_title = "SELECT query", home=False)

@app.route('/update', methods=['GET', 'POST'])
def update_query():
    return render_template("update.html", tab_title = "UPDATE query", home=False)

@app.route('/delete', methods=['GET', 'POST'])
def delete_query():
    return render_template("delete.html", tab_title = "DELETE query", home=False)

if __name__ == '__main__':
    app.run()