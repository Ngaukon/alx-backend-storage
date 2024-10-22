#!/usr/bin/env python3
'''Module for Task 8.
'''


def list_all(mongo_collection):
    '''Retrieves and returns a list of all documents in the specified MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection object to query.

    Returns:
        A list containing all documents in the collection.
    '''
    return [doc for doc in mongo_collection.find()]
