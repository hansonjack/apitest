#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.testcaseConfig.model.testcaseConfig import TestConfig
from infrastructure.repository_base import RepositoryBase


class ConfigRepository(RepositoryBase):
    def __init__(self):
        super().__init__(TestConfig)