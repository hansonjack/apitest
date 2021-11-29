#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.report.model.report import Report
from infrastructure.repository_base import RepositoryBase


class ReportRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Report)
