from flask import Blueprint,render_template,url_for,session,request
from extentions import db
from models import Student

bio_bp = Blueprint("bio",__name__)

@bio_bp.route("/bio",methods=["POST","GET"])
def bio():
    student_id = session.get("student_id")
    if student_id:
     student_bio = Student.query.get(student_id)
     return render_template("bio.html",bio=student_bio)
    else:
       return "You are not logged in"

    
