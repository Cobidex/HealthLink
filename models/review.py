#!/usr/bin/python3
'''contains the reviews class'''
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    '''defines the Reviews class'''
    if getenv('HLINK_DB') == 'db':
        __tablename__ = 'reviews'
        hospital_id = Column(String(60), ForeignKey('hospitals.id'),
                             nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
        text = Column(String(1024), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
