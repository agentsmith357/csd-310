"""
Author: Jelani Jenkins
Date: 04/27/2025
Assignment: Module 7 - MySQL Queries

Write four queries, in one Python file.The output from your queries should match the example below, including descriptions of output and format.
The first and second query is to select all the fields for the studio and genre tables.
The third query is to select the movie names for those movies that have a run time of less than two hours.
The fourth query is to get a list of film names, and directors grouped by director.

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
    "raise_on_warnings": True #not in .env file
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

def query_studio_records():
    '''The first and second query is to select all the fields for the studio and genre tables.'''
    cur = reconnect_to_db()
    query = "SELECT * FROM movies.studio;"
    cur.execute(query)
    results = cur.fetchall()

    writer.write("-- DISPLAYING Studio RECORDS --\n")
    for row in results:
        writer.write(f"Studio ID: {row[0]}\n")
        writer.write(f"Studio Name: {row[1]}\n")     
        writer.write("\n")
    
def query_genre_records():
    '''The first and second query is to select all the fields for the studio and genre tables.'''
    cur = reconnect_to_db()
    query = "SELECT * FROM movies.genre;"
    cur.execute(query)
    results = cur.fetchall()

    writer.write("-- DISPLAYING Genre RECORDS --\n")
    for row in results:
        writer.write(f"Genre ID: {row[0]}\n")
        writer.write(f"Genre Name: {row[1]}\n")     
        writer.write("\n")
    
def query_film_records():
    '''The third query is to select the movie names for those movies that have a run time of less than two hours.'''
    cur = reconnect_to_db()
    query = "SELECT film_name, film_runtime FROM movies.film where film_runtime < 120"
    cur.execute(query)
    results = cur.fetchall()

    writer.write("-- DISPLAYING Short Film RECORDS --\n")
    for row in results:
        writer.write(f"Film Name: {row[0]}\n")
        writer.write(f"Runtime: {row[1]}\n")     
        writer.write("\n")
    
def query_director_records():
    '''The fourth query is to get a list of film names, and directors grouped by director.'''
    cur = reconnect_to_db()
    query = "SELECT film_name, film_director FROM movies.film order by film_director"""
    cur.execute(query)
    results = cur.fetchall()

    writer.write("-- DISPLAYING Director RECORDS in Order --\n")
    for row in results:
        writer.write(f"Film Name: {row[0]}\n")
        writer.write(f"Director: {row[1]}\n")     
        writer.write("\n")

if __name__ == "__main__":
    writer = open(os.path.join(BASE_DIR,"module-7","queries.txt"),"w") 
    query_studio_records()
    query_genre_records()
    query_film_records()
    query_director_records()
    writer.close()