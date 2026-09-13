from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from extentions import db, mail
from models import Lecturers
from flask_mail import Message
from department import lec_department

register_lecturer_bp = Blueprint("register_lecturer", __name__)


@register_lecturer_bp.route(
    "/registerLecturer",
    methods=["GET", "POST"],
    endpoint="register_lecturer"
)
def register_lecturer():

    if request.method == "POST":

        first_N = request.form.get("first_N")
        last_N = request.form.get("last_N")
        email = request.form.get("email")
        rank = request.form.get("rank")

        lecturer = Lecturers(
            first_N=first_N,
            last_N=last_N,
            email=email,
            full_Name=f"{first_N} {last_N}"
        )

        # Save lecturer
        db.session.add(lecturer)
        db.session.commit()

        session["lec_id"] = lecturer.lec_id

        # Check whether lecturer qualifies
        if rank in ["masters_degree", "professor_degree"] and lec_department:

            try:
                msg = Message(
                    subject="Welcome To TaTU",
                    recipients=[lecturer.email]
                )

                msg.html = f"""
                    Hi {lecturer.full_Name},<br><br>

                    Welcome to TaTU institution.<br><br>

                    <p>
                        This is your temporary password:
                        {lecturer.password}
                    </p>

                    <p>
                        This is your ID:
                        {lecturer.lec_id}
                    </p>

                    <p>
                        Login with the ID and the password given to you
                        and change the password to your preferred password.
                    </p>
                """

                mail.send(msg)

                print("LECTURER EMAIL SENT SUCCESSFULLY", flush=True)

                flash(
                    "You have been granted admission as Lecturer to TaTU University.",
                    "info"
                )

            except Exception as e:

                print(
                    "LECTURER EMAIL ERROR:",
                    repr(e),
                    flush=True
                )

                flash(
                    "Lecturer registration succeeded, but the email could not be sent.",
                    "warning"
                )

            return redirect(
                url_for("lecturers_department.lec_department")
            )

        else:
            return (
                "Sorry, your rank does not guarantee you admission "
                "to the university."
            )

    return render_template("register_lecturer.html")
