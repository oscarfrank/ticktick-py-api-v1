import json
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ticktick.auth import get_access_token
from ticktick.api import delete_task

def delete_task_script(task_id):
    try:
        access_token = get_access_token()
        
        result = delete_task(access_token, task_id)
        
        if result:
            return json.dumps({"status": "success", "message": f"Task {task_id} deleted successfully"})
        else:
            return json.dumps({"status": "failure", "message": f"Failed to delete task {task_id}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
    else:
        task_id = input("Enter task ID to delete: ")
    
    result = delete_task_script(task_id)
    print(result)