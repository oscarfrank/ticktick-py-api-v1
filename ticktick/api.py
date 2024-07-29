import requests
import json
from datetime import date, datetime
from config.settings import TASK_URL
from .utils import format_date_for_api, parse_date_or_datetime

def add_task(access_token, task_title, start_date, due_date, priority, list_id=None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    task_data = {
        "title": task_title,
    }

    if start_date:
        task_data["startDate"] = format_date_for_api(parse_date_or_datetime(start_date))
    if due_date:
        task_data["dueDate"] = format_date_for_api(parse_date_or_datetime(due_date))

    if priority:
        if priority == "high":
            task_data["priority"] = 5
        elif priority == "medium":
            task_data["priority"] = 3
        elif priority == "low":
            task_data["priority"] = 1
    else:
        task_data["priority"] = 0

    if list_id:
        task_data["projectId"] = list_id
    
    response = requests.post(TASK_URL, json=task_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return {
            "id": result.get("id"),
            "projectId": result.get("projectId")
        }
    else:
        print(f"Failed to add task. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None
        
def get_task_by_id(access_token, project_id, task_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    url = f"{TASK_URL}/{project_id}/task/{task_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve task. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def update_task(access_token, task_id, update_data):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    url = f"{TASK_URL}/{task_id}"
    
    if 'startDate' in update_data:
        update_data['startDate'] = format_date_for_api(update_data['startDate'])
    if 'dueDate' in update_data:
        update_data['dueDate'] = format_date_for_api(update_data['dueDate'])
    
    response = requests.post(url, json=update_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to update task. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def delete_task(access_token, project_id, task_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    url = f"{TASK_URL}/{project_id}/task/{task_id}"
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        print(f"Failed to delete task. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def complete_task(access_token, task_id):
    return update_task(access_token, task_id, {"status": 2})

def get_tasks(access_token, start_date=None, end_date=None, status='all'):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {}
    if start_date:
        params['startDate'] = format_date_for_api(parse_date_or_datetime(start_date))
    if end_date:
        params['endDate'] = format_date_for_api(parse_date_or_datetime(end_date))
    if status in ['completed', 'incomplete']:
        params['status'] = status
    
    response = requests.get(TASK_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve tasks. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None