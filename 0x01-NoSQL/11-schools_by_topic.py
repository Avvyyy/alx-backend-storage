#!/usr/bin/env python3
"""11-schools_by_topic.py"""

def schools_by_topic(mongo_collection, topic):
    """function that returns the list of school having a specific topic"""

    topic_list = []

    result = mongo_collection.find_all({'topic': topic})

    for document in result:
        topic_list.append(document)
