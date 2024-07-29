import sys
import json
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta
from ticktick.auth import get_access_token
from ticktick.api import get_tasks

def list_monthly_tasks(status='all'):
    try:
        access_token = get_access_token()
        today = date.today()
        start_of_month = date(today.year, today.month, 1)
        if today.month == 12:
            end_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
        
        tasks = get_tasks(access_token, start_date=start_of_month, end_date=end_of_month, status=status)
        
        if tasks:
            return json.dumps({"status": "success", "tasks": tasks}, indent=2)
        else:
            return json.dumps({"status": "failure", "message": "No tasks found or failed to retrieve tasks."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    status = sys.argv[1] if len(sys.argv) > 1 else 'all'
    result = list_monthly_tasks(status)
    print(result)