from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for
)

from models import Student, Courses, Grades, StudentCourses
from extentions import db


upload_results_bp = Blueprint("upload_results", __name__)


@upload_results_bp.route("/upload_results", methods=["GET", "POST"])
def upload_results_view():

    # --------------------------------------------------
    # GET LECTURER ID
    # --------------------------------------------------

    lec_id = session.get("lec_id")

    # --------------------------------------------------
    # INITIAL VALUES
    # --------------------------------------------------

    students = []
    grade_map = {}

    department = (
        request.form.get("department")
        or request.args.get("department")
    )

    course = (
        request.form.get("course")
        or request.args.get("course")
    )

    # --------------------------------------------------
    # FETCH REGISTERED STUDENTS
    # --------------------------------------------------

    if request.method == "POST" and request.form.get("fetch_students"):

        if not department or not course:

            flash(
                "Please select a department and course.",
                "error"
            )

        else:

            # ------------------------------------------
            # CHECK THAT COURSE EXISTS
            # ------------------------------------------

            selected_course = Courses.query.filter_by(
                course_id=course
            ).first()

            if not selected_course:

                flash(
                    f"Course {course} was not found.",
                    "error"
                )

            else:

                # --------------------------------------
                # GET REGISTERED STUDENTS
                # --------------------------------------

                students = (
                    Student.query
                    .join(
                        StudentCourses,
                        Student._id == StudentCourses.student_id
                    )
                    .filter(
                        Student.department == department,
                        StudentCourses.course_id == course
                    )
                    .all()
                )

                if not students:

                    flash(
                        f"No students are registered for "
                        f"{course} under {department}.",
                        "error"
                    )

    # --------------------------------------------------
    # SAVE GRADES
    # --------------------------------------------------

    elif request.method == "POST" and request.form.get("save_grades"):

        if not department or not course:

            flash(
                "Department and course are required.",
                "error"
            )

            return redirect(
                url_for(
                    "upload_results.upload_results_view"
                )
            )

        # ----------------------------------------------
        # CHECK THAT COURSE EXISTS
        # ----------------------------------------------

        selected_course = Courses.query.filter_by(
            course_id=course
        ).first()

        if not selected_course:

            flash(
                f"Course {course} was not found.",
                "error"
            )

            return redirect(
                url_for(
                    "upload_results.upload_results_view"
                )
            )

        # ----------------------------------------------
        # GET REGISTERED STUDENTS
        # ----------------------------------------------

        students = (
            Student.query
            .join(
                StudentCourses,
                Student._id == StudentCourses.student_id
            )
            .filter(
                Student.department == department,
                StudentCourses.course_id == course
            )
            .all()
        )

        if not students:

            flash(
                f"No students are registered for "
                f"{course} under {department}.",
                "error"
            )

            return redirect(
                url_for(
                    "upload_results.upload_results_view",
                    department=department,
                    course=course
                )
            )

        # ----------------------------------------------
        # VALIDATION
        # ----------------------------------------------

        errors = []
        updated_count = 0

        for student in students:

            field_name = f"grade_{student._id}"

            grade_value = request.form.get(field_name)

            # Empty input means:
            # keep existing grade unchanged
            if grade_value is None or grade_value.strip() == "":
                continue

            # ------------------------------------------
            # CONVERT GRADE
            # ------------------------------------------

            try:
                grade_value = float(grade_value)

            except (ValueError, TypeError):

                errors.append(
                    f"Invalid grade for {student.full_Name}."
                )

                continue

            # ------------------------------------------
            # VALIDATE RANGE
            # ------------------------------------------

            if not 0 <= grade_value <= 100:

                errors.append(
                    f"Grade for {student.full_Name} "
                    f"must be between 0 and 100."
                )

                continue

            # ------------------------------------------
            # FIND EXISTING GRADE
            # ------------------------------------------

            existing_grade = (
                Grades.query
                .filter_by(
                    student_id=student._id,
                    course_id=course
                )
                .first()
            )

            if existing_grade:

                # Update existing grade
                existing_grade.grade = grade_value

            else:

                # Create new grade
                new_grade = Grades(
                    student_id=student._id,
                    course_id=course,
                    grade=grade_value
                )

                db.session.add(new_grade)

            updated_count += 1

        # ----------------------------------------------
        # HANDLE VALIDATION ERRORS
        # ----------------------------------------------

        if errors:

            db.session.rollback()

            for error in errors:
                flash(error, "error")

        else:

            # ------------------------------------------
            # COMMIT CHANGES
            # ------------------------------------------

            try:

                db.session.commit()

                flash(
                    f"{updated_count} grade(s) "
                    f"saved successfully.",
                    "success"
                )

            except Exception as e:

                db.session.rollback()

                print(
                    "ERROR saving grades:",
                    e,
                    flush=True
                )

                flash(
                    "An error occurred while saving "
                    "the grades.",
                    "error"
                )

        # ----------------------------------------------
        # REDIRECT AFTER SAVE
        # ----------------------------------------------

        return redirect(
            url_for(
                "upload_results.upload_results_view",
                department=department,
                course=course
            )
        )

    # --------------------------------------------------
    # GET REQUEST / AFTER SAVE REDIRECT
    # --------------------------------------------------

    elif request.method == "GET" and department and course:

        students = (
            Student.query
            .join(
                StudentCourses,
                Student._id == StudentCourses.student_id
            )
            .filter(
                Student.department == department,
                StudentCourses.course_id == course
            )
            .all()
        )

    # --------------------------------------------------
    # GET EXISTING GRADES
    # --------------------------------------------------

    if students and course:

        student_ids = [
            student._id
            for student in students
        ]

        grades = (
            Grades.query
            .filter(
                Grades.course_id == course,
                Grades.student_id.in_(student_ids)
            )
            .all()
        )

        grade_map = {
            grade.student_id: grade.grade
            for grade in grades
        }

    # --------------------------------------------------
    # RENDER PAGE
    # --------------------------------------------------

    return render_template(
        "upload_results.html",
        students=students,
        grade_map=grade_map,
        department=department,
        course=course
    )
