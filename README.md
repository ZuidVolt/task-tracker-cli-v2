# Task Tracker CLI

A simple command-line task tracking application to help you manage your to-do list efficiently.

#### extra info
  >this project was built for https://roadmap.sh/projects/task-tracker

## Features

- Add new tasks with descriptions
- Update existing task descriptions
- Mark tasks as "todo", "in-progress", or "done"
- Delete tasks
- List all tasks or filter by status
- Persistent storage using JSON

## Requirements

- Python 3.10 or higher

## Installation

Clone the repository:

```bash
git clone https://github.com/zuidvolt/task-tracker-cli-v2.git
cd task-tracker-cli
```

## Usage

### Basic Commands

**the best way to see an overview of the commands**
```bash
python main.py --help
```

**List all tasks:**
```bash
python main.py
```

**Add a task:**
```bash
python main.py --add "Complete project documentation"
```

**Update a task:**
```bash
python main.py --update 1 "Update project documentation with examples"
```

**Delete a task:**
```bash
python main.py --delete 1
```

### Task Status Management

**List tasks with a specific status:**
```bash
python main.py --list todo      # List only todo tasks
python main.py --list in-progress  # List only in-progress tasks
python main.py --list done      # List only completed tasks
python main.py --list all       # List all tasks (default)
```

**Change task status:**
```bash
python main.py --mark-in-progress 1  # Mark task 1 as in-progress
python main.py --mark-done 1         # Mark task 1 as done
```

## Development

This project uses:
- [Ruff](https://github.com/charliermarsh/ruff) for linting and formatting
- [MyPy](https://mypy.readthedocs.io/) for static type checking

Install development dependencies:
```bash
pip install -e ".[dev]"
```

## License

This project is licensed under the Apache License, Version 2.0 with important additional terms,
including specific commercial use conditions. Users are strongly advised to read the full
[LICENSE](LICENSE) file carefully before using, modifying, or distributing this work.
The additional terms contain crucial information about liability, data collection,
indemnification, and commercial usage requirements that may significantly affect your rights
and obligations.
