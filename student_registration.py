from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Student, Department, YearsOfStudy
from extentions import db

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

        # Create student
        user = Student(
            first_N=first_N,
            last_N=last_N,
            email=email,
            full_Name=full_N,
            department=department
        )

        db.session.add(user)
        db.session.commit()

        # Create YearsOfStudy record
        years = YearsOfStudy(
            student_id=user._id,
            years_of_study=years_of_study,
            semester=1,
            level=level
        )

        db.session.add(years)
        db.session.commit()

        # Find department
        dept = Department.query.filter_by(
            dept_name=user.department
        ).first()

        if dept:
            dept._id = user._id
            db.session.commit()

        flash(
            "Registration was successful. "
            "Login with the ID and password given to you "
            "and change the password."
        )

        return redirect(url_for("login.login_S"))

    return render_template("regiater_student.html")
