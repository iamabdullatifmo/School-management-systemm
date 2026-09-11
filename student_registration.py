from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Student, Department, YearsOfStudy
from extentions import db
from email_service import send_email

register_student_bp = Blueprint("register_student", __name__)


@register_student_bp.route("/registerStudent", methods=["POST", "GET"])
def register_student():

    if request.method == "POST":

        first_N = request.form.get("first")
        last_N = request.form.get("last")
        email = request.form.get("email")
        department = request.form.get("department")
        years_of_study = int(request.form.get("years_of_study"))

        full_N = first_N + " " + last_N
        level = 100

        try:
            # Create student
            user = Student(
                first_N=first_N,
                last_N=last_N,
                email=email,
                full_Name=full_N,
                department=department
            )

            db.session.add(user)

            # Get the generated student ID
            db.session.flush()

            # Create YearsOfStudy
            years = YearsOfStudy(
                student_id=user._id,
                years_of_study=years_of_study,
                semester=1,
                level=level
            )

            db.session.add(years)

            # Find department
            dept = Department.query.filter_by(
                dept_name=user.department
            ).first()

            if dept:
                dept._id = user._id

            # Commit database changes
            db.session.commit()

        except Exception as e:

            db.session.rollback()

            print("REGISTRATION ERROR:", repr(e))

            flash("Registration failed. Please try again.")

            return redirect(
                url_for("register_student.register_student")
            )

        # Send email AFTER successful database transaction
        email_sent = send_email(
            user.email,
            "School Management - Registration",
            f"""
            <h3>Hi {user.full_Name},</h3>

            <p>Welcome to TaTU institution.</p>

            <p>
                Your temporary password is:
                <strong>{user.password}</strong>
            </p>

            <p>
                Your ID is:
                <strong>{user._id}</strong>
            </p>

            <p>
                Please login with your ID and temporary password,
                then change your password.
            </p>
            """
        )

        if email_sent:
            flash(
                "Registration was successful. "
                "Your login details have been sent to your email."
            )
        else:
            flash(
                "Registration was successful, but we could not send "
                "the email. Please contact the administrator."
            )

        return redirect(url_for("login.login_S"))

    return render_template("regiater_student.html")
