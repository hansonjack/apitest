from types import FrameType
from flask import request
from flask_restx import Resource, Namespace, fields
from application.teststep.controller.teststep_controller import TeststepController
from application.testcase.controller.testcase_controller import TestcaseController
from infrastructure.teststep.teststep_exceptions import TeststepException
from infrastructure.handle_exception_messages import handle_message
from infrastructure.response import response
import copy
from utils import run_testcase,db2web_data
import random
from hr_report.gen_report import gen_html_report
import os

api = Namespace('teststep', description='teststep APIs')
teststep_model = api.model('teststeps', {
    'name': fields.String(required=True, description='接口名称', min_length=2),
    'variables': fields.List(fields.Raw,required=False, description='变量'),
    'request': fields.List(fields.Raw,required=False, description='接口信息'),
    'validate': fields.List(fields.Raw,required=False, description='断言'),
    'extract': fields.List(fields.Raw,required=False, description='提取'),
    'setup_hooks': fields.List(fields.Raw,required=False, description='前置执行'),
    'teardown_hooks': fields.List(fields.Raw,required=False, description='后置执行'),
    'project_id': fields.String(required=True, description='项目ID'),
})


@api.route('/teststeps')
class TeststepsResource(Resource):

    def get(self):
        teststep_controller = TeststepController()
        teststeps_response = copy.deepcopy(response)
        project_id = request.args.get('project_id')
        teststeps_response['data']['rows'] = [teststep.as_json() for teststep in teststep_controller.get_teststep_list(project_id)[::-1]]
        teststeps_response['count'] = len(teststeps_response['data']['rows'])
        return teststeps_response

    @api.expect(teststep_model, validate=True)
    def post(self):
        teststep_controller = TeststepController()
        data = request.get_json(force=True)
        print(data)
        headers = data.get('headers') or []
        headers.append({"key":'content_type','value':data['content_type'],'desc':''})
        request_info = {
            'method': data['method'],
            'url':data['url'],
            'headers':headers,
            'request_data_normal': data.get('normal'),
            'request_data_encryption': data.get('encryption')
        }
        new_teststep_response = copy.deepcopy(response) 
        project_id = request.args.get('project_id')
        try:
            new_teststep = teststep_controller.create_teststep(  
                                        name=data['name'],
                                        variables=data.get('variables'),
                                        request=request_info,
                                        validate=data.get('validate'),
                                        extract=data.get('extract'),
                                        setup_hooks=data.get('setup_hooks'),
                                        teardown_hooks=data.get('teardown_hooks'),
                                        project_id=project_id,
                                              
                                              )
            
            new_teststep_response['msg'] = 'teststep successfully created'
            new_teststep_response['data'] =new_teststep.as_json()
            return new_teststep_response
        except TeststepException as e:
            new_teststep_response['status'] = 409
            new_teststep_response['msg'] = handle_message(e)
            return new_teststep_response
        except Exception as e:
            new_teststep_response['status'] = 500
            new_teststep_response['msg'] = handle_message(e)
            return new_teststep_response


