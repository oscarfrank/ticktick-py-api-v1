# TickTick API Interaction Script

This project provides a set of Python scripts for interacting with the TickTick API v1. It allows you to perform various operations such as creating, retrieving, updating, and deleting tasks, as well as bulk operations (to create tasks) and task listing.

NB: This is using Ticktick v1 API which is available on their website. I'd recommend checking my profile in  for any updates as to implementing v2 API functionality when TickTick give me access. The API v2 seems to have more functionality, but isn't yet publicly available.

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/oscarfrank/ticktick-py-api-v1.git
   cd ticktick-py-api-v1
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your TickTick API credentials:
   ```
   CLIENT_ID=your_client_id_here
   CLIENT_SECRET=your_client_secret_here
   ```

## Project Structure

- `main.py`: The main interactive script
- `ticktick/`: Package containing core functionality
  - `api.py`: API interaction functions
  - `auth.py`: Authentication handling
  - `utils.py`: Utility functions
- `scripts/`: Individual operation scripts
- `config/`: Configuration files
- `data/`: Directory for CSV files (for bulk operations)

## Usage

### Main Interactive Script

Run the main interactive script:

```
python main.py
```

This script provides a menu-driven interface with the following options:

1. Add a new task
2. Retrieve a task by ID
3. Update a task
4. Delete a task
5. Mark a task as complete
6. Bulk add tasks from CSV
7. List daily tasks
8. List monthly tasks
9. Exit

### Individual Scripts

You can also use individual scripts for specific operations:

- Add a task: `python scripts/create_task.py`
- Update a task: `python scripts/update_task.py`
- Delete a task: `python scripts/delete_task.py`
- Complete a task: `python scripts/complete_task.py`
- Bulk add tasks: `python scripts/create_bulk_task.py`
- List daily tasks: `python scripts/list_daily_tasks.py`
- List monthly tasks: `python scripts/list_monthly_tasks.py`

## Features

- Add, retrieve, update, and delete individual tasks
- Mark tasks as complete
- Bulk add tasks from a CSV file
- List tasks for the current day or month
- Filter tasks by completion status
- Use "today" or "tomorrow" for quick date entry

## Date Formats

When entering dates, you can use the following formats:
- YYYY-MM-DD (e.g., 2023-07-01)
- YYYY-MM-DD HH:MM:SS (e.g., 2023-07-01 14:30:00)
- "today"
- "tomorrow"

## Priority Levels

Task priorities can be set to:
- high
- medium
- low
- none (default if not specified)

## CSV Format for Bulk Operations

For bulk adding tasks, use a CSV file with the following format:

```
Title,Start Date,Due Date,Priority
Task 1,2023-07-01,2023-07-02,high
Task 2,today,tomorrow,medium
Task 3,,,low
```

Place this file in the `data/` directory.

## API Endpoints

The script uses the following TickTick API endpoints:

- Add task: POST /open/v1/task
- Get task by ID: GET /open/v1/project/{projectId}/task/{taskId}
- Update task: POST /open/v1/task/{taskId}
- Delete task: DELETE /open/v1/project/{projectId}/task/{taskId}
- List tasks: GET /open/v1/task

Note: Some operations require both project ID and task ID. When adding a new task, both IDs will be displayed for future reference.

## Error Handling

The script includes basic error handling and will display error messages if operations fail. Check the console output for details on any issues encountered.

## Note

- Keep your `.env` file secure and do not share it publicly.
- The `ticktick_token.json` file will be created to store your access token. Do not delete this file unless you want to re-authenticate.

## Troubleshooting

If you encounter any issues:
- Check the console output for error messages.
- Ensure your API credentials are correct and up to date.
- Verify that you have the necessary permissions in your TickTick account to perform the operations.
- For operations requiring project ID, make sure you're using the correct ID as provided when creating the task.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.