#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.debugtalk.model.debugtalk import Debugtalk
from infrastructure.repository_base import RepositoryBase


class DebugtalkRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Debugtalk)