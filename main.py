from datetime import datetime
from models import Task
import argparse


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


parser = argparse.ArgumentParser(
    prog="Task-Tracker",
    description="Keep your tasks in tracks",
)


_ = parser.add_argument("--add", help="adds a new task", type=str, default=None)
_ = parser.add_argument("--update", nargs=2, default=None)
_ = parser.add_argument("--delete", type=int, default=None)
_ = parser.add_argument("--list", nargs=2, help="lists all tasks", default=None)
_ = parser.add_argument("--mark-in-progress", type=int, default=None)
_ = parser.add_argument("--mark-done", type=int, default=None)

args = parser.parse_args()


def main() -> None:
    task_list: list[Task] = []

    # Add default tasks for demonstration
    add_task(create_task(0, "test"), task_list)
    add_task(create_task(1, "test-2"), task_list)

    # Handle different arguments
    if args.add:
        # Handle add task
        pass
    elif args.update:
        # Handle update task
        pass
    elif args.delete:
        # Handle delete task
        pass
    elif args.list:
        # Handle list tasks
        pass
    elif args.mark_in_progress:
        # Handle mark in progress
        pass
    elif args.mark_done:
        # Handle mark done
        pass
    else:
        # Default action - list all tasks
        print(task_list)


if __name__ == "__main__":
    main()
