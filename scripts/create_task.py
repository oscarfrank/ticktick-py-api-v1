import json
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ticktick.auth import get_access_token
from ticktick.api import add_task
from ticktick.utils import parse_date_or_datetime

def create_task(task_json):
    try:
        access_token = get_access_token()
        task_data = json.loads(task_json)
        
        title = task_data.get('title')
        start_date = parse_date_or_datetime(task_data.get('start_date'))
        due_date = parse_date_or_datetime(task_data.get('due_date'))
        priority = task_data.get('priority', 'none')
        
        result = add_task(access_token, title, start_date, due_date, priority)
        
        if result:
            return json.dumps({"status": "success", "task": result})
        else:
            return json.dumps({"status": "failure", "message": "Failed to create task"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_json = sys.argv[1]
    else:
        task_json = sys.stdin.read()
    
    result = create_task(task_json)
    print(result)