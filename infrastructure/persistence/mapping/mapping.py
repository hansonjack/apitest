#!/usr/bin/env python
# # -*- coding: utf-8 -*-

from sqlalchemy import Table, MetaData, Column, String,JSON,Integer,Text,ForeignKey,DateTime
from sqlalchemy.orm import mapper
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Float
from domain.student.model.student import Student
from domain.teststep.model.teststep import Teststep
from domain.testcaseConfig.model.testcaseConfig import TestConfig
from domain.debugtalk.model.debugtalk import Debugtalk
from domain.project.model.project import Project
from domain.testcase.model.testcase import Testcase,TestcaseDetail
from domain.report.model.report import Report
import datetime


custom_metadata = MetaData()

student_mapping = Table('student', custom_metadata,
                        Column('id', String(36), primary_key=True),
                        Column('name', String(50)),
                        Column('surname', String(50)),
                        Column('tel', String(50)),
                        )

mapper(Student, student_mapping)

teststep_mapping = Table('teststep', custom_metadata,
                        Column('id', Integer,autoincrement=True,nullable=False, primary_key=True),
                        Column('name',String(512), nullable=True),
                        Column('variables',JSON, nullable=False),
                        Column('request',JSON, nullable=False),
                        Column('validate',JSON, nullable=False),
                        Column('extract',JSON, nullable=False),
                        Column('setup_hooks',JSON, nullable=False),
                        Column('teardown_hooks',JSON, nullable=False),
                        Column('project_id',String(36)),
                        )

mapper(Teststep, teststep_mapping)

config_mapping = Table('config', custom_metadata,
                        Column('id', Integer,autoincrement=True,nullable=False, primary_key=True),
                        Column('name',String(512), nullable=False),
                        Column('verify',String(10), default='False'),
                        Column('base_url',String(512), nullable=True),
                        Column('variables',JSON, nullable=True),
                        Column('parameters',JSON, nullable=True),
                        Column('export',JSON, nullable=True),
                        Column('path',String(256), nullable=True),
                        Column('weight',Integer, default=1),
                        Column('status',Integer, default=1),
                        Column('createtime',String(36), default=datetime.datetime.now),
                        Column('updatetime',String(36), default=datetime.datetime.now,onupdate=datetime.datetime.now),
                        Column('project_id',String(36)),
                        )

mapper(TestConfig, config_mapping)

debugtalk_mapping = Table('debugtalk', custom_metadata,
                        Column('id', Integer,autoincrement=True,nullable=False, primary_key=True),
                        Column('debugtalktext',Text),
                        Column('project_id',String(36), nullable=True),
                        )

mapper(Debugtalk, debugtalk_mapping)

project_mapping = Table('project', custom_metadata,
                        Column('id', Integer,autoincrement=True,nullable=False, primary_key=True),
                        Column('name',String(512), nullable=False),
                        Column('desc',String(1024), nullable=True),
                        Column('hrproject_path',String(1024), nullable=True),
                        )

mapper(Project, project_mapping)

testcase_mapping = Table('testcase', custom_metadata,
                        Column('id', Integer,autoincrement=True,nullable=False, primary_key=True),
                        Column('name',String(512), nullable=False),
                        Column('creator',String(36), nullable=True),
                        Column('project_id',String(36), nullable=True),
                        Column('create_time',DateTime),
                        Column('update_time',DateTime),
                        Column('env',String(36), nullable=True),
                        )

mapper(Testcase, testcase_mapping)
testcase_detail_mapping = Table('testcase_detail', custom_metadata,
                        Column('id', Integer,autoincrement=True,nullable=False, primary_key=True),
                        Column('testcase_id',String(36), nullable=False),
                        Column('teststep_id',String(36), nullable=False),
                        Column('name',String(36), nullable=True),
                        Column('variables',JSON, nullable=True),
                        Column('validate',JSON, nullable=True),
                        Column('extract',JSON, nullable=True),
                        Column('setup_hooks',JSON, nullable=True),
                        Column('teardown_hooks',JSON, nullable=True),
                        Column('request',JSON, nullable=True),
                        )

mapper(TestcaseDetail, testcase_detail_mapping)

report_mapping = Table('report', custom_metadata,
                        Column('id', Integer,autoincrement=True,nullable=False, primary_key=True),
                        Column('name',String(128), nullable=False),
                        Column('run_id',String(36), nullable=False),
                        Column('summarys',JSON, nullable=True),
                        Column('testcase_id',String(512), nullable=False),
                        Column('project_id',String(36), nullable=False),
                        Column('testcases',Integer, nullable=True,default=0),
                        Column('teststeps',Integer, nullable=True,default=0),
                        Column('testcases_success',Integer, nullable=True,default=0),
                        Column('teststeps_success',Integer, nullable=True,default=0),
                        Column('elapsed_time',Float, nullable=True,default=0),
                        Column('create_time',DateTime),
                        Column('config_name',String(128),nullable=True),
                        )

mapper(Report, report_mapping)
