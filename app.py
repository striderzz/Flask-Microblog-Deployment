from flask import Flask
from flask import render_template,request, redirect,url_for
import datetime
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


app = Flask(__name__)

# Mongo DB Connect
client = MongoClient(os.getenv("MONGODB_URI"))
app.db = client.Microblog

collection = app.db['entries']

entries = []

@app.route("/",methods = ["GET","POST"])
def home():

  print([e for e in app.db.entries.find({})])

  entries = collection.find({})
  return render_template("home.html", entries = entries)

@app.route("/submit",methods =["POST","GET"])
def submit():
  if request.method == "POST":
    entry_content = request.form.get("content")
    formatted_date =datetime.datetime.today().strftime("%Y-%m-%d")
    short_date = datetime.datetime.today().strftime("%d %B, %Y")
    
    # Insert new entry into MongoDB
    entry = {
        'content': entry_content,
        'formatted_date': formatted_date,
        'short_date': short_date
    }
    collection.insert_one(entry)

  return redirect(url_for("home"))



if __name__ == "__main__":
  app.run(debug=True)