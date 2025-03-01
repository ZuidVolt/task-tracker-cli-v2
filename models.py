from typing import TypedDict


class Task(TypedDict):
    id: int
    description: str
    status: str
    created_at: str
    updated_at: str
