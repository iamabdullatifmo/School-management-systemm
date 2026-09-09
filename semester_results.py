from flask import Blueprint, render_template, session
from models import Student, Grades, Courses, YearsOfStudy, SemesterResults
from extentions import db

semester_results_bp = Blueprint("semester_results", __name__)


@semester_results_bp.route("/semester_results", methods=["POST", "GET"])
def semester_results():

    student_id = session.get("student_id")

    if not student_id:
        return "Student not logged in", 401

    gpa = None
    cgpa = None
    results = []

    # 1. GET STUDENT'S CURRENT YEAR / LEVEL / SEMESTER

    study = (
        YearsOfStudy.query
        .filter_by(student_id=student_id)
        .order_by(YearsOfStudy.years_id.desc())
        .first()
    )

    if not study:
        return render_template(
            "semester_results.html",
            results=[],
            gpa=None,
            cgpa=None,
            semester=None,
            year=None,
            level=None
        )

    year = study.year
    level = study.level
    semester = study.semester


    # 2. GET THE STUDENT'S GRADES

    grades = (
        Grades.query
        .filter_by(student_id=student_id)
        .all()
    )

    total_points = 0
    total_credit_h = 0


    # 3. CALCULATE COURSE GRADES

    for g in grades:

        course = Courses.query.get(g.course_id)

        if not course:
            continue

        score = float(g.grade)


        # Convert mark to letter grade + grade point

        if score >= 85:
            grade_letter = "A+"
            grade_point = 5

        elif score >= 80:
            grade_letter = "A"
            grade_point = 4.5

        elif score >= 75:
            grade_letter = "B+"
            grade_point = 4

        elif score >= 70:
            grade_letter = "B"
            grade_point = 3.5

        elif score >= 65:
            grade_letter = "C+"
            grade_point = 3

        elif score >= 60:
            grade_letter = "C"
            grade_point = 2.5

        elif score >= 55:
            grade_letter = "D+"
            grade_point = 1.5

        elif score >= 50:
            grade_letter = "D"
            grade_point = 1

        else:
            grade_letter = "F"
            grade_point = 0


        # Add course to results

        results.append({
            "course_name": course.course_name,
            "mark": score,
            "letter": grade_letter,
            "point": grade_point,
            "credit_h": course.credit_h
        })


        # Calculate total points

        total_points += grade_point * course.credit_h

        total_credit_h += course.credit_h


    # 4. CALCULATE GPA

    if total_credit_h > 0:

        gpa = total_points / total_credit_h


    # 5. GET PREVIOUS SEMESTER RESULTS

    previous_results = (
        SemesterResults.query
        .filter_by(student_id=student_id)
        .all()
    )


    # 6. CALCULATE CGPA

    previous_gpas = [
        r.gpa
        for r in previous_results
        if r.gpa is not None
    ]


    if gpa is not None:

        if previous_gpas:

            cgpa = (
                sum(previous_gpas) + gpa
            ) / (
                len(previous_gpas) + 1
            )

        else:

            cgpa = gpa


    # 7. CHECK IF THIS SEMESTER RESULT ALREADY EXISTS

    existing_result = (
        SemesterResults.query
        .filter_by(
            student_id=student_id,
            semester=semester
        )
        .first()
    )


    # 8. SAVE SEMESTER RESULT

    if not existing_result:

        sem_result = SemesterResults(
            student_id=student_id,
            semester=semester,
            gpa=gpa,
            cgpa=cgpa
        )

        db.session.add(sem_result)

        db.session.commit()


    # 9. DISPLAY RESULTS

    return render_template(
        "semester_results.html",
        results=results,
        gpa=gpa,
        cgpa=cgpa,
        semester=semester,
        year=year,
        level=level
    )
