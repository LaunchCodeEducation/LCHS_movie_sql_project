from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_type = '/' + request.form['query_type'].lower()
        return redirect(query_type)

    query_types = ['INSERT', 'SELECT', 'UPDATE', 'DELETE']
    return render_template("index.html", tab_title = "Movie SQL Project", query_types = query_types)

@app.route('/display_results')
def display_results():
   return render_template("display_results.html", tab_title = "SELECT Results")

if __name__ == '__main__':
    app.run()