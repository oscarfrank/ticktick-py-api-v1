import sys
import json
from datetime import date, timedelta
from ticktick.auth import get_access_token
from ticktick.api import add_task, get_task_by_id, update_task, delete_task, complete_task, get_tasks
from ticktick.utils import parse_date_or_datetime, format_date_for_api
from scripts.create_bulk_task import create_bulk_tasks

def main():
    try:
        print("Authenticating...")
        access_token = get_access_token()
        print("Authentication successful!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new task")
        print("2. Retrieve a task by ID")
        print("3. Update a task")
        print("4. Delete a task")
        print("5. Mark a task as complete")
        print("6. Bulk add tasks from CSV")
        print("7. List daily tasks")
        print("8. List monthly tasks")
        print("9. Exit")
        
        choice = input("Enter your choice (1-9): ")
        
        try:
            if choice == '1':
                task_title = input("Enter the task title: ")
                start_date = input("Enter the start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, 'today', or 'tomorrow') or press Enter to skip: ")
                due_date = input("Enter the due date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, 'today', or 'tomorrow') or press Enter to skip: ")
                priority = input("Enter priority (high, medium, low, or none): ")
                
                result = add_task(access_token, task_title, start_date, due_date, priority)
                
                if result:
                    print(f"Task created with ID: {result['id']}")
                    print(f"Project ID: {result['projectId']}")
                else:
                    print("Failed to create task")
            
            elif choice == '2':
                project_id = input("Enter the project ID: ")
                task_id = input("Enter the task ID: ")
                task = get_task_by_id(access_token, project_id, task_id)
                if task:
                    print("Task details:")
                    print(json.dumps(task, indent=2))
                else:
                    print("Failed to retrieve task")
            
            elif choice == '3':
                task_id = input("Enter the task ID to update: ")
                update_data = {}
                title = input("Enter new title (or press Enter to skip): ")
                if title:
                    update_data['title'] = title
                start_date = input("Enter new start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, 'today', or 'tomorrow') or press Enter to skip: ")
                if start_date:
                    update_data['startDate'] = parse_date_or_datetime(start_date)
                due_date = input("Enter new due date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS, 'today', or 'tomorrow') or press Enter to skip: ")
                if due_date:
                    update_data['dueDate'] = parse_date_or_datetime(due_date)
                priority = input("Enter new priority (high, medium, low, or none) or press Enter to skip: ")
                if priority:
                    update_data['priority'] = priority
                
                result = update_task(access_token, task_id, update_data)
                if result:
                    print("Task updated successfully")
                else:
                    print("Failed to update task")
            
            elif choice == '4':
                project_id = input("Enter the project ID: ")
                task_id = input("Enter the task ID to delete: ")
                result = delete_task(access_token, project_id, task_id)
                if result:
                    print("Task deleted successfully")
                else:
                    print("Failed to delete task")
            
            elif choice == '5':
                task_id = input("Enter the task ID to mark as complete: ")
                result = complete_task(access_token, task_id)
                if result:
                    print("Task marked as complete")
                else:
                    print("Failed to mark task as complete")
            
            elif choice == '6':
                filename = input("Enter the CSV filename (default is tasks.csv): ") or "tasks.csv"
                result = create_bulk_tasks(filename)
                print(result)
            
            elif choice == '7':
                today = date.today()
                status = input("Enter status (all, completed, or incomplete) [default: all]: ") or "all"
                tasks = get_tasks(access_token, start_date=today, end_date=today, status=status)
                if tasks:
                    print(json.dumps(tasks, indent=2))
                else:
                    print("No tasks found or failed to retrieve tasks.")
            
            elif choice == '8':
                today = date.today()
                start_of_month = date(today.year, today.month, 1)
                if today.month == 12:
                    end_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
                else:
                    end_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
                status = input("Enter status (all, completed, or incomplete) [default: all]: ") or "all"
                tasks = get_tasks(access_token, start_date=start_of_month, end_date=end_of_month, status=status)
                if tasks:
                    print(json.dumps(tasks, indent=2))
                else:
                    print("No tasks found or failed to retrieve tasks.")
            
            elif choice == '9':
                print("Exiting the program. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()