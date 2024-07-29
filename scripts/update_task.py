import sys
import os
import json

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ticktick.auth import get_access_token
from ticktick.api import update_task
from ticktick.utils import parse_date_or_datetime

def update_task_script(task_json):
    try:
        access_token = get_access_token()
        task_data = json.loads(task_json)
        
        task_id = task_data.get('id')
        if not task_id:
            return json.dumps({"status": "failure", "message": "Task ID is required"})
        
        update_data = {}
        if 'title' in task_data:
            update_data['title'] = task_data['title']
        if 'start_date' in task_data:
            update_data['startDate'] = parse_date_or_datetime(task_data['start_date'])
        if 'due_date' in task_data:
            update_data['dueDate'] = parse_date_or_datetime(task_data['due_date'])
        if 'priority' in task_data:
            update_data['priority'] = task_data['priority']
        
        result = update_task(access_token, task_id, update_data)
        
        if result:
            return json.dumps({"status": "success", "task": result})
        else:
            return json.dumps({"status": "failure", "message": "Failed to update task"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_json = sys.argv[1]
    else:
        task_json = sys.stdin.read()
    
    result = update_task_script(task_json)
    print(result)