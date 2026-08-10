from flask import Blueprint,request,redirect,url_for,session,render_template,flash
from extentions import db
from models import Lecturers, Student

change_password_bp = Blueprint("change_password",__name__)

@change_password_bp.route("/password_change", methods=["POST","GET"])
def change_student():
      student_id = session.get("student_id")
      if not student_id:
          return redirect(url_for("login.login_S"))

      if request.method=="POST":
       new_password = request.form.get("new_password")
       confirm_password = request.form.get("confirm_password") 
       if new_password == confirm_password:
         student = Student.query.get(student_id)
         if not student:
             flash("student not found")
         student.password = new_password
         db.session.commit()
         flash("Password changed successfully","info")
         return redirect(url_for("login.login_S"))
       flash("Password do not match!")
       return redirect(url_for("change_password.change_student"))
      return render_template("change_password_student.html")

@change_password_bp.route("/change_password", methods=["POST","GET"])
def change_lecturer():
    # get the session id
    lecturer_id = session.get("lec_id")

    if request.method=="POST":
        
         new_password = request.form.get("new_password")
         confirm_password = request.form.get("confirm_password") 
         if new_password == confirm_password:
           lecturer = Lecturers.query.get(lecturer_id)
           if not lecturer:
               flash("Lecturer not found")
               return redirect(url_for("login.login_L"))
           lecturer.password = new_password
           db.session.commit()
           flash("Password changed successfully,please login with the new password","info")
           return redirect(url_for("login.login_L"))
           
         flash("Password do not match","error")
         return redirect(url_for("change_password.change_lecturer"))
               
    return render_template("change_password_lecturer.html")
      