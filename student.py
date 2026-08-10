from flask import Blueprint,url_for,redirect,render_template,session
from models import Student


student_bp = Blueprint("student",__name__)

@student_bp.route("/student", methods=["POST","GET"])
def student():
    get_id = session.get("_id")
    if get_id:
        student = Student.query.filter_by(_id=get_id).first()
        return render_template("student.html", student=student)
    else:
        return redirect(url_for("login.login_S"))