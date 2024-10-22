#!/usr/bin/env python3
'''Module for Task 14.
'''


def top_students(mongo_collection):
    '''Prints all students in a collection sorted by their average score.

    Args:
        mongo_collection: The MongoDB collection containing student documents.

    Returns:
        A cursor with all students sorted by average score in descending order.
    '''
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return students
