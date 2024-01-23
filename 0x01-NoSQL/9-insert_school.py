#!/usr/bin/env python3

"""
Python function that inserts a new document in the collection
based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts new document in the collection """
    return mongo_collection.insert_one(kwargs).inserted_id
