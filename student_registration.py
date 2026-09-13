from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Student, Department, YearsOfStudy
from extentions import db, mail
from flask_mail import Message

register_student_bp = Blueprint("register_student", __name__)


@register_student_bp.route("/registerStudent", methods=["POST", "GET"])
def register_student():

    if request.method == "POST":

        first_N = request.form.get("first")
        last_N = request.form.get("last")
        email = request.form.get("email")
        full_N = first_N + " " + last_N
        department = request.form.get("department")
        years_of_study = int(request.form.get("years_of_study"))

        level = 100

        user = Student(
            first_N=first_N,
            last_N=last_N,
            email=email,
            full_Name=full_N,
            department=department
        )

        # Save student
        db.session.add(user)
        db.session.commit()

        # Send email
        try:
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
                    Login with the ID and the password given to you
                    and change the password to your preferred password.
                </p>
            """

            mail.send(msg)

            print("EMAIL SENT SUCCESSFULLY", flush=True)

            flash(
                "Registration was successful. "
                "Your ID and password have been sent to your email."
            )

        except Exception as e:

            print("EMAIL ERROR:", repr(e), flush=True)

            flash(
                "Registration was successful, but we could not send "
                "the email. Please contact the administrator."
            )

        # Find student's department
        dept = Department.query.filter_by(
            dept_name=user.department
        ).first()

        # Create years of study record
        years = YearsOfStudy(
            student_id=user._id,
            years_of_study=years_of_study,
            semester=1,
            level=level
        )

        db.session.add(years)
        db.session.commit()

        # Store department ID as student's ID
        if dept:
            dept._id = user._id
            db.session.commit()

        return redirect(url_for("login.login_S"))

    return render_template("regiater_student.html")
