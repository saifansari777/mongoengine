from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient  
from bson import ObjectId
from mongoengine import *

app = Flask(__name__)


connect("newnotes", host='localhost', port=27017)

class Note(Document):
    title = StringField(required=True,  max_length=10)
    note = StringField(required=True)

@app.route("/",  methods=["GET", "POST"])
def home_page():
	if request.form:
		titled = request.form.get("title")
		noted = request.form.get("note")
		notes = Note(title=titled, note=noted)
		notes.save()
		
		return redirect("/")
	notes_all = Note.objects
	print(Note.objects)

	return render_template("home.html", notes=notes_all)

@app.route("/delete",  methods=["POST"])
def delete():
	ids = request.form.get("id")
	print(ids)
	note = Note.objects(id=ObjectId(ids))[0]
	note.delete()
	return redirect("/")


@app.route("/<id>/update", methods=["GET", "POST"])
def update(id):
    print(id)
    note = Note.objects(id=ObjectId(id))
    print(note, id)
    if request.form:
        newtitle = request.form.get("newtitle")
        newnote = request.form.get("newnote")
        note = Note.objects(id=ObjectId(id))[0]
        note.title, note.note = newtitle, newnote
        note.save()
        return redirect("/")
    return render_template("update.html", note=note)

if __name__ == '__main__':
	app.run()