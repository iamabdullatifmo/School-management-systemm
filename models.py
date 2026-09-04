from extentions import db
import uuid
from datetime import date


class Lecturers(db.Model):
    @staticmethod
    def generate_matrix():
        return str(uuid.uuid4())[:10]
    __tablename__="lecturers"
    lec_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    first_N = db.Column(db.String(20))
    last_N = db.Column(db.String(20))
    email = db.Column(db.String(100))
    full_Name = db.Column(db.String(200))
    password = db.Column(db.String(20), default=lambda: Lecturers.generate_matrix())
    department = db.Column(db.String(200))

class Student(db.Model):
    def generate_matrix():
        return str(uuid.uuid4())[:10]
    @property
    def btit_id(self):
        return f"BTIT230{self._id:02d}"
    
    __tablename__ = "student"
    _id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    first_N = db.Column(db.String(20))
    last_N = db.Column(db.String(20))
    email = db.Column(db.String(100))
    full_Name = db.Column(db.String(200))
    password = db.Column(db.String(20),default=generate_matrix)
    department = db.Column(db.String(200))

class Courses(db.Model):
        __tablename__ ="courses"
        course_id = db.Column(db.String(10), primary_key=True)
        course_name = db.Column(db.String(100))
        _id = db.Column(db.Integer(),db.ForeignKey("student._id"))
        lec_id = db.Column(db.Integer(),db.ForeignKey("lecturers.lec_id"))
        credit_h = db.Column(db.Integer())

class Department(db.Model):
         __tablename__ ="department"
         id = db.Column(db.Integer, primary_key=True, autoincrement=True)
         dept_id = db.Column(db.String(10), unique=True)
         dept_name = db.Column(db.String(100))
         course_id = db.Column(db.String(10),db.ForeignKey("courses.course_id"))
         _id = db.Column(db.Integer(),db.ForeignKey("student._id"))
         lec_id = db.Column(db.Integer(),db.ForeignKey("lecturers.lec_id"))

class Grades(db.Model):
     __tablename__ = "grades"    
     grade_id = db.Column(db.Integer,primary_key=True,autoincrement=True)   
     student_id  = db.Column(db.Integer, db.ForeignKey("student._id"),nullable= False)
     course_id = db.Column(db.String(10), db.ForeignKey("courses.course_id"))
     grade = db.Column(db.Numeric(5,2), nullable=False)
     gpa = db.Column(db.Numeric(8,7))
     cgpa = db.Column(db.Numeric(8,7))

class StudentCourses(db.Model):
    __tablename__ = "student_courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student._id"))
    course_id = db.Column(db.String(10), db.ForeignKey("courses.course_id"))

class SemesterResults(db.Model):   
    __tablename__ = "semester_results"
    sem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student._id"), nullable=False)
    semester = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    cgpa = db.Column(db.Float)

    student = db.relationship("Student", backref="semester_results")


class YearsOfStudy(db.Model):
     __tablename__ = "years_of_study"
     years_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     student_id = db.Column(db.Integer, db.ForeignKey("student._id"))
     years_of_study = db.Column(db.Integer)
     semester = db.Column(db.Integer)
     date = db.Column(db.Date, default=date.today)
     level = db.Column(db.Integer)
     year = db.Column(db.Integer)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)



    