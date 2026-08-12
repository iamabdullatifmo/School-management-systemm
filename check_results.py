from flask import Blueprint, session, render_template
from models import Grades, Courses

check_results_bp = Blueprint("check_result", __name__)

@check_results_bp.route("/check_results", methods=["GET"])
def check_results():
    student_id = session.get("student_id")
    grades = []
    gpa = 0.0

    if student_id:
        grades = Grades.query.filter_by(student_id=student_id).all()

        total_points = 0
        total_credit_h = 0
        # Now look through the Grades table and fetch course_id for me 
        # Course id is a foreign key in the Grades table
        for g in grades:
            course = Courses.query.get(g.course_id)
            if not course or g.grade is None:
                continue

            score = float(g.grade)

            if score >= 85:
                grade_letter, grade_point = "A+", 5
            elif score >= 80:
                grade_letter, grade_point = "A", 4.5
            elif score >= 75:
                grade_letter, grade_point = "B+", 4
            elif score >= 70:
                grade_letter, grade_point = "B", 3.5
            elif score >= 65:
                grade_letter, grade_point = "C+", 3
            elif score >= 60:
                grade_letter, grade_point = "C", 2.5
            elif score >= 55:
                grade_letter, grade_point = "D+", 1.5
            elif score >= 50:
                grade_letter, grade_point = "D", 1
            else:
                grade_letter, grade_point = "F", 0

            # Attach values for template
            g.course_name = course.course_name
            g.mark = score
            g.letter = grade_letter
            g.point = grade_point
            g.credit_h = course.credit_h

            # Accumulate totals
            total_points += grade_point * course.credit_h
            total_credit_h += course.credit_h

        # Final GPA
        if total_credit_h > 0:
            gpa = total_points / total_credit_h
            cgpa = gpa 

    return render_template("check_results.html", grades=grades, gpa=gpa)