@api.route('/teststep/<id>')
@api.param('id', 'teststep identifier')
class TeststepResource(Resource):

    def get(self, id):
        teststep_controller = TeststepController()
        teststep_response = copy.deepcopy(response)
        print(id)
        try:
            teststep = teststep_controller.get_teststep(id)
            print(teststep)
            if not teststep:
                teststep_response['status'] = 409
                teststep_response['msg'] = 'Student {} not found.'.format(id)
                return teststep_response

            teststep_response['msg'] = 'teststep successfully get by id'
            tmp = db2web_data(teststep.as_json())
            # print(db2web_data(teststep.as_json()))
           
            headers = tmp['headers']
            tmp1 = []
            for i in headers:
                if i['key'] != 'content_type':
                    tmp1.append(i)
            tmp['headers'] = tmp1
            teststep_response['data'] = tmp
            return teststep_response
        except TeststepException as e:
            teststep_response['status'] = 409
            teststep_response['msg'] = handle_message(e)
            return response
        except Exception as e:
            teststep_response['status'] = 500
            teststep_response['msg'] = handle_message(e)
            return teststep_response

    @api.expect(teststep_model, validate=False)
    def put(self, id):
        teststep_controller = TeststepController()
        data = request.get_json(force=True)
        edit_teststep_response = copy.deepcopy(response)
        headers = data.get('headers') or []
        headers.append({"key":'content_type','value':data['content_type'],'desc':''})
        request_info = {
            'method': data['method'],
            'url':data['url'],
            'headers':headers,
            'request_data_normal': data.get('normal'),
            'request_data_encryption': data.get('encryption')
        } 
        try:
            teststep_controller.update_teststep(  
                                        str(id),
                                        name=data['name'],
                                        variables=data.get('variables'),
                                        request=request_info,
                                        validate=data.get('validate'),
                                        extract=data.get('extract'),
                                        setup_hooks=data.get('setup_hooks'),
                                        teardown_hooks=data.get('teardown_hooks'),
                                        )

            edit_teststep_response['msg'] = 'teststep successfully updated'
            return edit_teststep_response
        except TeststepException as e:
            edit_teststep_response['status'] = 409
            edit_teststep_response['msg'] = handle_message(e)
            return edit_teststep_response
        except Exception as e:
            edit_teststep_response['status'] = 500
            edit_teststep_response['msg'] = handle_message(e)
            return edit_teststep_response


@api.route('/teststeps_select')
class TeststepsSelectResource(Resource):

    def get(self):
        teststep_controller = TeststepController()
        teststeps_response = copy.deepcopy(response)
        project_id = request.args.get('project_id')
        option = []
        for i in teststep_controller.get_teststep_list(project_id):
            option.append(
                {
                    'label':i.as_json()['name'] + '  ' +i.as_json()['request']['url'],
                    'value':i.as_json()['id']
                }
            )
        teststeps_response['data']['options'] = option
        teststeps_response['count'] = len(teststeps_response['data']['options'])
        return teststeps_response

@api.route('/get_teststeps_by_ids/<ids>')
@api.param('ids', 'teststep identifier')
class TeststepsByIdsResource(Resource):

    def get(self,ids):
        teststep_controller = TeststepController()
        teststeps_response = copy.deepcopy(response)
        rows = []
        ids_list = ids.split(',')
        for i in teststep_controller.get_teststep_list():
            teststep = i.as_json()
            if teststep['id'] in ids_list:
                rows.append(teststep)
        teststeps_response['data']['rows'] = rows
        teststeps_response['count'] = len(teststeps_response['data']['rows'])
        return teststeps_response

@api.route('/testcase_teststep/<id>')
class TeststepEditResource(Resource):

    def put(self, id):
        teststep_id = int(id.split('_')[0])
        testcase_id = int(id.split('_')[1])
        teststep_controller = TeststepController()
        testcase_controller = TestcaseController()
        data = request.get_json(force=True)
        edit_teststep_response = copy.deepcopy(response)
        try:
            teststep_controller.update_teststep(  
                                        teststep_id,
                                        name=data['name'],
                                        variables=data.get('variables'),
                                        request=data.get('request'),
                                        validate=data.get('validate'),
                                        extract=data.get('extract'),
                                        setup_hooks=data.get('setup_hooks'),
                                        teardown_hooks=data.get('teardown_hooks'),
                                        )
            
            if testcase_id:
                testcase_controller.update_testcase_detail(
                    data['id'],
                    name=data['name'],
                    variables=data['variables'], 
                    validate=data['validate'], 
                    extract=data['extract'], 
                    setup_hooks=data['setup_hooks'], 
                    teardown_hooks=data['teardown_hooks'], 
                    request=data['request']
                )
            
            edit_teststep_response['msg'] = 'teststep and testcasedetail successfully updated'
            return edit_teststep_response
        except TeststepException as e:
            edit_teststep_response['status'] = 409
            edit_teststep_response['msg'] = handle_message(e)
            return edit_teststep_response
        except Exception as e:
            edit_teststep_response['status'] = 500
            edit_teststep_response['msg'] = handle_message(e)
            return edit_teststep_response


