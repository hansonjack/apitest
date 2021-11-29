#!/usr/bin/env python
# # -*- coding: utf-8 -*-

from operator import and_
from infrastructure.db import DbManager


class RepositoryBase(object):
    def __init__(self, class_name):
        self.__db = DbManager.DB
        self.__session = DbManager.DB.session
        self.__class = class_name

    @property
    def db(self):
        return self.__db

    @property
    def session(self):
        return self.__session

    def save(self, entity, commit=True):
        self.session.add(entity)
        self.session.flush()  ##这样就可以插入数据后能获取到ID
        if commit:
            self.session.commit()
            return entity.id

    def delete(self, entity, commit=True):
        if isinstance(entity,list):
            for i in entity:
                self.session.delete(i)
        else:
            self.session.delete(entity)
        if commit:
            self.session.commit()

    def commit(self):
        self.session.commit()

    def get_all(self):
        return DbManager.DB.session.query(self.__class).all()

    def get_by_id(self, _id):
        
        return DbManager.DB.session.query(self.__class).get(_id)
    def filter_by(self, keyword):
        print('==============================SQL================================')
        # print(DbManager.DB.session.query(self.__class).filter_by(project_id=keyword))
        return DbManager.DB.session.query(self.__class).filter_by(project_id=keyword)

    def get_many_by_keyword(self, keyword):
        '''
        params:
            keyword = {}
        '''
        return DbManager.DB.session.query(self.__class).filter_by(**keyword).all()

    def get_one_by_keyword(self, keyword):
        '''
        params:
            keyword = {}
        '''
        return DbManager.DB.session.query(self.__class).filter_by(**keyword).first()

    def get_by_and(self,keyword1,keyword2):
        return DbManager.DB.session.query(self.__class).filter_by(**keyword1).filter_by(**keyword2).first()