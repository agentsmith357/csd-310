"""
Author: Jelani Jenkins
Date: 04/27/2025
Assignment: Module 8 - Updates and Deletes


Using the example code I provided, connect to the movies database.
Using the example code I have provided, call the show_films function to display the selected fields and the associated Label.
show_films(cursor, "DISPLAYING FILMS")
Insert a new record into the film table using a film of your choice. Do not use 'Star Wars'. (Easier if you use a studio already in use..)
Using the example code I have provided, call the show_films function to display the selected fields and the associated Label.
Using the example code I have provided, update the film Alien to being a Horror film.
Using the example code I have provided, call the show_films function to display the selected fields and the associated Label.
Using the example code I have provided, delete the movie Gladiator.
Using the example code I have provided, call theshow_films function to display the selected fields and the associated Label.
Run the script and take a screen shot of the results, or copy the output, and paste into the Word document. Save your document as <your-last-name>-<assignment-name> .docx into your CSD-310/module-8 directory.
Make sure your output matches the expected output (this is gradable.)

"""

import mysql.connector # to connect
from mysql.connector import errorcode
from pathlib import Path # to use Path
from dotenv import dotenv_values
import os, sys
BASE_DIR = Path(__file__).resolve().parent.parent # get the current working directory
#using our .env file
ENV = Path(os.path.join(BASE_DIR,".env"))
if os.path.exists(ENV):
    secrets = dotenv_values(ENV) # load the .env file
else:
    sys.exit("No .env file found.")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True, #not in .env file
    "autocommit": True
}

writer =None
conn = None

def reconnect_to_db():
    global conn
    if conn:
        conn = None
    db = mysql.connector.connect(**config) 
    conn = db
    cur = conn.cursor()
    return cur

def show_films(cursor, title):
    cursor.execute("""select film_name as Name, film_director as Director, genre_name as Genre, 
                   studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id 
                   INNER JOIN studio ON film.studio_id=studio.studio_id""")
    films = cursor.fetchall()
    print("\n -- {} --".format(title))
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))


def insert_film(cursor):
    query = """INSERT INTO film (film_id, film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
    VALUES (4, 'The Invisible Man', '2020', 124, 'Leigh Whannell', 3, 1);"""
    cursor.execute(query)

def update_film(cursor):
    query = """UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'"""
    cursor.execute(query)

def delete_film(cursor):
    query = """DELETE FROM film WHERE film_name = 'Gladiator'"""
    cursor.execute(query)
    

if __name__ == "__main__":
    show_films(reconnect_to_db(), "DISPLAYING FILMS")
    insert_film(reconnect_to_db())
    show_films(reconnect_to_db(), "DISPLAYING FILMS AFTER INSERT")
    update_film(reconnect_to_db())
    show_films(reconnect_to_db(), "DISPLAYING FILMS AFTER UPDATE")
    delete_film(reconnect_to_db())  
    show_films(reconnect_to_db(), "DISPLAYING FILMS AFTER DELETE")
    conn.close()