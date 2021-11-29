from flask import request
from flask_restx import Resource, Namespace, fields
from application.api.controller.api_controller import ApiController
from infrastructure.api.api_exceptions import ApiException
from infrastructure.handle_exception_messages import handle_message

api = Namespace('Api', description='Api APIs')
api_model = api.model('apis', {
    'name': fields.String(required=True, description='接口名称', min_length=2),
    'variables': fields.Raw(required=False, description='变量'),
    'request': fields.Raw(required=False, description='接口信息'),
    'validate': fields.Raw(required=False, description='断言'),
    'extract': fields.Raw(required=False, description='提取'),
    'setup_hooks': fields.Raw(required=False, description='前置执行'),
})


@api.route('/apis')
class ApisResource(Resource):

    def get(self):
        api_controller = ApiController()
        return {'apis': [api.as_json() for api in api_controller.get_api_list()]}

    @api.expect(api_model, validate=True)
    def post(self):
        api_controller = ApiController()
        data = request.get_json(force=True)

        try:
            api_controller.create_api(  name=data['name'],
                                        variables=data['variables'],
                                        request=data['request'],
                                        validate=data['validate'],
                                        extract=data['extract'],
                                        setup_hooks=data['setup_hooks'],
                                              
                                              )
            return {'message': 'api successfully created'}, 201
        except ApiException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500


@api.route('/api/<id>')
@api.param('id', 'api identifier')
class ApiResource(Resource):

    def get(self, id):
        api_controller = ApiController()
        try:
            api = api_controller.get_api(id)
            if not api:
                return {'message': 'api {} not found.'.format(id)}, 409

            return api.as_json()
        except ApiException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500

    @api.expect(api_model, validate=True)
    def put(self, id):
        api_controller = ApiController()
        data = request.get_json(force=True)

        try:
            api_controller.update_api(  str(id),
                                        data['name'],
                                        data['variables'],
                                        data['request'],
                                        data['validate'],
                                        data['extract'],
                                        data['setup_hooks'])

            return {'message': 'api successfully updated.'}, 201
        except ApiException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500
