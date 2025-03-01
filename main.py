from datetime import datetime
from pathlib import Path
from models import Task
import argparse
import json

JSON_PATH: Path = Path("data.json")


def check_json_file_exists() -> None:
    if not JSON_PATH.exists():
        Path.touch(JSON_PATH)


def create_task(task_id: int, description: str) -> Task:
    return {
        "id": task_id,
        "description": description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }


def append_task(new_task: Task, task_list: list[Task]) -> None:
    task_list.append(new_task)


def write_to_json_file(data: list[Task], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    json_str = json.dumps(data, indent=4, default=str)
    with path.open("w") as file:
        file.write(json_str)


def read_from_json_file(path: Path) -> list[Task]:
    try:
        if not path.exists():
            return []
        with path.open("r") as file:
            json_str = file.read()
            return list[Task](json.loads(json_str))
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error reading tasks: {e}")
        return []


def create_task_id_list(current_list: list[Task]) -> list[int]:
    return [task["id"] for task in current_list]


def generate_task_id(id_list: list[int]) -> int:
    if not id_list:
        print("the id list is empty")
        raise ValueError
    return max(id_list) + 1


def update_task_description(current_list: list[Task], task_id: int, description: str) -> None:
    for task in current_list:
        if task["id"] == task_id:
            task["description"] = description
            task["updated_at"] = datetime.now().isoformat()


def update_task_status(current_list: list[Task], task_id: int, new_status: str) -> None:
    for task in current_list:
        if task["id"] == task_id:
            if task["status"] == new_status:
                print(f"the status is already {new_status}")
            task["status"] = new_status
            task["updated_at"] = datetime.now().isoformat()


def update_all_task_ids(current_list: list[Task], removed_task_id: int) -> None:
    if not current_list:
        return
    for task in current_list:
        if task["id"] > removed_task_id:
            task["id"] -= 1


def delete_task(current_list: list[Task], task_id: int) -> bool:
    for i, task in enumerate(current_list):
        if task["id"] == task_id:
            del current_list[i]
            return True
    print(f"Task with ID {task_id} not found in the current list.")
    return False


def check_id_value(current_id_list: list[int], index_id: int) -> bool:
    if not current_id_list:
        return False
    return index_id in current_id_list


def change_task_progress(task_list: list[Task], task_id_list: list[int], task_id: int, status_str: str) -> None:
    try:
        if not check_id_value(task_id_list, task_id):
            raise ValueError("Invalid task ID")
        update_task_status(task_list, task_id, status_str)
    except IndexError:
        print("Invalid task ID")


def list_tasks(current_list: list[Task], list_format: str = "all") -> None:
    filtered_tasks = []
    # Filter tasks based on list_format
    match list_format:
        case "all":
            filtered_tasks = current_list
            status_display = "ALL TASKS"
        case "done":
            filtered_tasks = [task for task in current_list if task["status"] == "done"]
            status_display = "COMPLETED TASKS"
        case "in-progress":
            filtered_tasks = [task for task in current_list if task["status"] == "in-progress"]
            status_display = "IN-PROGRESS TASKS"
        case "todo":
            filtered_tasks = [task for task in current_list if task["status"] == "todo"]
            status_display = "TODO TASKS"
        case _:
            print(f"Unknown list type: {list_format}")
            return
    if not filtered_tasks:
        print(f"No {list_format} tasks found.")
        return

    # Calculate width based on the longest task description
    max_desc_length = max(len(task["description"]) for task in filtered_tasks) if filtered_tasks else 10
    max_desc_length = min(max_desc_length, 50)  # Cap at 50 chars to prevent overly wide output

    id_width = 4
    desc_width = max_desc_length + 2
    status_width = 12
    total_width = id_width + desc_width + status_width + 4  # +4 for separators

    # Print header
    print("\n" + "=" * total_width)
    print(f" {status_display} ".center(total_width))
    print("=" * total_width)
    print(f"{'ID':<{id_width}} | {'DESCRIPTION':<{desc_width}} | {'STATUS':<{status_width}}")
    print("-" * total_width)

    # Print tasks
    for task in filtered_tasks:
        description = task["description"]
        if len(description) > max_desc_length:
            description = description[: max_desc_length - 3] + "..."
        status = task["status"]
        status_formatted = status.upper()
        print(f"{task['id']:<{id_width}} | {description:<{desc_width}} | {status_formatted:<{status_width}}")
    # Print footer
    print("-" * total_width)
    print(f"Total: {len(filtered_tasks)} task(s)")
    print()


parser = argparse.ArgumentParser(
    prog="task-tracker",
    description="A command-line task tracking application to manage your to-do list",
)

# Group related arguments for better organization
task_management = parser.add_argument_group("Task Management")
task_viewing = parser.add_argument_group("Task Viewing")
status_management = parser.add_argument_group("Status Management")

# Task Management arguments
_ = task_management.add_argument(
    "--add",
    "-a",
    help="Add a new task with the provided description",
    nargs=1,
    type=str,
    default=None,
    metavar="DESCRIPTION",
)

_ = task_management.add_argument(
    "--update",
    "-u",
    help="Update an existing task by providing task ID and new description",
    nargs=2,
    default=None,
    metavar=("ID", "NEW_DESCRIPTION"),
)

_ = task_management.add_argument(
    "--delete",
    "-d",
    help="Delete a task by its ID",
    nargs=1,
    type=int,
    default=None,
    metavar="ID",
)

# Task Viewing arguments
_ = task_viewing.add_argument(
    "--list",
    "-l",
    help="List tasks with optional filter by status: 'all', 'todo', 'in-progress', or 'done'",
    nargs="?",
    const="all",
    default=None,
    metavar="STATUS",
    choices=["all", "todo", "in-progress", "done"],
)

# Status Management arguments
_ = status_management.add_argument(
    "--mark-in-progress",
    "-mp",
    help="Mark a task as 'in-progress' by its ID",
    nargs=1,
    type=int,
    default=None,
    metavar="ID",
)

_ = status_management.add_argument(
    "--mark-done",
    "-md",
    help="Mark a task as 'done' by its ID",
    nargs=1,
    type=int,
    default=None,
    metavar="ID",
)

args = parser.parse_args()


def main() -> None:  # noqa: C901
    check_json_file_exists()
    task_list: list[Task] = read_from_json_file(JSON_PATH)
    task_id_list: list[int] = create_task_id_list(task_list)
    if args.add:
        try:
            description = str(args.add[0])
            new_task_id = generate_task_id(task_id_list)
            append_task(create_task(new_task_id, description), task_list)
        except TypeError:
            print("the description must be a string")
    elif args.update:
        try:
            task_id = int(args.update[0])
            if not check_id_value(task_id_list, task_id):
                raise ValueError("Invalid task ID")
            new_description = str(args.update[1])
            if not new_description:
                raise ValueError("Description cannot be empty")
            update_task_description(task_list, task_id, new_description)
        except TypeError:
            print("Invalid update format")
    elif args.delete:
        task_id_to_remove = int(args.delete[0])
        if not check_id_value(task_id_list, task_id_to_remove):
            raise ValueError("Invalid task ID")
        if delete_task(task_list, task_id_to_remove):
            update_all_task_ids(task_list, task_id_to_remove)
    elif args.list:
        try:
            list_format = str(args.list[0])
            list_tasks(task_list, list_format)
        except IndexError:
            print("Invalid list type (must be a string)")
    elif args.mark_in_progress:
        change_task_progress(task_list, task_id_list, int(args.mark_in_progress[0]), "in-progress")
    elif args.mark_done:
        change_task_progress(task_list, task_id_list, int(args.mark_done[0]), "done")
    else:
        list_tasks(task_list)
    write_to_json_file(task_list, JSON_PATH)


if __name__ == "__main__":
    main()
