from datetime import datetime
from pathlib import Path
from models import Task
import argparse
import json

JSON_PATH: Path = Path("data.json")


def create_task(task_id: int, description: str) -> Task:
    return {
        "id": task_id,
        "description": description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }


def add_task(new_task: Task, task_list: list[Task]) -> None:
    task_list.append(new_task)


def write_to_json_file(data: list[Task], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    json_str = json.dumps(data, indent=4, default=str)  # default=str helps with datetime objects
    with path.open("w") as file:
        file.write(json_str)


def read_from_json_file(path: Path) -> list[Task]:
    try:
        if not path.exists():
            return []
        with Path.open(path, "r") as file:
            json_str = file.read()
            return list[Task](json.loads(json_str))
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error reading tasks: {e}")
        return []


def create_task_id_list(current_list: list[Task]) -> list[int]:
    id_list: list[int] = []
    for task in current_list:
        id_list.append(task["id"])
    return id_list


def add_task_id(id_list: list[int]) -> int:
    return max(id_list) + 1


def update_all_task_ids() -> None:
    pass


def update_task_description(current_list: list[Task], task_id: int, description: str) -> None:
    for task in current_list:
        if task["id"] == task_id:
            task["description"] = description


def check_id_value(current_id_list: list[int], index_id: int) -> bool:
    if not current_id_list:
        return False
    return index_id in current_id_list


def update_task_status(current_list: list[Task], task_id: int, new_status: str) -> None:
    for task in current_list:
        if task["id"] == task_id:
            if task["status"] == new_status:
                print(f"the staus is alreday {new_status}")
            task["status"] = new_status


def list_tasks(current_list: list[Task], list_format: str = "all") -> None:  # noqa: C901
    match list_format:
        case "all":
            for task in current_list:
                print(f"{task['id']} - {task['description']} - {task['status']}")
        case "done":
            for task in current_list:
                if task["status"] == "done":
                    print(f"{task['id']} - {task['description']} - {task['status']}")
        case "in-progress":
            for task in current_list:
                if task["status"] == "in-progress":
                    print(f"{task['id']} - {task['description']} - {task['status']}")
        case "todo":
            for task in current_list:
                if task["status"] == "todo":
                    print(f"{task['id']} - {task['description']} - {task['status']}")
        case _:
            print(f"Unknown list type: {args.list[0]}")


parser = argparse.ArgumentParser(
    prog="Task-Tracker",
    description="Keep your tasks in tracks",
)

_ = parser.add_argument("--add", "-a", help="adds a new task", nargs=1, type=str, default=None)
_ = parser.add_argument("--update", "-u", nargs=2, default=None)
_ = parser.add_argument("--delete", "-d", nargs=1, type=int, default=None)
_ = parser.add_argument("--list", "-l", nargs="?", help="lists all tasks", default=None)
_ = parser.add_argument("--mark-in-progress", "-mp", nargs=1, type=int, default=None)
_ = parser.add_argument("--mark-done", "-md", nargs=1, type=int, default=None)


args = parser.parse_args()


def main() -> None:  # noqa: C901
    task_list: list[Task] = read_from_json_file(JSON_PATH)
    task_id_list: list[int] = create_task_id_list(task_list)

    # Add default tasks for demonstration
    # add_task(create_task(0, "test"), task_list)
    # add_task(create_task(1, "test-2"), task_list)

    # Handle different arguments
    if args.add:
        try:
            description = str(args.add[0])
            new_task_id = add_task_id(task_id_list)
            add_task(create_task(new_task_id, description), task_list)
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
        # Handle delete task
        pass
    elif args.list:
        try:
            list_format = str(args.list[0])
            list_tasks(task_list, list_format)
        except IndexError:
            print("Invalid list type (must be a string)")
    elif args.mark_in_progress:
        try:
            task_id = int(args.mark_in_progress[0])
            if not check_id_value(task_id_list, task_id):
                raise ValueError("Invalid task ID")
            satus_str = "in progress"
            update_task_status(task_list, task_id, satus_str)
        except IndexError:
            print("Invalid task ID")
    elif args.mark_done:
        try:
            task_id = int(args.mark_in_progress[0])
            if not check_id_value(task_id_list, task_id):
                raise ValueError("Invalid task ID")
            satus_str = "done"
            update_task_status(task_list, task_id, satus_str)
        except IndexError:
            print("Invalid task ID")
    else:
        list_tasks(task_list)
    write_to_json_file(task_list, JSON_PATH)


if __name__ == "__main__":
    main()
