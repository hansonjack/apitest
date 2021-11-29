#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.api.model.api import Api
from infrastructure.repository_base import RepositoryBase


class ApiRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Api)