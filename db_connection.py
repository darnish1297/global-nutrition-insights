# db_connection.py
import sqlite3

def get_connection():
    return sqlite3.connect("nutrition_paradox.db")
