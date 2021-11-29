from flask import request
from flask_restx import Resource, Namespace, fields
from application.testcaseConfig.controller.testcaseConfig_controller import ConfigController
from infrastructure.testcaseConfig.testcaseConfig_exceptions import TestcaseConfigException
from infrastructure.handle_exception_messages import handle_message
from infrastructure.response import response
import copy
import time
day = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

api = Namespace('config', description='config APIs')
config_model = api.model('configs', {
    'name': fields.String(required=True, description='配置名称', min_length=2),
    'verify': fields.String(defaut='False',required=False, description='verify'),
    'base_url': fields.String(required=False, description='根地址'),
    'variables': fields.List(fields.Raw,required=False, description='variables'),
    
    'weight': fields.Integer(defaut=1,required=False, description='重复执行次数'),
    'status': fields.Integer(defaut=1,required=False, description='状态'),
    'createtime': fields.String(required=False, description='创建时间'),
    'updatetime': fields.String(required=False, description='更新时间'),
    'project_id': fields.String(required=True, description='项目ID'),
})


@api.route('/configs')
class ConfigsResource(Resource):

    def get(self):
        config_controller = ConfigController()
        configs_response = copy.deepcopy(response)
        project_id = request.args.get('project_id')
        configs_response['data']['rows'] = [config.as_json() for config in config_controller.get_config_list(project_id)]
        configs_response['count'] = len(configs_response['data']['rows'])
        return configs_response

    @api.expect(config_model, validate=True)
    def post(self):
        config_controller = ConfigController()
        data = request.get_json(force=True)
        print(data) 
        project_id = request.args.get('project_id')
        new_config_response = copy.deepcopy(response)
        try:
            new_config = config_controller.create_config(  
                                        name=data['name'],
                                        verify=data.get('verify') or 'False',
                                        base_url=data.get('base_url'),
                                        variables=data.get('variables'),
                                        parameters=data.get('parameters') or [],
                                        export=data.get('export'),
                                        path=data.get('path'),
                                        weight=data.get('weight') or 1,
                                        status=data.get('status') or 1,
                                        createtime=day,
                                        updatetime=day,
                                        project_id=project_id      
                                              )
            
            new_config_response['msg'] = 'config successfully created'
            new_config_response['data'] =new_config.as_json()
            return new_config_response
        except TestcaseConfigException as e:
            print('=======================================================')
            print(e)
            new_config_response['status'] = 409
            new_config_response['msg'] = handle_message(e)
            return new_config_response
        except Exception as e:
            new_config_response['status'] = 500
            new_config_response['msg'] = handle_message(e)
            print('=======================================================')
            print(e)
            return new_config_response


@api.route('/config/<id>')
@api.param('id', 'config identifier')
class ConfigResource(Resource):

    def get(self, id):
        config_controller = ConfigController()
        config_response = copy.deepcopy(response)
        try:
            config = config_controller.get_config(id)
            if not config:
                config_response['status'] = 409
                config_response['msg'] = 'Student {} not found.'.format(id)
                return config_response

            config_response['msg'] = 'config successfully get by id'
            config_response['data'] = config.as_json()
            return config_response
        except TestcaseConfigException as e:
            config_response['status'] = 409
            config_response['msg'] = handle_message(e)
            return response
        except Exception as e:
            config_response['status'] = 500
            config_response['msg'] = handle_message(e)
            return config_response

    @api.expect(config_model, validate=False)
    def put(self, id):
        config_controller = ConfigController()
        data = request.get_json(force=True)
        print(data)
        edit_config_response = copy.deepcopy(response)
        try:
            config_controller.update_config(  
                                        str(id),
                                        name=data['name'],
                                        base_url=data.get('base_url'),
                                        variables=data.get('variables') or [],
                                        parameters=data.get('parameters') or [],
                                        export=data.get('export') or [],
                                        updatetime=day,
                                        )

            edit_config_response['msg'] = 'config successfully updated'
            return edit_config_response
        except TestcaseConfigException as e:
            edit_config_response['status'] = 409
            edit_config_response['msg'] = handle_message(e)
            return edit_config_response
        except Exception as e:
            edit_config_response['status'] = 500
            edit_config_response['msg'] = handle_message(e)
            return edit_config_response
    @api.expect(config_model, validate=True)
    def delete(self, id):
        config_controller = ConfigController()
        edit_config_response = copy.deepcopy(response)
        try:
            config_controller.update_config(  
                                        str(id),
                                        status = 0,
                                        updatetime=day,
                                        )

            edit_config_response['msg'] = 'config successfully deleted'
            return edit_config_response
        except TestcaseConfigException as e:
            edit_config_response['status'] = 409
            edit_config_response['msg'] = handle_message(e)
            return edit_config_response
        except Exception as e:
            edit_config_response['status'] = 500
            edit_config_response['msg'] = handle_message(e)
            return edit_config_response


@api.route('/configs_select')
class ConfigsSelectResource(Resource):

    def get(self):
        config_controller = ConfigController()
        configs_response = copy.deepcopy(response)
        project_id = request.args.get('project_id')
        option = []
        config_list = config_controller.get_config_list(project_id)
        if not config_list:
            configs_response['data']['options'] = []
            return configs_response
        for i in config_list:
            option.append(
                {
                    'label':i.as_json()['name'],
                    'value':i.as_json()['id']
                }
            )
        if not option:
            configs_response['data']['options'] = []
            return configs_response
        configs_response['data']['options'] = option
        configs_response['data']['value'] = option[0]['value']
        configs_response['count'] = len(configs_response['data']['options'])
        return configs_response

    