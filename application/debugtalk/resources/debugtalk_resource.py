from flask import request
from flask_restx import Resource, Namespace, fields
from application.debugtalk.controller.debugtalk_controller import DebugtalkController
from infrastructure.debugtalk.debugtalk_exceptions import DebugtalkException
from infrastructure.handle_exception_messages import handle_message
from infrastructure.response import response
import copy
import os
from application.project.controller.project_controller import ProjectController
from application.debugtalk.controller.debugtalk_controller import DebugtalkController

api = Namespace('debugtalk', description='debugtalk APIs')
debugtalk_model = api.model('debugtalks', {
    'debugtalktext': fields.String(required=False, description='debugtalk'),
    'project_id': fields.String(required=False, description='project_id'),
})


@api.route('/debugtalks')
class DebugtalksResource(Resource):

    def get(self):
        debugtalk_controller = DebugtalkController()
        debugtalks_response = copy.deepcopy(response)
        project_id = request.args.get('project_id')
        debugtalks_response['data']['rows'] = [debugtalk.as_json() for debugtalk in debugtalk_controller.get_debugtalk_list(project_id)]
        debugtalks_response['count'] = len(debugtalks_response['data']['rows'])
        return debugtalks_response

    @api.expect(debugtalk_model, validate=True)
    def post(self):
        new_debugtalk_response = copy.deepcopy(response) 
        debugtalk_controller = DebugtalkController()
        data = request.get_json(force=True)
        print(data)
        project_id = request.args.get('project_id')
        hrproject_path = ProjectController().get_project(project_id).as_json().get('hrproject_path')
        if not hrproject_path:
            new_debugtalk_response['status'] = 200
            new_debugtalk_response['msg'] = '查不到项目信息'
            return new_debugtalk_response
        project_debugtalk = debugtalk_controller.get_debugtalk_list(project_id)

        if len(list(project_debugtalk)) >=1:
            new_debugtalk_response['status'] = 201
            new_debugtalk_response['msg'] = '已存在一个debugtalk文件，请勿重复添加'
            return new_debugtalk_response

        debugtalk_path = os.path.join(hrproject_path,'debugtalk.py')
        try:
            new_debugtalk = debugtalk_controller.create_debugtalk(  
                                        debugtalktext=data.get('debugtalktext'),
                                        project_id=data.get('project_id'),                        
                                              )
            
            new_debugtalk_response['msg'] = 'debugtalk successfully created'
            new_debugtalk_response['data'] =new_debugtalk.as_json()
            debugtalk_controller.save_debugtalk_to_pyfile(data.get('debugtalktext'),debugtalk_path)
            return new_debugtalk_response
        except DebugtalkException as e:
            new_debugtalk_response['status'] = 409
            new_debugtalk_response['msg'] = handle_message(e)
            return new_debugtalk_response
        except Exception as e:
            new_debugtalk_response['status'] = 500
            new_debugtalk_response['msg'] = handle_message(e)
            return new_debugtalk_response


@api.route('/debugtalk/<id>')
@api.param('id', 'debugtalk identifier')
class DebugtalkResource(Resource):

    def get(self, id):
        debugtalk_controller = DebugtalkController()
        debugtalk_response = copy.deepcopy(response)
        try:
            debugtalk = debugtalk_controller.get_debugtalk(id)
            if not debugtalk:
                debugtalk_response['status'] = 409
                debugtalk_response['msg'] = 'debugtalk {} not found.'.format(id)
                return debugtalk_response

            debugtalk_response['msg'] = 'debugtalk successfully get by id'
            debugtalk_response['data'] = debugtalk.as_json()
            return debugtalk_response
        except DebugtalkException as e:
            debugtalk_response['status'] = 409
            debugtalk_response['msg'] = handle_message(e)
            return response
        except Exception as e:
            debugtalk_response['status'] = 500
            debugtalk_response['msg'] = handle_message(e)
            return debugtalk_response

    @api.expect(debugtalk_model, validate=True)
    def put(self, id):
        debugtalk_controller = DebugtalkController()
        data = request.get_json(force=True)
        edit_debugtalk_response = copy.deepcopy(response)
        project_id = data.get('project_id')
        print('ppppppppppppppppppppppppp')
        print(type(data.get('debugtalktext')))
        hrproject_path = ProjectController().get_project(project_id).as_json().get('hrproject_path')
        if not hrproject_path:
            edit_debugtalk_response['status'] = 200
            edit_debugtalk_response['msg'] = '查不到项目信息'
        debugtalk_path = os.path.join(hrproject_path,'debugtalk.py')

        try:
            debugtalk_controller.update_debugtalk(  
                                        str(id),
                                        debugtalktext=(data.get('debugtalktext')),
                                        )
            edit_debugtalk_response['msg'] = 'debugtalk successfully updated'
            debugtalk_controller.save_debugtalk_to_pyfile(data.get('debugtalktext'),debugtalk_path)
            return edit_debugtalk_response
        except DebugtalkException as e:
            edit_debugtalk_response['status'] = 409
            edit_debugtalk_response['msg'] = handle_message(e)
            return edit_debugtalk_response
        except Exception as e:
            edit_debugtalk_response['status'] = 500
            edit_debugtalk_response['msg'] = handle_message(e)
            return edit_debugtalk_response
    
@api.route('/run')
class RunDebugtalkResource(Resource):

    @api.expect(debugtalk_model, validate=True)
    def post(self):
        debugtalk_controller = DebugtalkController()
        data = request.get_json(force=True)
        run_debugtalk_response = copy.deepcopy(response) 
        print(data)
        project_id = request.args.get('project_id')
        print('=====================-00000000000000000000000000000')
        print(project_id)
        project = ProjectController().get_project(project_id).as_json()
        if not project:
            run_debugtalk_response['status'] = 200
            run_debugtalk_response['msg'] = '查不到项目信息'
        
        debugtalk_path = os.path.join(project['hrproject_path'],'debugtalk.py')
        
        try:
            debugtalk_controller.save_debugtalk_to_pyfile(data.get('debugtalktext'),debugtalk_path)
            output = debugtalk_controller.run(debugtalk_path)
            run_debugtalk_response['data']['output'] = output
            return run_debugtalk_response
        except DebugtalkException as e:
            run_debugtalk_response['data']['output'] = str(e)
            return run_debugtalk_response
        except Exception as e:
            
            run_debugtalk_response['data']['output'] = str(e)
            return run_debugtalk_response


@api.route('/get_debugtalk')
class GetDebugtalkResource(Resource):
    @api.expect(debugtalk_model, validate=False)
    def get(self):
        debugtalk_response = copy.deepcopy(response) 
        project_id = request.args.get('project_id')
        print('=====================-00000000000000000000000000000')
        print(project_id)
        debugtalk = DebugtalkController().get_debugtalk_by_project_id(project_id)
        if not debugtalk:
            debugtalk_response['status'] = 400
            debugtalk_response['msg'] = 'not found'
            return debugtalk_response
        print(debugtalk.as_json())
        debugtalk_response['data'] = debugtalk.as_json()
        return debugtalk_response
        

 