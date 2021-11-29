#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from domain.entity_base import EntityBase


class Teststep(EntityBase):

    def __init__(self, name, variables, request,validate,extract,setup_hooks,teardown_hooks,project_id):
        self.id = None
        self.name = name
        self.variables = variables
        self.request = request
        self.validate = validate
        self.extract = extract
        self.setup_hooks = setup_hooks
        self.teardown_hooks = teardown_hooks
        self.project_id = project_id

    def __repr__(self):
        return "Entity : {}, Name: {}, variables: {}, request: {},validate: {}, extract: {},setup_hooks: {},teardown_hooks: {},project_id:{},Id: {}" \
            .format(self.__class__.__name__, self.name, self.variables, self.request, self.validate, self.extract,self.setup_hooks,self.teardown_hooks,self.project_id,self.id)

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'variables': self.variables,
            'request': self.request,
            'validate': self.validate,
            'extract': self.extract,
            'setup_hooks': self.setup_hooks,
            'teardown_hooks': self.teardown_hooks,
            'project_id': self.project_id
        }