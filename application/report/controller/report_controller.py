from infrastructure.report.report_repository import ReportRepository
from domain.report.model.report_factory import ReportFactory


class ReportController:

    def __init__(self):
        self.__report_repo = ReportRepository()
        self.__report_factory = ReportFactory(self.__report_repo)

    def get_report_list(self):
        return self.__report_repo.get_all()

    def get_report_list_from_keyword(self,keyword):
        return self.__report_repo.get_many_by_keyword(keyword)


    def get_report(self, _id):
        return self.__report_repo.get_by_id(_id)

    def create_report(self, name, summarys, testcase_id, project_id,config_name):
        new_report = self.__report_factory.report_create(
            name=name, 
            run_id='', 
            summarys=summarys, 
            testcase_id=testcase_id, 
            project_id=project_id, 
            testcases=None, 
            teststeps=None, 
            testcases_success=None, 
            teststeps_success=None, 
            elapsed_time=None,
            config_name=config_name
        )
        self.__report_repo.save(new_report)
        return new_report

    def delete_report(self,id_list):
        for i in id_list:
            report = self.__report_repo.get_by_id(i)
            self.__report_repo.delete(report)