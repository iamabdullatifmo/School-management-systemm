from flask import Blueprint,render_template,url_for,redirect,session,flash
from models import Student,Grades,Courses
from check_results import grade_letter,grade_point,total_points,total_credit_h

semester_results_bp = Blueprint("semester_results",__name__)

@semester_results_bp.route("/semester_results", methods=["POST","GET"])
def semester_results():
    student_id = session.get("student_id")
    gpa = None
    cgpa = None
    results = []
    grades = Grades.query.filter_by(student_id=student_id).all()
    credit_h =Student.query.join(Courses,student_id=student_id).query.filter_by(credit_h).all


    for g in grades:
         course = Courses.query.get(g.course_id)
         score = float(g.grade)
   
               # Convert numeric score → letter + grade point
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
         g.letter = grade_letter
         g.point = grade_point
         g.credit_h = course.credit_h
   
         # Accumulate totals
         total_points += grade_point * course.credit_h
         total_credit_h += course.credit_h
   
    # Final GPA/CGPA
    if total_credit_h > 0:
       gpa = total_points / total_credit_h
       cgpa = gpa 


