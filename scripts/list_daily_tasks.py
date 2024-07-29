import sys
import json
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from ticktick.auth import get_access_token
from ticktick.api import get_tasks

def list_daily_tasks(status='all'):
    try:
        access_token = get_access_token()
        today = date.today()
        tasks = get_tasks(access_token, start_date=today, end_date=today, status=status)
        
        if tasks:
            return json.dumps({"status": "success", "tasks": tasks}, indent=2)
        else:
            return json.dumps({"status": "failure", "message": "No tasks found or failed to retrieve tasks."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    status = sys.argv[1] if len(sys.argv) > 1 else 'all'
    result = list_daily_tasks(status)
    print(result)