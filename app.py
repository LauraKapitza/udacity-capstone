from flask import jsonify, abort, request

from auth.auth import requires_auth, AuthError
from config import app
from models import *

PAGE_LIMIT = 10


def paginate_models(page, models):
    start = (page - 1) * PAGE_LIMIT
    end = start + PAGE_LIMIT

    formatted_data = [model.format_long() for model in models]
    sliced_data = formatted_data[start:end]

    return sliced_data


# ---------------------------------------------------------------------------- #
# Class routes
# ---------------------------------------------------------------------------- #

@app.route('/')
@requires_auth("classes:read")
def get_classes(payload):
    # try:
    page = request.args.get("page", 1, type=int)
    classes = Class.query.order_by(Class.id).all()
    paginated_classes = paginate_models(page, classes)

    return jsonify({
        "success": True,
        "classes": paginated_classes,
        "total_classes": len(classes),
    })


# except Exception as err:
#     print(err)
#     abort(422)

@app.route('/<int:class_id>')
@requires_auth("classes:read")
def get_class(payload, class_id):
    dance_class = Class.query.filter_by(id=class_id).first_or_404()

    return jsonify({
        "success": True,
        "class": dance_class.format_long(),
    })


@app.route('/', methods=["POST"])
@requires_auth("classes:create")
def create_class(payload):
    body = request.get_json()

    # creates new dance class
    new_class = Class(
        teacher_id=payload["sub"],
        dance_types=body.get("dance_types", []),
        title=body.get("title", None),
        description=body.get("description", None),
        max_participants=body.get("max_participants", None),
        date=body.get("date", None),
        start_time=body.get("start_time", None),
        end_time=body.get("end_time", None)
    )
    new_class.insert()

    return jsonify({
        "success": True,
        "class": new_class.format_long()
    })


# route for students to add themselves to a dance class
@app.route('/<int:class_id>/participants', methods=["POST"])
@requires_auth("classes:update")
def add_participant(payload, class_id):
    dance_class = Class.query.filter_by(id=class_id).first_or_404()

    # finds student by user id
    user_id = payload["sub"]
    student = Student.query.filter_by(id=user_id).first_or_404()

    # throws error when user is already a participant
    if student in dance_class.participants:
        abort(400)

    # adds participant to class
    dance_class.participants.append(student)
    dance_class.update()

    return jsonify({
        "success": True,
        "class_id": class_id,
        "added_participant": student.format_short()
    })


# route for students to add themselves to a dance class
@app.route('/<int:class_id>/participants', methods=["DELETE"])
@requires_auth("classes:update")
def remove_participant(payload, class_id):
    dance_class = Class.query.filter_by(id=class_id).first_or_404()

    # finds student by user id
    user_id = payload["sub"]
    student = Student.query.filter_by(id=user_id).first_or_404()

    # throws error when user is not a participant
    if student not in dance_class.participants:
        abort(400)

    # removes participant from class
    dance_class.participants.remove(student)
    dance_class.update()

    return jsonify({
        "success": True,
        "class_id": class_id,
        "removed_participant": student.format_short()
    })


# route for teachers to update an existing dance class
@app.route('/<int:class_id>', methods=["PATCH"])
@requires_auth("classes:update")
def update_class(payload, class_id):
    # gets potential  new dance class values
    body = request.get_json()
    user_id = payload["sub"]
    body_fields = [
        {"name": "dance_types", "value": body.get("dance_types", [])},
        {"name": "title", "value": body.get("title", None)},
        {"name": "description", "value": body.get("description", None)},
        {"name": "date", "value": body.get("date", None)},
        {"name": "start_time", "value": body.get("start_time", None)},
        {"name": "end_time", "value": body.get("end_time", None)},
    ]

    # checks if user is the teacher of the given dance class
    dance_class = Class.query.filter_by(id=class_id, teacher_id=user_id).first_or_404()

    # updates dance class with new values if exist
    for field in body_fields:
        field_value = field["value"]
        if field_value:
            setattr(dance_class, field["name"], field_value)

    dance_class.update()

    return jsonify({
        "success": True,
        "class": dance_class.format_long()
    })


@app.route('/<int:class_id>', methods=["DELETE"])
@requires_auth("classes:delete")
def delete_class(payload, class_id):
    dance_class = Class.query.filter_by(id=class_id).first_or_404()
    dance_class.delete()

    return jsonify({
        "success": True,
        "deleted": class_id,
    })


# ---------------------------------------------------------------------------- #
# Teacher routes
# ---------------------------------------------------------------------------- #

@app.route('/teachers')
@requires_auth("teachers:read")
def get_teachers():
    # try:
    page = request.args.get("page", 1, type=int)
    teachers = Teacher.query.order_by(Teacher.last_name).all()
    paginated_teachers = paginate_models(page, teachers)

    return jsonify({
        "success": True,
        "teachers": paginated_teachers,
        "total_teachers": len(teachers),
    })


