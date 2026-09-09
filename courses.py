from flask import Blueprint,render_template,request,url_for,session
from models import Courses,StudentCourses,Student,YearsOfStudy
from extentions import db

courses_bp = Blueprint("courses",__name__)

@courses_bp.route("/courses", methods =["POST","GET"])
def courses():
         if request.method == "POST":
              student_id = session.get("student_id")
              answer = request.form.get("submit")

              if answer == "yes":
                  courses = Courses.query.limit(7).all()
                  check_level = db.session.execute(db.select(YearsOfStudy.level,YearsOfStudy.semester).where(YearsOfStudy.student_id==student_id)).first()
                  if check_level.semester == 1 and check_level.level == 100:
                  #Store courses in the student_courses table
                   for course in courses:
                      store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                      db.session.add(store_courses) 
                   db.session.commit()
                   return render_template("courses.html", courses=courses)
                  
                  elif check_level.semester == 2 and check_level.level == 100:
                     #Jump the first 7 courses
                     courses = Courses.query.offset(7).limit(7).all()
                     for course in courses:
                        store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                        db.session.add(store_courses) 
                     db.session.commit()
                     return render_template("courses.html", courses=courses)

                  elif check_level.semester == 1 and check_level.level == 200:
                     #Jump the first 7 courses
                     courses = Courses.query.offset(14).limit(7).all()
                     for course in courses:
                        store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                        db.session.add(store_courses) 
                     db.session.commit()
                     return render_template("courses.html", courses=courses)

                  
                  elif check_level.semester == 2 and check_level.level == 200:
                     #Jump the first 7 courses
                     courses = Courses.query.offset(21).limit(7).all()
                     for course in courses:
                        store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                        db.session.add(store_courses) 
                     db.session.commit()
                     return render_template("courses.html", courses=courses)

                  elif check_level.semester == 1 and check_level.level == 300:
                     #Jump the first 7 courses
                     courses = Courses.query.offset(28).limit(7).all()
                     for course in courses:
                        store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                        db.session.add(store_courses) 
                     db.session.commit()
                     return render_template("courses.html", courses=courses)

                  elif check_level.semester == 2 and check_level.level == 300:
                     #Jump the first 7 courses
                     courses = Courses.query.offset(35).limit(5).all()
                     for course in courses:
                        store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                        db.session.add(store_courses) 
                     db.session.commit()
                     return render_template("courses.html", courses=courses)

                  
                  elif check_level.semester == 1 and check_level.level == 400:
                     #Jump the first 7 courses
                     courses = Courses.query.offset(40).limit(5).all()
                     for course in courses:
                        store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                        db.session.add(store_courses) 
                     db.session.commit()
                     return render_template("courses.html", courses=courses)

                  
                  elif check_level.semester == 2 and check_level.level == 400:
                     #Jump the first 7 courses
                     courses = Courses.query.offset(45).limit(5).all()
                     for course in courses:
                        store_courses = StudentCourses(student_id=student_id,course_id=course.course_id)
                        db.session.add(store_courses) 
                     db.session.commit()
                     return render_template("courses.html", courses=courses)




                  
              else:
                    return render_template("index.html")
         return render_template("pay_fees.html")