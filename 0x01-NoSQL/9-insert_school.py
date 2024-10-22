#!/usr/bin/env python3
'''Module for Task 9.
'''


def insert_school(mongo_collection, **kwargs):
    '''Inserts a new document into the specified MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection object where the document will be inserted.
        **kwargs: Arbitrary keyword arguments representing the document fields and values.

    Returns:
        The unique identifier (ID) of the newly inserted document.
    '''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
