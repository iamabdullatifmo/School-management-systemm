from flask import Blueprint,session,render_template,redirect,url_for
from models import Grades,Student

check_results_bp = Blueprint("check_result", __name__)

@check_results_bp.route("/check_results", methods = ["POST","GET"])
def check_results():
     student_id = session.get("student_id")
     grades=[]
     if student_id:
        grades =Grades.query.filter_by(student_id=student_id).all()
        
     return render_template("check_results.html",grades=grades)    
