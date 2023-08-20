import datetime
from flask import Flask, render_template, request, redirect
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
application = Flask(__name__)
client=MongoClient("mongodburlhere")
application.db=client.Microblog

@application.route("/", methods=["GET","POST"])

def home():
    if request.method == "POST":
        if request.form.get("contents"):
            entry_content= request.form.get("contents")
            formatted_date= datetime.datetime.today().strftime("%Y-%m-%d")
            application.db.entries.insert_one({"content":entry_content, "date":formatted_date})
        if request.form.get("deleting"):
            thisid=request.form.get("deleting")
            application.db.entries.delete_one({"_id": ObjectId(thisid)})


    global entries_final
    entries_final=[]
    for entry in application.db.entries.find({}):
        entries_final.append((entry["content"],entry["date"],
                                datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d"),
                            entry["_id"]
                                ))
    return render_template("main_page.html", entries=entries_final)

@application.route("/edit", methods=["GET","POST"])
def edithome():
    global edit_id
    if request.method == "POST":
        if request.form.get("editinfo"):
            edit_id=request.form['editinfo']
        if request.form.get("edit_content"):
            edit_content=request.form.get("edit_content")
            formatted_date= datetime.datetime.today().strftime("%Y-%m-%d")
            application.db.entries.update_one({"_id": ObjectId(edit_id)},{"$set": {"content":edit_content, "date":formatted_date}})
            return redirect('/')
    return render_template("edit_page.html",entries=entries_final)




if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))
