import ast
import random
import time
from datetime import datetime, timedelta

import pymongo
import os
import certifi
from typing import Dict

from flask import session


class Database:
    URI = os.environ.get('URI')
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI, tlsCAFile=certifi.where())
        Database.DATABASE = client["WordMaster"]
        session["email"] = None


        ### Only need to create once ###

        # Database.create_dicts()
        # Database.random_words()

        ###                          ###

    @staticmethod
    def random_words():

        for i in range(3, 10):
            now = datetime.now()
            today = now.date()
            words_dict = Database.find_one("dicts", {"name": str(i)})
            words_list = list(words_dict["dict"].items())
            words = {}
            for j in range(1000):
                random_word = random.choice(words_list)
                random_word = random_word[0]
                random_word.upper()
                today_s = today.strftime("%Y%m%d")
                words[today_s] = random_word.upper()
                today += timedelta(days=1)

            words_dict["random"] = words
            Database.update("dicts", {"name": str(i)}, words_dict)

    @staticmethod
    def create_dicts():

        ### need to run once a time periord so dont have to remove it all the time
        for i in range(10):
            Database.remove("dicts", {})

        for i in range(3, 10):
            # reading the data from the file
            temp = f"Data/Dicts/{str(i)}letters.txt"
            with open(temp) as f:
                data = f.read()
            dict_ = ast.literal_eval(data)
            Database.insert("dicts", {"name": str(i), "dict": dict_, "random": {}})

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_one_return_one(collection: str, query: Dict, data: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query, data)

    @staticmethod
    def find_exact(collection: str, query1: Dict, query2: Dict) -> Dict:
        return Database.DATABASE[collection].find(query1, query2)

    def all(name: str, query: dict):
        # does this actualy retrn all different values?
        elements_from_db = Database.find_exact(name, {}, query)
        return [elem for elem in elements_from_db]

    # upsert = True updates the db id no unique id is found
    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        # had to use replace_one as update did not work
        Database.DATABASE[collection].replace_one(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict):
        Database.DATABASE[collection].delete_many(query)

    @staticmethod
    def real_update(collection: str, query: Dict, data: Dict):
        Database.DATABASE[collection].update_one(query, data)
