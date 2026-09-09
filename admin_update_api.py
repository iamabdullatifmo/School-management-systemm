from flask import Blueprint,render_template,url_for,session,request,jsonify
from models import YearsOfStudy
from extentions import db


admin_update_api = Blueprint("admin_update_api", __name__)

@admin_update_api.route("/api/admin/update-semester_years", methods=["POST"])
def api_update_years():

    # Check if admin is logged in
    if "admin" not in session:
        return {
            "success": False,
            "message": "Unauthorized. Please login as admin."
        }, 401

    # Get JSON data
    data = request.get_json()

    if not data:
        return {
            "success": False,
            "message": "Request body must contain JSON."
        }, 400

    new_semester = data.get("semester")
    new_year = data.get("year")

    # Validate that at least one value was provided
    if new_semester is None and new_year is None:
        return {
            "success": False,
            "message": "Provide semester or year."
        }, 400

    # Validate semester
    if new_semester is not None:
        try:
            new_semester = int(new_semester)
        except (ValueError, TypeError):
            return {
                "success": False,
                "message": "Semester must be an integer."
            }, 400

        if new_semester < 1:
            return {
                "success": False,
                "message": "Semester must be greater than 0."
            }, 400

    # Validate year
    if new_year is not None:
        try:
            new_year = int(new_year)
        except (ValueError, TypeError):
            return {
                "success": False,
                "message": "Year must be an integer."
            }, 400

    # Get all students
    years_of_study = YearsOfStudy.query.all()

    updated_count = 0

    for student in years_of_study:

        if new_semester is not None:
            student.semester = new_semester

        if new_year is not None:
            student.year = new_year

        if student.level < student.years_of_study * 100:
            student.level += 100

        updated_count += 1

    # Save changes
    db.session.commit()

    return {
        "success": True,
        "message": "Years of study updated successfully.",
        "updated_students": updated_count,
        "semester": new_semester,
        "year": new_year
    }, 200

