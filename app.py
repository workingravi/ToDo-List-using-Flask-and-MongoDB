from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
import os

mongodb_host = os.environ.get('MONGO_URL', 'localhost')
client = MongoClient(mongodb_host)    #Configure the connection to the database
db = client.demodb    #Select the database
users = db.test #Select the collection

app = Flask(__name__)
title = "Wendorse"
heading = "User List"

def redirect_url():
	return request.args.get('next') or \
		request.referrer or \
		url_for('index')


@app.route("/")
@app.route("/new")
def add_user():
  users_l = users.find()
  a3=""
  a2="active"
  return render_template('index.html',a2=a2, users=users_l,t=title,h=heading)


@app.route("/existing")
def curr_users():
  users_l = users.find()
  a2=""
  a3="active"
  return render_template('index.html',a3=a3,users=users_l,t=title,h=heading)


#@app.route("/add")
#def add():
#	return render_template('add.html',h=heading,t=title)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("pass")
	date=request.values.get("pass2")
	pr=request.values.get("email")
	users.insert({ "name":name, "email":email, "password":pass2})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	users.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=users.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/about")
def about():
	return render_template('credits.html',t=title,h=heading)

if __name__ == "__main__":
	env = os.environ.get('APP_ENV', 'development')
	port = int(os.environ.get('PORT', 5000))
	debug = False if env == 'production' else True
	app.run(host='0.0.0.0', port=port, debug=debug)
	# Careful with the debug mode..