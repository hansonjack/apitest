from flask import request
from flask_restx import Resource, Namespace, fields
from application.testcase.controller.testcase_controller import TestcaseController
from infrastructure.testcase.testcase_exceptions import TestcaseException
from infrastructure.handle_exception_messages import handle_message
from application.teststep.controller.teststep_controller import TeststepController
from application.report.controller.report_controller import ReportController
import copy
from infrastructure.response import response
from utils import run_testcases,run_testcase,run_hr_with_command
import time
from application.testcaseConfig.controller.testcaseConfig_controller import ConfigController
import os

api = Namespace('testcase', description='testcase APIs')
testcase_model = api.model('testcase', {
    'name': fields.String(required=True, description='name value', min_length=2),
})


@api.route('/testcases')
class TestcasesResource(Resource):

    def get(self):
        testcase_controller = TestcaseController()
        project_id = request.args.get('project_id')
        testcases_resp = copy.deepcopy(response)
        testcases_resp['data']['rows'] = testcase_controller.get_testcase_list(project_id)
        testcases_resp['data']['count'] = len(testcases_resp['data']['rows'])
        return testcases_resp

    @api.expect(testcase_model, validate=True)
    def post(self):
        testcase_controller = TestcaseController()
        data = request.get_json(force=True)
        # print(data)
        try:
            testcase_controller.create_testcase(name=data['name'],
                                              creator='admin',
                                              project_id=data['project_id'],
                                              env=data['env']['env'],
                                              teststeps=data['pre_apis'] )
            return {'message': 'testcase successfully created'}, 201
        except TestcaseException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500


@api.route('/testcase/<id>')
@api.param('id', 'testcase identifier')
class TestcaseResource(Resource):

    def get(self, id):
        testcase_controller = TestcaseController()
        try:
            testcase = testcase_controller.get_testcase(id)
            if not testcase:
                return {'message': 'testcase {} not found.'.format(id)}, 409

            return testcase
        except TestcaseException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500

    @api.expect(testcase_model, validate=True)
    def put(self, id):
        testcase_controller = TestcaseController()
        data = request.get_json(force=True)

        try:
            testcase_controller.update_testcase(str(id),
                                              name=data['name'],
                                              env=data['env']['env'],
                                              teststeps=data['pre_apis']
                                              )

            return {'message': 'testcase successfully updated.'}, 201
        except TestcaseException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500

@api.route('/run')
class TestcaseRunResource(Resource):
    @api.expect(testcase_model, validate=True)
    def post(self):
        teststep_controller = TeststepController()
        data = request.get_json(force=True)
        hr_project_path,yml_path,config_name = teststep_controller.hr_testcase(data,isteststep=False)
        run_resp = copy.deepcopy(response)
        # config_controller = ConfigController()
        # config_name = config_controller.get_config(data['env']['env']).as_json()['name']
        try:
            summary,run_id = run_testcase(yml_path,hr_project_path)
            print('==========-------------')
            print(summary)
            if not summary:
                run_resp['status'] = 400
                run_resp['msg'] = '用例执行失败'
                return run_resp
            testcases_success = 0
            if summary['success']:
                testcases_success = 1
            teststeps_success = 0
            for i in summary['step_datas']:
                if i['success']:
                    teststeps_success = teststeps_success + 1
            report_controller = ReportController()
            report = report_controller.create_report(
                name=data['name'], 
                run_id=run_id, 
                summarys=[summary], 
                testcase_id=str(data['id']), 
                project_id=data['project_id'], 
                testcases=1, 
                teststeps=data['teststeps_count'], 
                testcases_success=testcases_success, 
                teststeps_success=teststeps_success, 
                elapsed_time=summary['time']['duration'],
                config_name=config_name
            )
            run_resp['data']['summary'] = summary
            run_resp['data']['config_name'] = config_name
            run_resp['data']['run_id'] = run_id
            run_resp['data']['report_id'] = report.as_json()['id']
            run_resp['data']['report_name'] = report.as_json()['name']
            return run_resp
        except TestcaseException as e:
            run_resp['status'] = 409
            run_resp['msg'] = handle_message(e)
            return run_resp
        except Exception as e:
            run_resp['status'] = 500
            run_resp['msg'] = handle_message(e)
            return run_resp
