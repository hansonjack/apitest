from flask import request
from flask_restx import Resource, Namespace, fields
from application.project.controller.project_controller import ProjectController
from application.debugtalk.controller.debugtalk_controller import DebugtalkController
from infrastructure.project.project_exceptions import ProjectException
from infrastructure.handle_exception_messages import handle_message
import copy
from infrastructure.response import response
from utils import create_httprunner_projiect
import os

api = Namespace('project', description='project APIs')
project_model = api.model('projects', {
    'name': fields.String(required=True, description='name value', min_length=2),
    'desc': fields.String(required=False, description='desc value'),
})


@api.route('/projects')
class projectsResource(Resource):

    def get(self):
        project_controller = ProjectController()
        projects_response = copy.deepcopy(response)
        projects_response['data']['rows'] = [project.as_json() for project in project_controller.get_project_list()]
        projects_response['count'] = len(projects_response['data']['rows'])
        return projects_response

    @api.expect(project_model, validate=True)
    def post(self):
        project_controller = ProjectController()
        data = request.get_json(force=True)
        new_project_response = copy.deepcopy(response) 
        try:
            new_project = project_controller.create_project(  
                                        name=data.get('name'),
                                        desc=data.get('desc'),                        
                                              )
            hr_project_path,hr_testcase_path = create_httprunner_projiect(str(new_project.as_json()['id']))
            project_controller.update_project(
                new_project.as_json()['id'],
                name=new_project.as_json()['name'],
                desc=new_project.as_json()['desc'],
                hrproject_path=hr_project_path
            )
            # ##在static目录下创建report
            # project_controller.create_reports_dir(str(new_project.as_json()['id']))
            hr_debugtalk = os.path.join(hr_project_path,'debugtalk.py')
            with open(hr_debugtalk,'r',encoding='utf-8') as f:
                debugtalk_controller = DebugtalkController()
                debugtalk_controller.create_debugtalk(f.read(),new_project.as_json()['id'])
            new_project_response['msg'] = 'project successfully created'
            new_project_response['data'] =new_project.as_json()
            new_project_response['data']['hr_project_path'] = hr_project_path
            new_project_response['data']['hr_testcase_path'] = hr_testcase_path
            return new_project_response
        except ProjectException as e:
            new_project_response['status'] = 409
            new_project_response['msg'] = handle_message(e)
            return new_project_response
        except Exception as e:
            new_project_response['status'] = 500
            new_project_response['msg'] = handle_message(e)
            return new_project_response


@api.route('/project/<id>')
@api.param('id', 'project identifier')
class projectResource(Resource):

    def get(self, id):
        project_controller = ProjectController()
        project_response = copy.deepcopy(response)
        try:
            project = project_controller.get_project(id)
            if not project:
                project_response['status'] = 409
                project_response['msg'] = 'project {} not found.'.format(id)
                return project_response

            project_response['msg'] = 'project successfully get by id'
            project_response['data'] = project.as_json()
            return project_response
        except ProjectException as e:
            project_response['status'] = 409
            project_response['msg'] = handle_message(e)
            return response
        except Exception as e:
            project_response['status'] = 500
            project_response['msg'] = handle_message(e)
            return project_response

    @api.expect(project_model, validate=True)
    def put(self, id):
        project_controller = ProjectController()
        data = request.get_json(force=True)
        edit_project_response = copy.deepcopy(response)
        try:
            project_controller.update_project(  
                                        str(id),
                                        name=data.get('name'),
                                        desc=data.get('desc'),
                                        )

            edit_project_response['msg'] = 'project successfully updated'
            return edit_project_response
        except ProjectException as e:
            edit_project_response['status'] = 409
            edit_project_response['msg'] = handle_message(e)
            return edit_project_response
        except Exception as e:
            edit_project_response['status'] = 500
            edit_project_response['msg'] = handle_message(e)
            return edit_project_response


