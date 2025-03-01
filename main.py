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
    json_str = json.dumps(data, indent=4)
    with Path.open(path, "w") as file:
        file.write(json_str)


def read_from_json_file(path: Path) -> list[Task]:
    with Path.open(path, "r") as file:
        json_str = file.read()
        return list[Task](json.loads(json_str))


def create_task_id_list(current_list: list[Task]) -> list[int]:
    id_list: list[int] = []
    for task in current_list:
        id_list.append(task["id"])
    return id_list


def add_task_id(id_list: list[int]) -> int:
    return max(id_list) + 1


def update_task_status(current_list: list[Task], task_id: int, new_status: str) -> None:
    for task in current_list:
        if task["id"] == task_id:
            task["status"] = new_status


parser = argparse.ArgumentParser(
    prog="Task-Tracker",
    description="Keep your tasks in tracks",
)


_ = parser.add_argument("--add", "-a", help="adds a new task", nargs=1, type=str, default=None)
_ = parser.add_argument("--update", "-u", nargs=2, default=None)
_ = parser.add_argument("--delete", "-d", nargs=1, type=int, default=None)
_ = parser.add_argument("--list", "-l", nargs=2, help="lists all tasks", default="all")
_ = parser.add_argument("--mark-in-progress", "-mp", nargs=1, type=int, default=None)
_ = parser.add_argument("--mark-done", "-md", nargs=1, type=int, default=None)


args = parser.parse_args()


def main() -> None:  # noqa: C901
    task_list: list[Task] = read_from_json_file(JSON_PATH)

    # Add default tasks for demonstration
    # add_task(create_task(0, "test"), task_list)
    # add_task(create_task(1, "test-2"), task_list)

    # Handle different arguments
    if args.add:
        add_task(create_task(add_task_id(create_task_id_list(task_list)), str(args.add[0])), task_list)
    elif args.update:
        try:
            task_id = int(args.update[0])
            new_status = str(args.update[1])
            update_task_status(task_list, task_id, new_status)
        except IndexError:
            print("Invalid update format")
    elif args.delete:
        # Handle delete task
        pass
    elif args.list:
        try:
            match str(args.list[0]):
                case "all":
                    pass
                case "done":
                    pass
                case "in-progress":
                    pass
                case "todo":
                    pass
                case _:
                    print(f"Unknown list type: {args.list[0]}")
        except IndexError:
            print("Invalid list type (must be a string)")
    elif args.mark_in_progress:
        # Handle mark in progress
        pass
    elif args.mark_done:
        # Handle mark done
        pass
    else:
        # Default action - list all tasks
        pass
    print(task_list)
    write_to_json_file(task_list, JSON_PATH)


if __name__ == "__main__":
    main()
