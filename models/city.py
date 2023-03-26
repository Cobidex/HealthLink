#!/usr/bin/python3
'''module contains the city class'''

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    '''defines the city class'''
    if getenv('HLINK_DB') == 'db':
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'),
                          nullable=False)
        hospitals = relationship('Hospital', backref='cities',
                                 cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
