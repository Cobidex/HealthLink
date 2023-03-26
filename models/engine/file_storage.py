#!/usr/bin/python3
'''
    module to help save objects in files and back facilitated by JSON
'''
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.service import Service
from models.hospital import Hospital
from models.review import Review

class FileStorage():
    __file_path = "file.json"
    __objects = {}
    
    def all(self, cls=None):
        '''returns all stored objects'''
        if cls:
            objects = self.__objects.items()
            return {k: o for k, o in objects if eval(cls).__name__ in k}
        return self.__objects

    def new(self, obj):
        '''sets a new object'''
        s = '{}.{}'. format(obj.__class__.__name__, obj.id)
        self.__objects[s] = obj

    def save(self):
        '''serializes object to json file'''
        objects = {}
        for key, value in self.all().items():
            objects[key] = value.to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(objects, f)

    def reload(self):
        '''deserializes JSON file to objects'''
        try:
            with open(self.__file_path) as f:
                objects = json.load(f)
                for value in objects.values():
                    self.new(eval(value['__class__'])(**value))
        except:
            self.save()
    def delete(self, obj=None):
        '''deletes an object from the objects'''
        if obj:
            key = '{}.{}'. format(obj.__class__.__name__, obj.id)
            del self.__objects[key]
            self.save()

    def close(self):
        '''deserializing the JSON file to objects'''
        self.reload

    def get(self, cls, id):
        '''retrieve one object'''
        key = '{}.{}'. format(cls.__name__, id)
        return self.all().get(key)

    def count(self, cls=None):
        '''count number of objects in storage'''
        return len(self.all(cls))
