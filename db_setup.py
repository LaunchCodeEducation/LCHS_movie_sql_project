import sqlite3

db = sqlite3.connect('project.db')
cursor = db.cursor()

sql_query = """
    CREATE TABLE IF NOT EXISTS directors 
    (director_id INTEGER PRIMARY KEY, last_name TEXT, first_name TEXT, country TEXT)
    """
cursor.execute(sql_query)
sql_query = """
    CREATE TABLE IF NOT EXISTS movies 
    (movie_id INTEGER PRIMARY KEY, title TEXT, year_released INT, director INT,
    FOREIGN KEY (director) REFERENCES directors(director_id))
    """
cursor.execute(sql_query)

insert_movie = f"INSERT INTO movies (title, year_released, director) VALUES (?, ?, ?)"
insert_director = f"INSERT INTO directors (last_name, first_name, country) VALUES (?, ?, ?)"

titles = {
    'Iron Man': [2008, 'Jon Favreau'], 
    'Captain America: The First Avenger': [2011, 'Joe Johnston'], 
    "The Avengers" : [2012, 'Joss Whedon'],
    'Guardians of the Galaxy': [2014, 'James Gunn'], 
    'Black Panther': [2018, 'Ryan Coogler'], 
    'Spider-Man: Homecoming': [2017, 'Jon Watts'], 
    'Black Widow': [2021, 'Cate Shortland']
}

for (title, data) in titles.items():
    cursor.execute(insert_movie, (title, data[0], data[1]))
db.commit()

db.close()