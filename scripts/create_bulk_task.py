import sys
import os
import csv
import json

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ticktick.auth import get_access_token
from ticktick.api import add_task
from ticktick.utils import parse_date_or_datetime

def create_bulk_tasks(filename='tasks.csv'):
    try:
        access_token = get_access_token()
        tasks_added = 0
        failed_tasks = []

        # Construct the full path to the CSV file
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)

        with open(csv_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            for row in csvreader:
                if len(row) == 4:
                    title, start_date_str, due_date_str, priority = row
                    start_date = parse_date_or_datetime(start_date_str.strip()) if start_date_str.strip() else None
                    due_date = parse_date_or_datetime(due_date_str.strip()) if due_date_str.strip() else None
                    result = add_task(access_token, title, start_date, due_date, priority)
                    if result:
                        tasks_added += 1
                    else:
                        failed_tasks.append(title)
                else:
                    failed_tasks.append(f"Invalid row: {row}")

        return json.dumps({
            "status": "success",
            "tasks_added": tasks_added,
            "failed_tasks": failed_tasks
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    result = create_bulk_tasks()
    print(result)