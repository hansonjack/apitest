#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from domain.entity_base import EntityBase


class Student(EntityBase):

    def __init__(self, name, surname, tel, _id=None):
        self.id = super().get_id(_id)
        self.name = name
        self.surname = surname
        self.tel = tel

    def __repr__(self):
        return "Entity : {}, Name: {}, Surname: {}, Tel: {}, Id: {}" \
            .format(self.__class__.__name__, self.name, self.surname, self.tel, self.id)

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'tel': self.tel
        }
