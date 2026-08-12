from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from models import Student,Department,YearsOfStudy
from extentions import db,mail
from flask_mail import Message

register_student_bp = Blueprint("register_student",__name__)


@register_student_bp.route("/registerStudent",methods=["POST","GET"])
def register_student():
    if request.method == "POST":
        first_N=request.form.get("first")
        last_N=request.form.get("last")
        email=request.form.get("email")
        full_N=first_N + " " + last_N
        department = request.form.get("department")
        years_of_study = int(request.form.get("years_of_study"))
    
        user = Student(first_N=first_N,last_N=last_N,email=email,full_Name=full_N,department=department)
        db.session.add(user)
        db.session.commit()

        msg = Message(subject='School Mangement',recipients=[user.email] )
        msg.html = f"""
                    Hi {user.full_Name},<br>
                    Welcome to TaTU institution.<br>
                    <p>This is your temporary password: {user.password}</p>
                    <p>This is your ID: {user._id}</p>
                    <p>Login with the ID and the password and change the password with your preferred password</p>

                    """
        mail.send(msg)
        flash("Registration was successfully.Login with the ID and password given to you and change the password")
        # query and check the department table whose department name matches with the department the student chooses
        dept = Department.query.filter_by(dept_name=user.department).first()
        student_id = session.get("student_id")
        years= YearsOfStudy(student_id=student_id,years_of_study=years_of_study,semester=1)
        db.session.add(years)
        db.session.commit()
        # Store the department _id as the same of student _id
        if dept:
         dept._id = user._id
         db.session.commit()
        
        return redirect(url_for("login.login_S"))
    return render_template("regiater_student.html")


