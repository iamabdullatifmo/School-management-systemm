from flask import Blueprint,render_template,request,flash,session,redirect,url_for
from models import Lecturers,Student,Courses,Grades,StudentCourses
from extentions import db,mail
from flask_mail import Message


upload_results_bp = Blueprint ("upload_results",__name__)

@upload_results_bp.route("/upload_results", methods=["POST","GET"])
def upload_results_view():
   lec_id = session.get("lec_id")
   # I first define the list of student as empty then when the lecturer posts the request it fetches the query in line 15
   students = []
   grades = []
   if request.method == "POST":
        department = request.form.get("department")
        course = request.form.get("course")
        # Join the Course model to the student model to get access to courses
        if department and course:  
            
            flash("Students fetched successfully")
            students = Student.query.join(StudentCourses, Student._id == StudentCourses.student_id).join(Courses, StudentCourses.course_id == Courses.course_id).filter(Student.department == department, Courses.course_id == course).all()
            grades = Grades.query.join(Student, Grades.student_id == Student._id).filter(Student.department == department, Grades.course_id == course).all()

            for student in students:
                  get_grade = request.form.get(f"grade_{student._id}")
                  if get_grade:
                      grade = Grades(student_id=student._id, course_id=course, grade=get_grade)
                      db.session.add(grade)
            db.session.commit()
            flash("Grades saved successfully")

            emails = [s.email for s in students]  # build list of emails
            names_of_students = [n.full_Name for n in students]# Get all the names 
            msg = Message(subject="School management", recipients=emails)
            msg.html = f""""
                        Hi {names_of_students}, <br>
                        the semester results of {course} has been released,
                        you can visit the portal to check the results <br>
                        From mangement.
            
            """
            mail.send(msg)
            return redirect(url_for("upload_results.upload_results_view",department=department, course=course))

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
           
   return render_template("upload_results.html", students=students,grades=grades)

    


