#!/usr/bin/env python3
'''Module for Task 11.
'''


def schools_by_topic(mongo_collection, topic):
    '''Retrieves a list of schools that contain a specific topic.

    Args:
        mongo_collection: The MongoDB collection object from which to query documents.
        topic (str): The topic to filter the schools by.

    Returns:
        A list of documents representing schools that include the specified topic.
    '''
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