@api.route('/run_teststep')
class RunTeststepResource(Resource):

    @api.expect(teststep_model, validate=False)
    def post(self):
        run_teststep_resp = copy.deepcopy(response)
        teststep_controller = TeststepController()
        data = request.get_json(force=True)
        print(data)
        hr_project_path,yml_path,config_name = teststep_controller.hr_testcase(data)
        try:
            summary,case_id = run_testcase(yml_path,hr_project_path)
            if not summary:
                run_teststep_resp['status'] = 400
                run_teststep_resp['msg'] = '用例执行失败'
                return run_teststep_resp
            run_teststep_resp['data']['summary'] = summary
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            # print(type(summary))
            # reports_path = os.path.join(hr_project_path,'reports')
            # report_name = os.path.basename(yml_path)
            # print(report_name)
            # report_path = os.path.join(reports_path,report_name + '.html')
            # gen_html_report(summary=summary,report_dir=reports_path,report_file=report_path)
            # report1 = hr_project_path.replace(os.getcwd(),'').strip()
            # report2 = os.path.join(report1[1:],'reports')
            # run_teststep_resp['data']['report_name'] = report_name + '.html'
            # run_teststep_resp['data']['report_path'] = os.path.join(report2,report_name + '.html')
            # run_teststep_resp['data']['config_name'] = config_name
            return run_teststep_resp
        except TeststepException as e:
            run_teststep_resp['status'] = 409
            run_teststep_resp['msg'] = handle_message(e)
            return run_teststep_resp
        except Exception as e:
            run_teststep_resp['status'] = 500
            run_teststep_resp['msg'] = handle_message(e)
            return run_teststep_resp
@api.route('/run_testcase')
class RunTestcaseResource(Resource):

    @api.expect(teststep_model, validate=False)
    def post(self):
        run_teststep_resp = copy.deepcopy(response)
        teststep_controller = TeststepController()
        data = request.get_json(force=True)
        # print(data)
        hr_project_path,yml_path,config_name = teststep_controller.hr_testcase(data,isteststep=False)
        try:
            summary,case_id = run_testcase(yml_path,hr_project_path)
            if not summary:
                run_teststep_resp['status'] = 400
                run_teststep_resp['msg'] = '用例执行失败'
                return run_teststep_resp
            run_teststep_resp['data']['summary'] = summary
            run_teststep_resp['data']['config_name'] = config_name
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(type(summary))
            reports_path = os.path.join(hr_project_path,'reports')
            report_name = os.path.basename(yml_path)
            print(report_name)
            report_path = os.path.join(reports_path,report_name + '.html')
            gen_html_report(summary=summary,report_dir=reports_path,report_file=report_path)
            report1 = hr_project_path.replace(os.getcwd(),'').strip()
            report2 = os.path.join(report1[1:],'reports')
            run_teststep_resp['data']['report_name'] = report_name + '.html'
            run_teststep_resp['data']['report_path'] = os.path.join(report2,report_name + '.html')
            return run_teststep_resp
        except TeststepException as e:
            run_teststep_resp['status'] = 409
            run_teststep_resp['msg'] = handle_message(e)
            return run_teststep_resp
        except Exception as e:
            run_teststep_resp['status'] = 500
            run_teststep_resp['msg'] = handle_message(e)
            return run_teststep_resp
        

@api.route('/copy')
class TeststepCopyResource(Resource):
    @api.expect(teststep_model, validate=False)
    def post(self):
        teststep_controller = TeststepController()
        data = request.get_json(force=True)
        print(data)
        new_teststep_response = copy.deepcopy(response) 
        project_id = request.args.get('project_id')
        try:
            new_teststep = teststep_controller.create_teststep(  
                                        name=data['name'] + ' 复制',
                                        variables=data.get('variables'),
                                        request=data.get('request'),
                                        validate=data.get('validate'),
                                        extract=data.get('extract'),
                                        setup_hooks=data.get('setup_hooks'),
                                        teardown_hooks=data.get('teardown_hooks'),
                                        project_id=project_id,
                                              
                                              )
            
            new_teststep_response['msg'] = 'teststep successfully created'
            new_teststep_response['data'] =new_teststep.as_json()
            return new_teststep_response
        except TeststepException as e:
            new_teststep_response['status'] = 409
            new_teststep_response['msg'] = handle_message(e)
            return new_teststep_response
        except Exception as e:
            new_teststep_response['status'] = 500
            new_teststep_response['msg'] = handle_message(e)
            return new_teststep_response


   