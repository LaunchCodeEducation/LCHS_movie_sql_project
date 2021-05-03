from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
   return render_template("index.html", tab_title = "Movie SQL Project")

@app.route('/display_results')
def display_results():
   return render_template("display_results.html", tab_title = "SELECT Results")

if __name__ == '__main__':
    app.run()