from flask import Flask,make_response,request
from flask_restx  import Api as fAPI
from config import Config
from application.teststep.resources.teststep_resource import api as teststep_api
from application.testcaseConfig.resources.testcaseConfig_resource import api as config_api
from application.debugtalk.resources.debugtalk_resource import api as debugtalk_api
from application.project.resources.project_resource import api as project_api
from application.testcase.resources.testcase_resource import api as testcase_api
from application.report.resources.report_resource import api as report_api
from infrastructure.db import DbManager
from flask_migrate import Migrate
from flask_cors import CORS
import os
import codecs

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)

db = DbManager.start_db(app)
migrate = Migrate(app, db)


myapi = fAPI(app, title='接口自动化测试平台',
          version='1.0',
          description='Student Restful Services')

# myapi.add_namespace(student_api, path='/api/v1')
myapi.add_namespace(teststep_api, path='/teststep/v1')
myapi.add_namespace(config_api, path='/config/v1')
myapi.add_namespace(debugtalk_api, path='/debugtalk/v1')
myapi.add_namespace(project_api, path='/project/v1')
myapi.add_namespace(testcase_api, path='/testcase/v1')
myapi.add_namespace(report_api, path='/report/v1')


@app.before_first_request
def create_db():
    db.create_all()


@app.route('/<name>')
def get_html(name):
    report_path = request.args.get('report_path')
    name = name + '.html'
    report_path1 = os.path.join(report_path,name)
    print('********************$$$$$$$$$$$$$$$$$$$')
    print(name)
    try:
        resp = make_response(open(report_path,encoding='utf-8').read())
        resp.headers["Content-type"]="text/html;charset=UTF-8"
        return resp
    except:
        pass

@app.route('/log')
def get_hr_logs():
    log_path = request.args.get('log_path')
    log_path1 = os.path.join(os.getcwd(),log_path)
    try:
        resp = make_response(codecs.open(log_path1).read())
        resp.headers["Content-type"]="text/html;charset=UTF-8"
        print('dsaaaaaaaaaaaaaaaaaaaaaaaaaaaaa--------------------------')
        return resp
    except:
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)