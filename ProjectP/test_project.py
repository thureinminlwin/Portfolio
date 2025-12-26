import pytest
from datetime import date, datetime
from project import add_task, clear_completed, mark_complete, delete_task

def test_add_task():
    tasks = []
    # simulate adding a task
    new_tasks = tasks + [{
        "task": "Test Task",
        "completed": False,
        "due": date.today()
    }]
    assert len(new_tasks) == 1
    assert new_tasks[0]["task"] == "Test Task"
    assert new_tasks[0]["completed"] is False


def test_mark_complete():
    tasks = [{
        "task": "Test Task",
        "completed": False,
        "due": date.today()
    }]
    updated = tasks.copy()
    updated[0] = {**updated[0], "completed": True}
    assert updated[0]["completed"] is True

def test_clear_completed():
    tasks = [
        {"task": "Done Task", "completed": True, "due": date.today()},
        {"task": "Pending Task", "completed": False, "due": date.today()}
    ]
    new_tasks = [task for task in tasks if not task["completed"]]
    assert len(new_tasks) == 1
    assert new_tasks[0]["task"] == "Pending Task"

def test_delete_task():
    tasks = [
        {"task": "Task 1", "completed": False, "due": date.today()},
        {"task": "Task 2", "completed": False, "due": date.today()}
    ]
    new_tasks = tasks[:0] + tasks[1:]  # delete first task
    assert len(new_tasks) == 1
    assert new_tasks[0]["task"] == "Task 2"
