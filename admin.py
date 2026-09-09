from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import YearsOfStudy, Admin
from extentions import db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["POST", "GET"])
def admin_page():
    if request.method == "POST":
        
        admin_password = request.form.get("password")

        admin = Admin.query.filter_by(password=admin_password).first()
        if not admin:
            flash("Invalid admin password.", "error")
            return redirect(url_for("admin.admin_page"))
        session["admin"] = admin.name
        session["admin"] = True
        return redirect(url_for("admin.admin_update"))

    return render_template("admin.html")    

@admin_bp.route("/admin_update", methods=["POST", "GET"])
def admin_update():
        admin = session.get("admin")
        
        new_semester = request.form.get("semester", type =int)
        new_year = request.form.get("years", type=int)

        if request.method == "POST":

            # Loop through all the existing students
            years_of_study = YearsOfStudy.query.all()
            for students in years_of_study:            
                if new_semester:
                    students.semester = new_semester

                    if new_year:
                        students.year = new_year

                    if students.level < students.years_of_study * 100:
                        students.level += 100

            db.session.commit()

            flash("Years of study updated successfully.", "success")
        return render_template("admin_post.html")


