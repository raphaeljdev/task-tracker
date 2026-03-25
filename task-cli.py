#!/usr/bin/env python3
"""
Task Tracker CLI - A simple command line task manager.

Usage:
    python task-cli.py add "Task description"
    python task-cli.py update <id> "New description"
    python task-cli.py delete <id>
    python task-cli.py mark-in-progress <id>
    python task-cli.py mark-done <id>
    python task-cli.py list
    python task-cli.py list done
    python task-cli.py list todo
    python task-cli.py list in-progress
"""

import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


# ── File helpers ──────────────────────────────────────────────────────────────

def load_tasks() -> list:
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error reading {TASKS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)


def save_tasks(tasks: list) -> None:
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except OSError as e:
        print(f"Error writing {TASKS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)


# ── ID helpers ────────────────────────────────────────────────────────────────

def next_id(tasks: list) -> int:
    return max((t["id"] for t in tasks), default=0) + 1


def find_task(tasks: list, task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_add(args):
    if not args:
        print("Usage: task-cli.py add <description>", file=sys.stderr)
        sys.exit(1)
    description = " ".join(args)
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")


def cmd_update(args):
    if len(args) < 2:
        print("Usage: task-cli.py update <id> <new description>", file=sys.stderr)
        sys.exit(1)
    task_id = parse_id(args[0])
    new_desc = " ".join(args[1:])
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task is None:
        print(f"Error: Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)
    task["description"] = new_desc
    task["updatedAt"] = now_iso()
    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")


def cmd_delete(args):
    if not args:
        print("Usage: task-cli.py delete <id>", file=sys.stderr)
        sys.exit(1)
    task_id = parse_id(args[0])
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Error: Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)
    save_tasks(new_tasks)
    print(f"Task {task_id} deleted successfully.")


def cmd_mark(args, status: str):
    if not args:
        print(f"Usage: task-cli.py mark-{status} <id>", file=sys.stderr)
        sys.exit(1)
    task_id = parse_id(args[0])
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task is None:
        print(f"Error: Task {task_id} not found.", file=sys.stderr)
        sys.exit(1)
    task["status"] = status
    task["updatedAt"] = now_iso()
    save_tasks(tasks)
    print(f"Task {task_id} marked as {status}.")


def cmd_list(args):
    STATUS_FILTER = {
        "done": "done",
        "todo": "todo",
        "in-progress": "in-progress",
    }
    filter_status = None
    if args:
        key = args[0].lower()
        if key not in STATUS_FILTER:
            print(f"Error: Unknown status '{args[0]}'. Use: done, todo, in-progress", file=sys.stderr)
            sys.exit(1)
        filter_status = STATUS_FILTER[key]

    tasks = load_tasks()
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("No tasks found.")
        return

    # Column widths
    id_w   = max(len("ID"),  max(len(str(t["id"])) for t in tasks))
    desc_w = max(len("Description"), max(len(t["description"]) for t in tasks))
    desc_w = min(desc_w, 60)  # cap long descriptions
    st_w   = max(len("Status"), max(len(t["status"]) for t in tasks))

    STATUS_ICONS = {"todo": "○", "in-progress": "◑", "done": "●"}
    hr = f"+-{'-'*id_w}-+-{'-'*desc_w}-+-{'-'*st_w}-+-{'-'*19}-+"

    print(hr)
    print(f"| {'ID':<{id_w}} | {'Description':<{desc_w}} | {'Status':<{st_w}} | {'Updated At':<19} |")
    print(hr)
    for t in tasks:
        icon   = STATUS_ICONS.get(t["status"], "?")
        desc   = t["description"]
        if len(desc) > desc_w:
            desc = desc[:desc_w - 1] + "…"
        status = f"{icon} {t['status']}"
        print(f"| {t['id']:<{id_w}} | {desc:<{desc_w}} | {status:<{st_w}} | {t['updatedAt']:<19} |")
    print(hr)
    print(f"  {len(tasks)} task(s) shown.")


# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_id(value: str) -> int:
    try:
        task_id = int(value)
        if task_id < 1:
            raise ValueError
        return task_id
    except ValueError:
        print(f"Error: '{value}' is not a valid task ID.", file=sys.stderr)
        sys.exit(1)


def usage():
    print(__doc__)
    sys.exit(0)


# ── Entry point ───────────────────────────────────────────────────────────────

COMMANDS = {
    "add":              lambda args: cmd_add(args),
    "update":           lambda args: cmd_update(args),
    "delete":           lambda args: cmd_delete(args),
    "mark-in-progress": lambda args: cmd_mark(args, "in-progress"),
    "mark-done":        lambda args: cmd_mark(args, "done"),
    "list":             lambda args: cmd_list(args),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        usage()

    command = sys.argv[1].lower()
    args    = sys.argv[2:]

    if command not in COMMANDS:
        print(f"Error: Unknown command '{command}'.", file=sys.stderr)
        print(f"Available commands: {', '.join(COMMANDS)}", file=sys.stderr)
        sys.exit(1)

    COMMANDS[command](args)


if __name__ == "__main__":
    main()
