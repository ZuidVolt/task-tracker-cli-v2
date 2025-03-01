from typing import TypedDict


class Task(TypedDict):
    """
    Represents a task in the task tracking system.

    Attributes:
        id (int): Unique identifier for the task
        description (str): Description of the task
        status (str): Current status of the task (e.g., "todo", "in progress", "done")
        created_at (str): ISO format timestamp of when the task was created
        updated_at (str): ISO format timestamp of when the task was last updated
    """

    id: int
    description: str
    status: str
    created_at: str
    updated_at: str
