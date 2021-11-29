#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from domain.entity_base import EntityBase


class Project(EntityBase):

    def __init__(self, name, desc,hrproject_path):
        self.id = None
        self.name = name
        self.desc = desc
        self.hrproject_path=hrproject_path

    def __repr__(self):
        return "Entity : {}, Name: {}, desc: {}, Id: {}" \
            .format(self.__class__.__name__, self.name, self.desc,self.id)

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'hrproject_path': self.hrproject_path
        }
