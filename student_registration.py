from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from models import Student,Department,YearsOfStudy
from extentions import db,mail
from flask_mail import Message

register_student_bp = Blueprint("register_student",__name__)

@register_student_bp.route("/registerStudent", methods=["GET", "POST"])
def register_student():

    if request.method == "GET":
        return render_template("regiater_student.html")

    # Get form data
    first_N = request.form.get("first")
    last_N = request.form.get("last")
    email = request.form.get("email")
    department = request.form.get("department")
    years_of_study_raw = request.form.get("years_of_study")

    # Validate required fields
    if not first_N or not last_N or not email or not department:
        flash("Please fill in all required fields.")
        return redirect(url_for("register_student.register_student"))

    # Validate years
    try:
        years_of_study = int(years_of_study_raw)
    except (TypeError, ValueError):
        flash("Invalid years of study.")
        return redirect(url_for("register_student.register_student"))

    full_N = f"{first_N} {last_N}"
    level = 100

    try:
        # Find department
        dept = Department.query.filter_by(
            dept_name=department
        ).first()



        # Create student
        user = Student(
            first_N=first_N,
            last_N=last_N,
            email=email,
            full_Name=full_N,
            department=department
        )

        db.session.add(user)
        db.session.flush()

        # Create years-of-study record
        years = YearsOfStudy(
            student_id=user._id,
            years_of_study=years_of_study,
            semester=1,
            level=level
        )

        db.session.add(years)

        # Save database changes
        db.session.commit()

        # Send email AFTER successful DB transaction
        msg = Message(
            subject="School Management",
            recipients=[user.email]
        )

        msg.html = f"""
        Hi {user.full_Name},<br><br>

        Welcome to TaTU institution.<br><br>

        <p>This is your temporary password: {user.password}</p>
        <p>This is your ID: {user._id}</p>

        <p>
        Login with the ID and password given to you
        and change the password to your preferred password.
        </p>
        """

        mail.send(msg)

        flash(
            "Registration was successful. "
            "Login with the ID and password given to you "
            "and change your password."
        )

        return redirect(url_for("login.login_S"))

    except Exception as e:
        db.session.rollback()

        print("REGISTRATION ERROR:", repr(e), flush=True)

        flash("Registration failed. Please try again.")
        return redirect(url_for("register_student.register_student"))
