#!/usr/bin/python3
'''contains the hospital class'''
from os import getenv
from sqlalchemy.orm import relationship
import models
from models.service import Service
from models.base_model import BaseModel, Base
from sqlalchemy import *


if getenv('HLINK_DB') == 'db':
    hospital_service = Table('hospital_service', Base.metadata,
                             Column('hospital_id', String(60),
                                    ForeignKey('hospitals.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    primary_key=True, nullable=False),
                             Column('service_id', String(60),
                                    ForeignKey('services.id',
                                               onupdate='CASCADE',
                                               ondelete='CASCADE'),
                                    primary_key=True, nullable=False))


class Hospital(BaseModel, Base):
    '''defines the Hospital class'''
    if getenv('HLINK_DB') == 'db':
        __tablename__ = 'hospitals'
        city_id = Column(String(60), ForeignKey('cities.id'),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        address = Column(String(128), nullable=False)
        phone_number = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        website = Column(String(128))
        ratings = Column(Integer)
        working_hours = Column(String(128))
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship('Review', backref='hospital',
                               cascade='all, delete-orphan')
        services = relationship('Service', secondary='hospital_service',
                                back_populates="hospitals",
                                viewonly=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    if getenv('HLINK_DB') != 'db':
        services = []
        @property
        def reviews(self):
            '''
                getter method for hospital/review
                relationship in filestorage
            '''
            rev = models.storage.all(Review).values()
            return [o for o in rev if self.id in o.hospital_ids]

        @property
        def services(self):
            '''getter method for hospital/service'''
            am = models.storage.all(Service).values()
            return [o for o in am if self.id in o.hospital_ids]

        @services.setter
        def services(self, obj):
            '''appends id to services_ids'''
            if isinstance(obj, Service):
                self.service_ids.append(obj.id)
                obj.save()
