from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import YearsOfStudy, Admin, AcademicSession
from extentions import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin", methods=["POST", "GET"])
def admin_page():
    if request.method == "POST":

        admin_password = request.form.get("password")
        admin = Admin.query.filter_by(password=admin_password).first()

        if not admin or admin.password != admin_password:
            flash("Invalid admin password.", "error")
            return redirect(url_for("admin.admin_page"))

        # Login successful
        session["admin_logged_in"] = True
        session["admin_name"] = admin.name

        return redirect(url_for("admin.admin_update"))

    return render_template("admin.html")


@admin_bp.route("/admin_update", methods=["POST", "GET"])
def admin_update():

    if not session.get("admin_logged_in"):
        flash("Please login as admin first.", "error")
        return redirect(url_for("admin.admin_page"))

    if request.method == "POST":

        new_semester = request.form.get("semester", type=int)
        new_year = request.form.get("years")

        if new_semester not in [1, 2]:
            flash("Please select a valid semester.", "error")
            return redirect(url_for("admin.admin_update"))

        if not new_year:
            flash("Please select an academic year.", "error")
            return redirect(url_for("admin.admin_update"))

        academic_session = AcademicSession.query.first()

        if academic_session:
            academic_session.academic_year = new_year
            academic_session.semester = new_semester
            academic_session.registration_open = True

        else:
            academic_session = AcademicSession(
                academic_year=new_year,
                semester=new_semester,
                registration_open=True
            )

            db.session.add(academic_session)

        db.session.commit()

        flash(
            f"Academic session updated to {new_year}, Semester {new_semester}. "
            "Course registration is now open.",
            "success"
        )

        return redirect(url_for("admin.admin_update"))

    current_session = AcademicSession.query.first()

    return render_template(
        "admin_post.html",
        current_session=current_session
    )
