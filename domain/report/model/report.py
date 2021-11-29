#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from domain.entity_base import EntityBase
from utils import time2str

class Report(EntityBase):

    def __init__(self, name, run_id, summarys,testcase_id,project_id,
    testcases,teststeps,testcases_success,teststeps_success,elapsed_time,create_time,config_name):
        self.id = None
        self.name = name
        self.run_id = run_id
        self.summarys = summarys
        self.testcase_id = testcase_id
        self.project_id = project_id
        self.testcases = testcases
        self.teststeps = teststeps
        self.testcases_success = testcases_success
        self.teststeps_success = teststeps_success
        self.elapsed_time = elapsed_time
        self.create_time = create_time
        self.config_name = config_name
        # self.__mapper_args__ = {
        # "order_by": self.id.desc()
        # }

    def __repr__(self):
        return "Entity : {}, Name: {}" \
            .format(self.__class__.__name__, self.name)

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'run_id': self.run_id,
            'summarys': self.summarys,
            'testcase_id': self.testcase_id,
            'project_id': self.project_id,
            'testcases': self.testcases,
            'teststeps': self.teststeps,
            'testcases_success': self.testcases_success,
            'teststeps_success': self.teststeps_success,
            'elapsed_time': self.elapsed_time,
            'create_time': time2str(self.create_time),
            'config_name': self.config_name
        }
