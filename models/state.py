#!/usr/bin/python3
'''contain the state class'''
from os import getenv
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    if getenv('HLINK_DB') == 'db':
        '''defines the state class'''
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='states',
                              cascade='all, delete-orphan')

        def __init__(self, *args, **kwargs):
            '''initializes state'''
            super().__init__(*args, **kwargs)

        if getenv('HLINK_DB') != 'db':
            @property
            def cities(self):
                '''gets cities linked to state onject'''
                o_l = models.storage.all(City).values()
                return [o for o in o_l if self.id == o.state_id]
