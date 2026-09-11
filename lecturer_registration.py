from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from extentions import db
from models import Lecturers
from department import lec_department
from email_service import send_email


register_lecturer_bp = Blueprint(
    "register_lecturer",
    __name__
)


@register_lecturer_bp.route(
    "/registerLecturer",
    methods=["GET", "POST"],
    endpoint="register_lecturer"
)
def register_lecturer():

    if request.method == "POST":

        first_N = request.form.get("first_N", "").strip()
        last_N = request.form.get("last_N", "").strip()
        email = request.form.get("email", "").strip()
        rank = request.form.get("rank", "").strip()

        # Validate required fields
        if not first_N or not last_N or not email or not rank:
            flash(
                "Please complete all required fields.",
                "error"
            )
            return render_template("register_lecturer.html")

        # Check whether the rank qualifies
        if rank not in ["masters_degree", "professor_degree"]:
            flash(
                "Sorry, your rank does not qualify you for admission "
                "as a lecturer.",
                "error"
            )
            return render_template("register_lecturer.html")

        # Check department
        if not lec_department:
            flash(
                "No lecturer department is currently available.",
                "error"
            )
            return render_template("register_lecturer.html")

        try:

            # Create lecturer
            lecturer = Lecturers(
                first_N=first_N,
                last_N=last_N,
                email=email,
                full_Name=f"{first_N} {last_N}"
            )

            db.session.add(lecturer)

            # Get generated lecturer ID before committing
            db.session.flush()

            # Save lecturer
            db.session.commit()

            # Store lecturer ID in session
            session["lec_id"] = lecturer.lec_id

        except Exception as e:

            db.session.rollback()

            print("LECTURER REGISTRATION ERROR:", repr(e))

            flash(
                "Lecturer registration failed. Please try again.",
                "error"
            )

            return render_template("register_lecturer.html")

        # Send welcome email after successful registration
        email_sent = send_email(
            lecturer.email,
            "Welcome To TaTU",
            f"""
            <h3>Hi {lecturer.full_Name},</h3>

            <p>Welcome to TaTU institution.</p>

            <p>
                This is your temporary password:
                <strong>{lecturer.password}</strong>
            </p>

            <p>
                This is your lecturer ID:
                <strong>{lecturer.lec_id}</strong>
            </p>

            <p>
                Login with your ID and temporary password,
                then change your password to your preferred password.
            </p>
            """
        )

        if email_sent:

            flash(
                "You have been granted admission as a Lecturer "
                "to TaTU University. Your login details have been "
                "sent to your email.",
                "info"
            )

        else:

            flash(
                "You have been granted admission as a Lecturer "
                "to TaTU University, but we could not send your "
                "email. Please contact the administrator for your "
                "login details.",
                "warning"
            )

        return redirect(
            url_for("lecturers_department.lec_department")
        )

    return render_template("register_lecturer.html")
