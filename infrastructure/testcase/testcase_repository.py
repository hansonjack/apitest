#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.testcase.model.testcase import Testcase,TestcaseDetail
from infrastructure.repository_base import RepositoryBase


class TestcaseRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Testcase)
class TestcaseDetailRepository(RepositoryBase):
    def __init__(self):
        super().__init__(TestcaseDetail)
