#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.teststep.model.teststep import Teststep
from infrastructure.repository_base import RepositoryBase


class TeststepRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Teststep)