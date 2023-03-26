#!/usr/bin/python3
'''contains the filestorage test classes'''

import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class test_FileStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage = FileStorage()
        cls.ob = BaseModel()
        cls.ob.save()

    @classmethod
    def tearDownClass(cls):
        cls.ob.delete()
        cls.storage.reload()

    def test_all_type(self):
        self.assertTrue(isinstance(self.storage.all(), dict))


    def test_all_vals(self):
        m_dic = self.storage.all()
        key = '{}.{}'. format(self.ob.__class__.__name__, self.ob.id)
        self.assertTrue(isinstance(m_dic[key], BaseModel))


    def test_all_keys(self):
        m_dic = self.storage.all()
        self.assertIn('BaseModel.'+ self.ob.id, m_dic.keys())


    def test_get_obs(self):
        obj = self.storage.get(BaseModel, self.ob.id)
        self.assertTrue(isinstance(obj, BaseModel))


    def test_count(self):
        num = self.storage.count(BaseModel)
        ob = BaseModel()
        ob.save()
        num2 = self.storage.count(BaseModel)
        self.assertEqual(1, num2 - num)
