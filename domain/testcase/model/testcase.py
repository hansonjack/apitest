#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from domain.entity_base import EntityBase
from utils import time2str

class Testcase(EntityBase):

    def __init__(self, name, creator, project_id, create_time,update_time,env):
        self.id = None
        self.name = name
        self.creator = creator
        self.project_id = project_id
        self.create_time = create_time
        self.update_time = update_time
        self.env = env

    def __repr__(self):
        return "Entity : {}, Name: {},  Id: {}" \
            .format(self.__class__.__name__, self.name, self.id)

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'creator': self.creator,
            'project_id': self.project_id,
            'create_time': time2str(self.create_time),
            'update_time': time2str(self.update_time),
            'env': self.env
        }

class TestcaseDetail(EntityBase):

    def __init__(self, testcase_id, teststep_id,name, variables,validate,extract,setup_hooks,teardown_hooks,request):
        self.id = None
        self.testcase_id = testcase_id
        self.teststep_id = teststep_id
        self.name = name
        self.variables = variables
        self.validate = validate
        self.extract = extract
        self.setup_hooks = setup_hooks
        self.teardown_hooks = teardown_hooks
        self.request = request

    def __repr__(self):
        return "Entity : {}, Name: {},  Id: {}" \
            .format(self.__class__.__name__, self.name, self.id)

    def as_json(self):
        return {
            'id': self.id,
            'testcase_id': self.testcase_id,
            'teststep_id': self.teststep_id,
            'name': self.name,
            'variables': self.variables,
            'validate': self.validate,
            'extract': self.extract,
            'setup_hooks': self.setup_hooks,
            'teardown_hooks': self.teardown_hooks,
            'request': self.request
        }