# except Exception as err:
#     print(err)
#     abort(422)

@app.route('/teachers', methods=["POST"])
@requires_auth("teachers:create")
def add_teacher():
    body = request.get_json()

    teacher = Teacher(
        id=body.get("user_id", None),
        first_name=body.get("first_name", None),
        last_name=body.get("last_name", None),
        dance_types=body.get("dance_types", [])
    )

    teacher.insert()

    return jsonify({
        "success": True,
        "teacher": teacher.format_long()
    })

# TODO create teachers/me for a teacher to get their details
@app.route('/teachers/<int:teacher_id>')
@requires_auth("teachers:read")
def get_teacher(teacher_id):
    # try:
    teacher = Teacher.query.filter_by(id=teacher_id).first_or_404()

    return jsonify({
        "success": True,
        "teacher": teacher.format_long()
    })


# except Exception as err:
#     print(err)
#     abort(422)

# TODO add logic for teacher  to update their details
@app.route('/teachers/<int:teacher_id>', methods=["PATCH"])
@requires_auth("teachers:update")
def update_teacher(teacher_id):
    body = request.get_json()
    body_fields = [
        {"name": "dance_types", "value": body.get("dance_types", [])},
        {"name": "first_name", "value": body.get("first_name", None)},
        {"name": "last_name", "value": body.get("last_name", None)}
    ]

    teacher = Teacher.query.filter_by(id=teacher_id).first_or_404()

    # updates teacher with new values if exist
    for field in body_fields:
        field_value = field["value"]
        if field_value:
            setattr(teacher, field["name"], field_value)

    teacher.update()

    return jsonify({
        "success": True,
        "teacher": teacher.format_long()
    })


@app.route('/teachers/<int:teacher_id>', methods=["DELETE"])
@requires_auth("teachers:delete")
def delete_teacher(teacher_id):
    teacher = Teacher.query.filter_by(id=teacher_id).first_or_404()
    teacher.delete()

    return jsonify({
        "success": True,
        "deleted": teacher_id,
    })


# ---------------------------------------------------------------------------- #
# Student routes
# ---------------------------------------------------------------------------- #

@app.route('/students')
@requires_auth("students:read")
def get_students(payload):
    # try:
    page = request.args.get("page", 1, type=int)
    students = Student.query.order_by(Student.last_name).all()
    paginated_students = paginate_models(page, students)

    return jsonify({
        "success": True,
        "students": paginated_students,
        "total_students": len(students),
    })


# except Exception as err:
#     print(err)
#     abort(422)

# TODO add logic for student to create student
@app.route('/students', methods=["POST"])
@requires_auth("students:create")
def add_student(payload):
    body = request.get_json()

    student = Student(
        id=body.get("id", None),
        first_name=body.get("first_name", None),
        last_name=body.get("last_name", None)
    )

    student.insert()

    return jsonify({
        "success": True,
        "student": student.format_long()
    })

# TODO change students:add to all:read to have a generic read permission for all user types
@app.route('/students/<string:student_id>')
def get_student(student_id):
    print(student_id)
    # try:
    student = Student.query.filter_by(id=student_id).first_or_404()

    return jsonify({
        "success": True,
        "student": student.format_long()
    })


# except Exception as err:
#     print(err)
#     abort(422)

# TODO add logic for student to change their details
@app.route('/students/<int:student_id>', methods=["PATCH"])
@requires_auth("students:update")
def update_student(student_id):
    body = request.get_json()
    body_fields = [
        {"name": "first_name", "value": body.get("first_name", None)},
        {"name": "last_name", "value": body.get("last_name", None)}
    ]

    student = Student.query.filter_by(id=student_id).first_or_404()

    # updates student with new values if exist
    for field in body_fields:
        field_value = field["value"]
        if field_value:
            setattr(student, field["name"], field_value)

    student.update()

    return jsonify({
        "success": True,
        "student": student.format_long()
    })


#TODO add admin:delete role for admin to delete stuff
@app.route('/students/<int:student_id>', methods=["DELETE"])
@requires_auth("students:delete")
def delete_student(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    student.delete()

    return jsonify({
        "success": True,
        "deleted": student_id,
    })


# ---------------------------------------------------------------------------- #
# Dance type routes
# ---------------------------------------------------------------------------- #

@app.route('/dance-types')
def get_dance_types():
    # try:
    dance_types = [type.format() for type in DanceTypes]

    return jsonify({
        "success": True,
        "dance_types": dance_types,
        "total_dance_types": len(dance_types),
    })


# except Exception as err:
#     print(err)
#     abort(422)


# ---------------------------------------------------------------------------- #
# Error handlers
# ---------------------------------------------------------------------------- #

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unauthorized'
    }), 401


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": 'Resource not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500

# ---------------------------------------------------------------------------- #
# Launch
# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    app.run()
