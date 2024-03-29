#!/usr/bin/env python3
"""10-update_topics.py"""

def update_topics(mongo_collection, name, topics):
    """function that changes all topics of a school document based on the name"""

   db.mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})