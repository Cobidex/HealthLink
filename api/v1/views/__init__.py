#!/usr/bin/python3
'''initializing package'''
from flask import Blueprint
app_views = Blueprint('app_views', __name__)
State_view = Blueprint('State_view', __name__)
City_view = Blueprint('City_view', __name__)
Service_view = Blueprint('Service_view', __name__)
User_view = Blueprint('User_view', __name__)
Hospital_view = Blueprint('Hospital_view', __name__)
Review_view = Blueprint('Review_view', __name__)
Hospital_Service_view = Blueprint('Hospital_Service_view', __name__)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.services import *
from api.v1.views.users import *
from api.v1.views.hospitals import *
from api.v1.views.reviews import *
from api.v1.views.hospitals_services import *
