from flask import Blueprint,render_template,session,request
from extentions import db
from models import Lecturers,Student
import uuid

lecturer_bp=Blueprint("lecturer",__name__)

@staticmethod 
def generate_matrix():
    return str(uuid.uuid4())

@lecturer_bp.route("/lecturer")
def lecturer_home():
    session["lec_id"] = lecturer.lec_id
    get_id = session.get("lec_id")
    if get_id:
        lecturer = Lecturers.query.filter_by(lec_id=get_id).first()
        return render_template("lecturer.html")

@lecturer_bp.route("/upload_results",methods=["POST","GET"])    
def upload_results():
    department = request.form.get("department")
    get_id = session.get("lec_id")
    if get_id:
     if request.method == "POST":
        if department == "computer science":
            return render_template("comp_department")


    


