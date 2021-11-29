#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.student.model.student import Student
from infrastructure.repository_base import RepositoryBase


class StudentRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Student)
