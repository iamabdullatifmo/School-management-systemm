from flask import Flask,render_template,url_for,request,flash,session,redirect
import uuid
import os
from dotenv import load_dotenv


from extentions import db,mail
from flask_mail import Message

load_dotenv()

app=Flask(__name__)
app.secret_key= os.getenv("SECRET_KEY")

@app.errorhandler(500)
def internal_error(error):
    return render_template("error_debug.html"), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html"), 404


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")



from models import Student,Lecturers,Courses,Department,Grades

from lecturer import lecturer_bp
from student_registration import register_student_bp
from lecturer_registration import register_lecturer_bp
from login import login
from student import student_bp
from bio import bio_bp
from change_password import change_password_bp
from courses import courses_bp
from upload_results import upload_results_bp
from department import department
from check_results import check_results_bp
from semester_results import semester_results_bp
from admin import admin_bp
from admin_update_api import admin_update_api


app.register_blueprint(lecturer_bp,url_prefix="")
app.register_blueprint(register_student_bp,url_prefix="")
app.register_blueprint(register_lecturer_bp,url_prefix="")
app.register_blueprint(login,url_prefix="")
app.register_blueprint(student_bp,url_prefix="")
app.register_blueprint(bio_bp,url_prefix="")
app.register_blueprint(change_password_bp,url_prefix="")
app.register_blueprint(courses_bp,url_prefix="")
app.register_blueprint(upload_results_bp,url_prefix="/lecturer")
app.register_blueprint(department,url_prefix="")
app.register_blueprint(check_results_bp,url_prefix="")
app.register_blueprint(semester_results_bp,url_prefix="")
app.register_blueprint(admin_bp,url_prefix="")
app.register_blueprint(admin_update_api, url_prefix="")


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
app.config["SESSION_PERMANENT"] = False


db.init_app(app)
mail.init_app(app)


@app.route("/home")
@app.route("/")
def home():
    msg = Message(subject="School management",recipients=['touhirabubakr8437@gmail.com'])
    msg.body = " Dear customer you are Welcome to TaTU school system "
    mail.send(msg)
   # return "message was sent"
    return render_template("index.html")
   
    
with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