@api.route('/run_with_command')
class TestcaseRunWithCommandResource(Resource):
    @api.expect(testcase_model, validate=True)
    def post(self):
        testcase_controller = TestcaseController()
        data = request.get_json(force=True)
        run_resp = copy.deepcopy(response)
        try:
            hr_project_path,yml_path,config_name,task_info = testcase_controller.hr_testcase_with_run(data)
            report_name = task_info['name']+'.html'
            # project_report = os.path.join(str(data['id'],'reports'))
            # report_path = os.path.join(project_report,report_name)
            run_resp['data']['report_path'] =  str(data['project_id']) +'/reports/'+report_name
            run_resp['data']['config_name'] = config_name
            run_resp['data']['success'] = True
            run_resp['data']['task_info'] = task_info
            return run_resp
        except TestcaseException as e:
            run_resp['status'] = 409
            run_resp['msg'] = handle_message(e)
            run_resp['data']['success'] = False
            return run_resp
        except Exception as e:
            run_resp['status'] = 500
            run_resp['msg'] = handle_message(e)
            run_resp['data']['success'] = False
            return run_resp


@api.route('/runs')
@api.param('id', 'testcase identifier')
class TestcaseRunsResource(Resource):
    @api.expect(testcase_model, validate=False)
    def post(self):
        testcase_controller = TestcaseController()
        data = request.get_json(force=True)
        print(data['ids'])
        config_controller = ConfigController()
        config_name = config_controller.get_config(data['env']).as_json()['name']
        
        run_resp = copy.deepcopy(response)
        try:
            hr_project_path,yml_paths,task_info = testcase_controller.hr_testcases(data['selectedItems'],data['env'],data['project_id'])
            
            return run_resp
        except TestcaseException as e:
            run_resp['status'] = 409
            run_resp['msg'] = handle_message(e)
            return run_resp
        except Exception as e:
            run_resp['status'] = 500
            run_resp['msg'] = handle_message(e)
            return run_resp


@api.route('/testcase_detail_select/<id>')
class TestcaseDetailSelectResource(Resource):

    def get(self,id):
        testcase_controller = TestcaseController()
        details = testcase_controller.get_testcase_detail(id)
        teststep_controller = TeststepController()
        project_id = request.args.get('project_id')
        teststeps = teststep_controller.get_teststep_list(project_id)
        testcase_response = copy.deepcopy(response)
        option = []
        saved_teststep_id = []
        for i in details:
            saved_teststep_id.append(i.as_json()['teststep_id'])
            option.append(
                {
                    'label':i.as_json()['name'] + '  ' +i.as_json()['request']['url'],
                    'value':str(i.as_json()['teststep_id']) + '_' + str(id)
                }
            )
        print(saved_teststep_id)
        for j in teststeps:
            tmp = j.as_json()
            if str(tmp['id']) not in saved_teststep_id:
                option.append(
                    {
                        'label':tmp['name'] + '  ' +tmp['request']['url'],
                        'value':str(tmp['id'])+ '_' + '0'
                    }
                )
        testcase_response['data']['options'] = option
        testcase_response['count'] = len(testcase_response['data']['options'])
        return testcase_response
@api.route('/testcase_teststep_edit_detail/<teststep_id_and_testcase_id>')
class TestcaseTeststepDetailResource(Resource):

    def get(self,teststep_id_and_testcase_id):
        testcase_controller = TestcaseController()
        testcase_response = copy.deepcopy(response)
        try:
            details = testcase_controller.testcase_teststep(teststep_id_and_testcase_id)
            testcase_response['data'] = details.as_json()
            return testcase_response
        except TestcaseException as e:
            testcase_response['status'] = 409
            testcase_response['msg'] = handle_message(e)
            return testcase_response
        except Exception as e:
            testcase_response['status'] = 500
            testcase_response['msg'] = handle_m