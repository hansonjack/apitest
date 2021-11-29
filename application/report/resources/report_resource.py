from flask import request
from flask_restx import Resource, Namespace, fields
from sqlalchemy.sql.expression import delete
from application.report.controller.report_controller import ReportController
from infrastructure.exception_base import ModelException
from infrastructure.handle_exception_messages import handle_message
from infrastructure.response import response
import copy
api = Namespace('report', description='report APIs')
report_model = api.model('reports', {
    'name': fields.String(required=True, description='name value', min_length=2),
})


@api.route('/reports')
class ReportsResource(Resource):

    def get(self):
        report_resp = copy.deepcopy(response)
        project_id = request.args.get('project_id')
        testcase_id = request.args.get('testcase_id')
        report_controller = ReportController()
        print(project_id,testcase_id)
        if testcase_id:
            print('======================------------')
            testcase_reports = report_controller.get_report_list_from_keyword({'testcase_id':testcase_id})
            report_resp['data']['rows'] = [report.as_json() for report in testcase_reports[::-1]]
            report_resp['data']['count'] = len(report_resp['data']['rows'])
            return report_resp
        else:
            if project_id:
                project_reports = report_controller.get_report_list_from_keyword({'project_id':project_id})
                report_resp['data']['rows'] = [report.as_json() for report in project_reports[::-1]]
                report_resp['data']['count'] = len(report_resp['data']['rows'])
                return report_resp
            else:
                report_resp['data']['rows'] = [report.as_json() for report in report_controller.get_report_list()[::-1]]
                report_resp['data']['count'] = len(report_resp['data']['rows'])
                return report_resp
    def post(self):
        report_controller = ReportController()
        data = request.get_json(force=True)
        report_resp = copy.deepcopy(response)
        try:
            report_controller.create_report(
                name=data['name'], 
                summarys=data['summarys'], 
                testcase_id=data['testcase_id'], 
                project_id=data['project_id'], 
                config_name=data['config_name'])
            return report_resp
        except ModelException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500

    

@api.route('/report/<id>')
@api.param('id', 'report identifier')
class ReportResource(Resource):

    def get(self, id):
        report_resp = copy.deepcopy(response)
        report_controller = ReportController()
        try:
            report = report_controller.get_report(id)
            if not report:
                return {'message': 'report {} not found.'.format(id)}, 409
            report_resp['data'] = report.as_json()
            return report_resp
        except ModelException as e:
            return {'message': handle_message(e)}, 409
        except Exception as e:
            return {'message': handle_message(e)}, 500
    def delete(self,id):
        report_resp = copy.deepcopy(response)
        report_controller = ReportController()
        try:
            report_controller.delete_report([id])
            return report_resp
        except ModelException as e:
            return {'message': handle_message(e)}, 409
        