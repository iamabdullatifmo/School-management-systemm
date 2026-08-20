from flask import Blueprint,render_template,request,url_for,session,flash,redirect
from models import YearsOfStudy,Admin
from extentions import db

admin_bp = Blueprint("admin",__name__)

@admin_bp.route("/admin", methods=["POST", "GET"])
def admin_page():
    if request.method == "POST":
        admin_password = request.form.get("password")

        admin = Admin.query.filter_by(password=admin_password).first()

        if admin:
            session["admin"] = admin.name

            new_semester = request.form.get("semester")
            new_year = request.form.get("year")

            updated = False

            if new_semester:
                YearsOfStudy.query.update({YearsOfStudy.semester: new_semester})
                updated = True

            if new_year:
                YearsOfStudy.query.update({YearsOfStudy.years_of_study: new_year})
                updated = True

            if updated:
                db.session.commit()
                flash("Semester/Year updated for all students!", "success")
            else:
                flash("No updates provided", "warning")

            return redirect(url_for("admin.admin_page"))
        else:
            flash("Invalid admin password", "danger")

    return render_template("admin.html")
