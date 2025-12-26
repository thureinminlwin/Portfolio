import json
from datetime import datetime, date

def main():
    data = load_data()
    while True:
        main_choice = main_menu()
        if main_choice == "1":
            list_choice = choose_list(data) # This gets back the list name
            if not list_choice == None:
                tasks = data[list_choice]
                while True:
                    choice = options(list_choice)
                    if choice ==  "1":
                        view_tasks(tasks)
                    elif choice == "2":
                        tasks = add_task(tasks)
                    elif choice == "3":
                        tasks = mark_complete(tasks)
                    elif choice == "4":
                        tasks = clear_completed(tasks)
                    elif choice == "5":
                        tasks = delete_task(tasks)
                    elif choice == "6":
                        break
                    else:
                        print("❌ Invalid input")
                    data[list_choice] = tasks
                    save_data(data)
        elif main_choice == "2":
            add_list(data)
        elif main_choice == "3":
            delete_list(data)
        elif main_choice == "4":
            break
        else:
            print("❌ Invalid input")

# Main menu
def main_menu():
    print("""
        😊 Welcome!
========== Main Menu ==========
1. 📂 Select a list
2. ➕ Create new list
3. 🗑️  Delete a list
4. ❌ Quit
          """)
    return input("Enter your choice(1-4): ").strip()


# Viewing a to-do-list
def choose_list(data):
    if not data:
        print("\n⚠️ No list found. Create one first.")
        return None
    print("\nYour lists: ")
    show_list(data)
    try:
        choice = int(input("\nChoose a list by number: ").strip())
        list_name = list(data.keys())[choice-1]
        return list_name
    except(ValueError, IndexError):
        print("❌ Invalid choice")
        return None


# Adding a new to-do-list
def add_list(data):
    while True:
        list_name = input("Enter a name for your new to-do-list: ").strip()
        if list_name in data:
            print("⚠️ A list with that name already exists!")
        elif not list_name:
            print("⚠️ List name cannot be empty!")
        else:
            break
    data[list_name] = []   # create empty list
    save_data(data)
    print(f"\n✅ Created new list '{list_name}'")

# Deleting a to-do-list
def delete_list(data):
    if not data:
        print("\n⚠️ No list to delete.")
        return
    print("\nYour lists: ")
    show_list(data)
    try:
        choice = int(input("\nChoose a list number to delete: ").strip())
        list_name = list(data.keys())[choice - 1]
        confirm = input(f"Are you sure you want to delete '{list_name}'? (y/n): ")
        if confirm.lower() in ["y","yes"]:
            del data[list_name]
            print(f"🗑️ Deleted list '{list_name}'")
            save_data(data)   # Save changes after deleting
        else:
            print("❌ Cancelled")

    except (ValueError, IndexError):
        print("❌ Invalid input")

def show_list(data):
    for i, name in enumerate(data.keys(), 1):
        print(f"{i}. {name}")

# Loading data from the json file
def load_data():
    try:
        with open("tasks.json","r") as f:
            data = json.load(f)
            for tasklist in data.values():
                for task in tasklist:
                    task["due"] = date.fromisoformat(task["due"])
            return data
    except FileNotFoundError:
        return {}

# Saving data to the file after each change
def save_data(data):
    serializable = {}
    for list_name, tasklist in data.items():
        serializable[list_name] = []
        for task in tasklist:
            serializable[list_name].append({
                "task": task["task"],
                "completed": task["completed"],
                "due": task["due"].isoformat() if task["due"] else None
            })
    with open("tasks.json","w") as f:
        json.dump(serializable, f, indent=4)

# Options for each list
def options(name):
    print(f"""\n========== {name} ==========\n
1. ☑️ View tasks
2. ➕ Add a task
3. ✅ Mark a task as complete
4. 🧹 Clear all completed tasks
5. 🗑️  Delete a task
6. ❌ Quit
          """)
    return input("Enter your choice(1-6): ").strip()

# Viewing the tasks in the list
def view_tasks(tasks):
    print(f"\n========== Your List ===========\n")
    if not tasks:
        print("Your list is empty!")
    else:
        today = date.today()
        for i,task in enumerate(tasks, 1):
            day = task["due"] - today
            due_info = ""
            status = "✅" if task["completed"] else "⬜"
            if not task["completed"]:
                if day.days > 0:
                    due_info = f"- {day.days} days left"
                elif day.days == 0:
                    due_info = "- Due today!"
                else:
                    due_info = f"- Overdue by {abs(day.days)} days"
            print(f"{i}. {status} {task['task']} {due_info}")


# Adding a task to a list
def add_task(tasks):
    task_name = input("Enter a task: ")
    while not task_name.strip():
        task_name = input("Task name cannot be empty. Enter again: ")
    while True:
        due_str = input("Enter due date (YYYY-MM-DD): ")
        try:
            due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Invalid date format.")
    new_tasks = tasks + [{"task": task_name, "completed": False, "due": due_date}]
    print("\n✅Task added!")
    view_tasks(new_tasks)
    return new_tasks

# Marking a task as complete in a list
def mark_complete(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        task = int(input("\nEnter the number of the task to mark as complete: ").strip())
        if 1 <= task <= len(tasks):
            updated = tasks.copy()
            updated[task-1] = {
                **updated[task-1],
                "completed": True
            }
            print(f"✅ Marked {tasks[task-1]['task']} as complete!")
            view_tasks(updated)
            return updated
        else:
            print("❌ Invalid task number")
    except (ValueError, IndexError):
        print("❌ Invalid input. Please enter a number")
    return tasks

# Clearing all completed tasks
def clear_completed(tasks):
    before = len(tasks)
    new_tasks = [task for task in tasks if not task["completed"]]
    after = len(new_tasks)
    print(f"\n🧹 Cleared {before-after} completed tasks!")
    view_tasks(new_tasks)
    return new_tasks

# Deleting a task in a list
def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        task = int(input("\nEnter the number of the task to delete: ").strip())
        if 1 <= task <= len(tasks):
            new_tasks = tasks[:task-1] + tasks[task:]
            print(f"🗑️ Deleted {tasks[task-1]['task']}")
            view_tasks(new_tasks)
            return new_tasks
        else:
            print("❌ Invalid task number")
    except (ValueError, IndexError):
        print("❌ Invalid input. Please enter a number")

    return tasks

if __name__ == "__main__":
    main()