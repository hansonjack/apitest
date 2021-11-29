from domain.report.model.report import Report
from infrastructure.exception_base import ModelNotFoundException
import time

daytime = time.localtime()

class ReportFactory:
    def __init__(self,
                 report_repo):
        self.__report_repo = report_repo

    def report_create(self, name, run_id, summarys, testcase_id, project_id, testcases, teststeps, testcases_success, teststeps_success, elapsed_time,config_name):
        report = Report(
            name=name, 
            run_id=run_id, 
            summarys=summarys, 
            testcase_id=testcase_id, 
            project_id=project_id, 
            testcases=testcases, 
            teststeps=teststeps, 
            testcases_success=testcases_success, 
            teststeps_success=teststeps_success, 
            elapsed_time=elapsed_time, 
            create_time=daytime,
            config_name=config_name,
            )

        return report

