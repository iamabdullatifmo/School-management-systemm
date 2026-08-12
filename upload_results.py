from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from models import Lecturers, Student, Courses, Grades, StudentCourses
from extentions import db, mail
from flask_mail import Message

upload_results_bp = Blueprint("upload_results", __name__)

@upload_results_bp.route("/upload_results", methods=["POST", "GET"])
def upload_results_view():
    lec_id = session.get("lec_id")
    students, grades = [], []

    if request.method == "POST":
        department = request.form.get("department")
        course = request.form.get("course")

        if department and course:
            # Fetch students for this department/course
            students = (
                Student.query
                .join(StudentCourses, Student._id == StudentCourses.student_id)
                .join(Courses, StudentCourses.course_id == Courses.course_id)
                .filter(Student.department == department, Courses.course_id == course)
                .all()
            )

            # Fetch existing grades for this course
            grades = (
                Grades.query
                .join(Student, Grades.student_id == Student._id)
                .filter(Student.department == department, Grades.course_id == course)
                .all()
            )

            # Save or update grades
            for student in students:
                get_grade = request.form.get(f"grade_{student._id}")
                if get_grade:
                    existing_grade = Grades.query.filter_by(
                        student_id=student._id,
                        course_id=course
                    ).first()

                    if existing_grade:
                        # Update existing grade
                        existing_grade.grade = get_grade
                    else:
                        # Insert new grade
                        grade = Grades(student_id=student._id, course_id=course, grade=get_grade)
                        db.session.add(grade)

            db.session.commit()
            flash("Grades saved/updated successfully")

            return redirect(url_for("upload_results.upload_results_view",
                                    department=department, course=course))
               # Notify students
            emails = [s.email for s in students]
            names = [s.full_Name for s in students]
            msg = Message(subject="School management", recipients=emails)
            msg.html = f"""
                          Hi {', '.join(names)}, <br>
                          The semester results for {course} have been released.
                          You can visit the portal to check your results. <br>
                          From management.
                        """
            mail.send(msg)

    # Handle GET
    department = request.args.get("department")
    course = request.args.get("course")
    if department and course:
        students = (
            Student.query
            .join(StudentCourses, Student._id == StudentCourses.student_id)
            .join(Courses, StudentCourses.course_id == Courses.course_id)
            .filter(Student.department == department, Courses.course_id == course)
            .all()
        )
        grades = (
            Grades.query
            .join(Student, Grades.student_id == Student._id)
            .filter(Student.department == department, Grades.course_id == course)
            .all()
        )

    return render_template("upload_results.html", students=students, grades=grades)
