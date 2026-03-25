# 📋 Task Tracker CLI

A lightweight command-line task manager written in pure Python — no dependencies, no frameworks, just Python and a JSON file.

---

## Features

- Add, update, and delete tasks
- Mark tasks as **todo**, **in-progress**, or **done**
- Filter task listings by status
- Persistent storage in a local `tasks.json` file (auto-created on first use)
- Clean, formatted table output with status icons

---

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

Clone the repository and you're ready to go — no packages to install.

```bash
git clone https://github.com/raphaeljdev/task-tracker.git
cd task-tracker
```

---

## Usage

```bash
python task-cli.py <command> [arguments]
```

### Commands

| Command | Description |
|---|---|
| `add <description>` | Add a new task |
| `update <id> <description>` | Update a task's description |
| `delete <id>` | Delete a task |
| `mark-in-progress <id>` | Mark a task as in-progress |
| `mark-done <id>` | Mark a task as done |
| `list` | List all tasks |
| `list todo` | List only pending tasks |
| `list in-progress` | List only in-progress tasks |
| `list done` | List only completed tasks |

### Examples

```bash
# Adding tasks
python task-cli.py add "Buy groceries"
# Output: Task added successfully (ID: 1)

python task-cli.py add "Fix login bug"
# Output: Task added successfully (ID: 2)

# Updating a task
python task-cli.py update 2 "Fix critical login bug"

# Changing task status
python task-cli.py mark-in-progress 2
python task-cli.py mark-done 1

# Listing tasks
python task-cli.py list
```

**Sample output:**

```
+----+------------------------+-------------+---------------------+
| ID | Description            | Status      | Updated At          |
+----+------------------------+-------------+---------------------+
| 1  | Buy groceries          | ● done      | 2025-01-15T10:32:00 |
| 2  | Fix critical login bug | ◑ in-progress | 2025-01-15T10:35:42 |
+----+------------------------+-------------+---------------------+
  2 task(s) shown.
```

**Status icons:**

| Icon | Status |
|------|--------|
| `○` | todo |
| `◑` | in-progress |
| `●` | done |

---

## Data Storage

Tasks are stored in a `tasks.json` file in the current working directory. The file is created automatically on the first run.

**Example `tasks.json`:**

```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "status": "done",
    "createdAt": "2025-01-15T10:30:00",
    "updatedAt": "2025-01-15T10:32:00"
  },
  {
    "id": 2,
    "description": "Fix critical login bug",
    "status": "in-progress",
    "createdAt": "2025-01-15T10:31:00",
    "updatedAt": "2025-01-15T10:35:42"
  }
]
```

Each task contains:

- `id` — Unique, auto-incremented identifier
- `description` — Task description
- `status` — `todo`, `in-progress`, or `done`
- `createdAt` — ISO 8601 timestamp of creation
- `updatedAt` — ISO 8601 timestamp of last update

---

## Project Structure

```
task-tracker/
├── task-cli.py   # Main CLI application
├── tasks.json    # Auto-generated task storage (git-ignored)
└── README.md
```

> **Tip:** Add `tasks.json` to your `.gitignore` if you don't want to commit your task list.

---

## Design Decisions

- **No external libraries** — Uses only Python's built-in `json`, `os`, `sys`, and `datetime` modules.
- **Positional arguments** — Commands and IDs are passed as CLI positional arguments for simplicity.
- **Auto-incrementing IDs** — IDs always increase and are never reused after deletion.
- **Graceful error handling** — Invalid commands, missing tasks, and bad IDs all produce clear error messages and non-zero exit codes.

---

## License

This project is open source and available under the [MIT License](LICENSE).
