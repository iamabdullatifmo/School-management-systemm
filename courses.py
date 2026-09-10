from flask import Blueprint, render_template, request, session
from models import Courses, StudentCourses, YearsOfStudy, AcademicSession
from extentions import db

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/courses", methods=["POST", "GET"])
def courses():

    student_id = session.get("student_id")

    # Make sure student is logged in
    if not student_id:
        return "Please login again.", 401

    # GET CURRENT ACADEMIC SESSION

    current_session = AcademicSession.query.filter_by(
        registration_open=True
    ).first()

    if current_session is None:
        return "Course registration is currently closed.", 403


    current_semester = current_session.semester
    current_year = current_session.academic_year

    # CHECK IF STUDENT ALREADY REGISTERED
    # FOR THIS ACADEMIC SESSION

    registered_courses = StudentCourses.query.filter_by(
        student_id=student_id,
        academic_year=current_year,
        semester=current_semester
    ).all()


    # If courses already registered,
    # show them immediately
    if registered_courses:

        courses = Courses.query.filter(
            Courses.course_id.in_(
                [course.course_id for course in registered_courses]
            )
        ).all()

        return render_template(
            "courses.html",
            courses=courses,
            academic_year=current_year,
            semester=current_semester
        )

    # IF NOT REGISTERED, CHECK PAYMENT PAGE

    if request.method == "GET":
        return render_template("pay_fees.html")

    # PAYMENT PAGE SUBMITTED
    answer = request.form.get("submit")

    if answer != "yes":
        return render_template("index.html")

    # GET STUDENT LEVEL

    check_level = db.session.execute(
        db.select(
            YearsOfStudy.level
        ).where(
            YearsOfStudy.student_id == student_id
        )
    ).first()


    if check_level is None:
        return "Student academic information was not found.", 404


    level = check_level.level

    # DETERMINE COURSES

    if level == 100 and current_semester == 1:

        offset = 0
        limit = 7

    elif level == 100 and current_semester == 2:

        offset = 7
        limit = 7

    elif level == 200 and current_semester == 1:

        offset = 14
        limit = 7

    elif level == 200 and current_semester == 2:

        offset = 21
        limit = 7

    elif level == 300 and current_semester == 1:

        offset = 28
        limit = 7

    elif level == 300 and current_semester == 2:

        offset = 35
        limit = 5

    elif level == 400 and current_semester == 1:

        offset = 40
        limit = 5

    elif level == 400 and current_semester == 2:

        offset = 45
        limit = 5

    else:

        return "No courses are available for your level.", 404

    # GET COURSES

    courses = Courses.query.offset(offset).limit(limit).all()


    if not courses:
        return "No courses are available.", 404

    # SAVE COURSES

    for course in courses:

        store_courses = StudentCourses(
            student_id=student_id,
            course_id=course.course_id,
            academic_year=current_year,
            semester=current_semester
        )

        db.session.add(store_courses)

    db.session.commit()

    # SHOW REGISTERED COURSES

    return render_template(
        "courses.html",
        courses=courses,
        academic_year=current_year,
        semester=current_semester
    )
