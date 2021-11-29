from flask import request
from flask_restx import Resource, Namespace, fields
from application.student.controller.student_controller import StudentController
from infrastructure.student.student_exceptions import StudentException
from infrastructure.handle_exception_messages import handle_message

api = Namespace('Student', description='Student APIs')
student_model = api.model('students', {
    'name': fields.String(required=True, description='name value', min_length=2),
    'surname': fields.String(required=True, description='surname value', min_length=2),
    'tel': fields.String(required=True, description='tel value', min_length=2),
})


@api.route('/students')
class StudentsResource(Resource):

    def get(self):
        student_controller = StudentController()
        return {'students': [student.as_json() for student in student_controller.get_student_list()]}

    @api.expect(student_model, validate=True)
    def post(self):
        student_controller = StudentController()
        data = request.get_json(force=True)

        try:
            student_controller.create_student(name=data['name'],
                                              surname=data['surname'],
                                              tel=data['tel'])
            return {'message': 'Student successfully created'}, 201
        except StudentException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500


@api.route('/student/<id>')
@api.param('id', 'Student identifier')
class StudentResource(Resource):

    def get(self, id):
        student_controller = StudentController()
        try:
            student = student_controller.get_student(id)
            if not student:
                return {'message': 'Student {} not found.'.format(id)}, 409

            return student.as_json()
        except StudentException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500

    @api.expect(student_model, validate=True)
    def put(self, id):
        student_controller = StudentController()
        data = request.get_json(force=True)

        try:
            student_controller.update_student(str(id),
                                              data['name'],
                                              data['surname'],
                                              data['tel'])

            return {'message': 'Student successfully updated.'}, 201
        except StudentException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500
