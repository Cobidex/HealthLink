#!/usr/bin/python
'''this module contains the db_storage class'''
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.review import Review
from models.hospital import Hospital
from models.service import Service


class DBStorage():
    '''defines the DBStorage class'''
    __engine = None
    __session = None
               

    def __init__(self):
        c = 'mysql+mysqldb://{}:{}@{}/{}'. format(getenv('HLINK_MYSQL_USER'),
                                                  getenv('HLINK_MYSQL_PWD'),
                                                  getenv('HLINK_MYSQL_HOST'),
                                                  getenv('HLINK_MYSQL_DB'))
        self.__engine = create_engine(c, pool_pre_ping=True)

    def all(self, cls=None):
        '''gets objects of specific class'''
        objects = {}
        if cls:
            query = self.__session.query(eval(cls.__name__)).all()
            for row in query:
                key = "{}.{}". format(row.__class__.__name__, row.id)
                objects[key] = row
        else:
            for c in [State, City, User, Hospital, Service, Review]:
                query = self.__session.query(c).all()
                for row in query:
                    key = "{}.{}". format(row.__class__.__name__, o.id)
                    objects[key] = row
        return objects

    def new(self, obj):
        '''adds the object to current database session'''
        self.__session.add(obj)

    def save(self):
        '''commit changes to current db session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current session'''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''create all classes'''
        Base.metadata.create_all(self.__engine)
        session_f = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_f)
        self.__session = Session()

    def close(self):
        '''closes the current session'''
        self.__session.close()

    def get(self,cls, id):
        '''retrieves one object'''
        key = '{}.{}'. format(cls.__name__, id)
        return self.all().get(key)

    def count(self, cls=None):
        '''count numbe rof objects'''
        return len(self.all(cls))

