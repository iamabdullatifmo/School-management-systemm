from flask import Blueprint,render_template,url_for,redirect,session,flash
from models import Student,Grades,Courses,YearsOfStudy,SemesterResults
from extentions import db

semester_results_bp = Blueprint("semester_results",__name__)

@semester_results_bp.route("/semester_results", methods=["POST","GET"])
def semester_results():
    student_id = session.get("student_id")
    gpa = None
    cgpa = None
    results = []
    grades = Grades.query.filter_by(student_id=student_id).all()
    total_points = 0
    total_credit_h = 0

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
   
         # Accumulate totals
         total_points += grade_point * course.credit_h
         total_credit_h += course.credit_h

     # next semester
    last_result = SemesterResults.query.filter_by(student_id=student_id).order_by(SemesterResults.semester.desc()).first()
    if last_result:
           next_semester = last_result.semester + 1
    else:
          next_semester = 1

    # Calculate CGPA
    all_results = SemesterResults.query.filter_by(student_id=student_id).all()
    if all_results:
        cgpa = sum(r.gpa for r in all_results if r.gpa) / len(all_results)
    
    # Final GPA/CGPA
    if total_credit_h > 0:
       gpa = total_points / total_credit_h
       
    sems_results = SemesterResults(student_id=student_id,semester =1,gpa=gpa,cgpa=cgpa) 
    db.session.add(sems_results)
    db.session.commit()
    return render_template("semester_results.html",results=results,gpa=gpa,cgpa=cgpa,semester=next_semester)

