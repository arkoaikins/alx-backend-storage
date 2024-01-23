#!/usr/bin/env python3
"""
Python script that provides some
stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    all_logs = collection.count_documents({})
    get_logs = collection.count_documents({"method": "GET"})
    post_logs = collection.count_documents({"method": "POST"})
    put_logs = collection.count_documents({"method": "PUT"})
    patch_logs = collection.count_documents({"method": "PATCH"})
    delete_logs = collection.count_documents({"method": "DELETE"})
    checks = collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{all_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_logs}")
    print(f"\tmethod POST: {post_logs}")
    print(f"\tmethod PUT: {put_logs}")
    print(f"\tmethod PATCH: {patch_logs}")
    print(f"\tmethod DELETE: {delete_logs}")
    print(f"{checks} status_checks")
