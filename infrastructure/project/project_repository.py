#!/usr/bin/env python
# # -*- coding: utf-8 -*-


from domain.project.model.project import Project
from infrastructure.repository_base import RepositoryBase


class ProjectRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Project)
