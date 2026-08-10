from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from extentions import db,mail
from models import Lecturers
import uuid
from flask_mail import Message
from department import lec_department

register_lecturer_bp=Blueprint("register_lecturer",__name__)

@register_lecturer_bp.route("/registerLecturer", methods=["GET","POST"], endpoint="register_lecturer")
def register_lecturer():
    if request.method =="POST":
        first_N=request.form.get("first_N")
        last_N=request.form.get("last_N")
        email=request.form.get("email")
        rank=request.form.get("rank")
        lecturer = Lecturers(first_N=first_N,last_N=last_N,email=email,full_Name=f"{first_N} {last_N}")
        db.session.add(lecturer)
        db.session.commit()
        session["lec_id"] = lecturer.lec_id

        if rank in ["masters_degree","professor_degree"] and lec_department:
            msg = Message(subject="Welcome To TaTU",recipients=[lecturer.email])
            msg.html = f"""
                    Hi {lecturer.full_Name},<br>
                    Welcome to TaTU institution.<br>
                    <p>This is your temporary password: {lecturer.password}</p>
                    <p>This is your ID: {lecturer.lec_id}</p>
                    <p>Login with the ID and the password and change the password with your preferred password</p>

                    """
            mail.send(msg)
            flash("You have been granted admission as Lecturer to TATU University","info")
            return redirect(url_for("lecturers_department.lec_department"))
        else:
            return f"Sorry your rank does not guaranteed you admission to the univerty"
    return render_template("register_lecturer.html")

