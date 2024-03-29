#!/usr/bin/env python3
"""12-log_stats.py"""

from pymongo import MongoClient

def count_logs(collection):
    # Count total number of logs
    total_logs = collection.count_documents({})

    # Count number of logs with each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    # Count number of logs with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    return total_logs, method_counts, status_check_count

def main():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs  # Connect to 'logs' database
    collection = db.nginx  # Connect to 'nginx' collection

    # Get stats about Nginx logs
    total_logs, method_counts, status_check_count = count_logs(collection)

    # Display stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    main()

