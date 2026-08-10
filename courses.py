from flask import Blueprint,render_template,request,url_for,session
from models import Courses,StudentCourses,Student
from extentions import db

courses_bp = Blueprint("courses",__name__)

@courses_bp.route("/courses", methods =["POST","GET"])
def courses():
         if request.method == "POST":
              student_id = session.get("student_id")
              answer = request.form.get("submit")
             # Check if student already registered courses
            #  existing_courses = StudentCourses.query.filter_by(student_id=student_id).all()
             # if first_seven:
                #  return render_template("courses.html", courses=first_seven)

              if answer == "yes":
                  first_seven = Courses.query.limit(7).all()
                  #Store courses in the student_courses table
                  for course in first_seven:
                    store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                    db.session.add(store_courses) 
                  db.session.commit()

                  return render_template("courses.html", courses=first_seven)
              else:
                    return render_template("index.html")
         return render_template("pay_fees.html")