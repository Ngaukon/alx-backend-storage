#!/usr/bin/env python3
'''Module for Task 10.
'''


def update_topics(mongo_collection, name, topics):
    '''Updates the topics of all documents in a collection that match the specified name.

    Args:
        mongo_collection: The MongoDB collection object containing the documents to update.
        name (str): The name of the documents to match for the update.
        topics (list): The new list of topics to set for the matched documents.
    
    Returns:
        The result of the update operation.
    '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
