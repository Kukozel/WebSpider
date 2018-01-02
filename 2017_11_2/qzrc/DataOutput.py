# coding:utf-8
import pymongo
from qzrc.account import account
ac=account()
# 数据储存器
class DataOutput(object):
    def store_data(self, data):
        if data is None:
            return
        self._output_data_to_mongo(data)

    def _output_data_to_mongo(self, data):
        client = pymongo.MongoClient(ac.con)
        db = client.qzrc
        collection = db.infos
        collection.insert(data)