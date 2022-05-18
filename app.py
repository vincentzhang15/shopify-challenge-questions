from flask import Flask
import mysql.connector
from front import front_page

app = Flask(__name__)

app.debug = False
app.testing = False

@app.route('/')
def site():
    return front_page("root")

PASS = "root"

def dbconn():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password=f"{PASS}",
      database="root"
    )
    return mydb

