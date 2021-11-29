#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from domain.entity_base import EntityBase


class TestConfig(EntityBase):

    def __init__(self, name, verify, base_url,variables,parameters,export, path,weight,status,createtime,updatetime,project_id):
        self.id = None
        self.name = name
        self.verify = verify
        self.base_url = base_url
        self.variables = variables
        self.parameters = parameters
        self.export = export
        self.path = path
        self.weight = weight
        self.status = status
        self.createtime = createtime
        self.updatetime = updatetime
        self.project_id = project_id


    def __repr__(self):
        return "Entity : {}, Name: {}, verify: {}, base_url: {},variables: {}, parameters: {},export: {},path: {},weight:{},status:{},createtime:{},updatetime:{},project_id:{},Id: {}" \
            .format(self.__class__.__name__, self.name, self.verify, self.base_url, self.variables, self.parameters,self.export,self.path,self.weight,self.status,self.createtime,self.updatetime,self.project_id,self.id)

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'verify': self.verify,
            'base_url': self.base_url,
            'variables': self.variables,
            'parameters': self.parameters,
            'export': self.export,
            'path': self.path,
            'weight': self.weight,
            'status': self.status,
            'createtime': self.createtime,
            'updatetime': self.updatetime,
            'project_id': self.project_id
        }