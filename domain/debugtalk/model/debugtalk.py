#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from domain.entity_base import EntityBase


class Debugtalk(EntityBase):

    def __init__(self, debugtalktext, project_id):
        self.id = None
        self.debugtalktext = debugtalktext
        self.project_id = project_id

    def __repr__(self):
        return "Entity : {}, debugtalktext: {}, project_id: {},Id: {}" \
            .format(self.__class__.__name__,  self.debugtalktext, self.project_id, self.id)

    def as_json(self):
        return {
            'id': self.id,
            'debugtalktext': self.debugtalktext,
            'project_id': self.project_id

        }