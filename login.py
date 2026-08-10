from flask import Blueprint,render_template,request,url_for,session,redirect,flash
from extentions import db
from models import Lecturers,Student

login =Blueprint("login",__name__)

@login.route("/login_L",methods=["POST","GET"])
def login_L():
     if request.method == "POST":
      lec_id = request.form.get("_id")
      password = request.form.get("password")
      #verify password and ID to the stored database
      check = Lecturers.query.filter_by(password=password,lec_id=lec_id).first()
      if check:
         session["lec_id"]= check.lec_id
         return render_template("lecturer.html")
      else:
         flash("Wrong credentials","warning")
         return redirect(url_for("login.login_L"))
     return render_template("login.html" )

@login.route("/login_S",methods=["POST","GET"])
def login_S():
     if request.method == "POST":
       _id = request.form.get("_id")
       password = request.form.get("password")
       check = Student.query.filter_by(password=password,_id=_id).first()
       if check:
         session["student_id"] = check._id
         return render_template("student.html", student=check)
       else:
          flash("wrong credentials","error")
          return redirect(url_for("login.login_S"))
     return render_template("login.html")
     