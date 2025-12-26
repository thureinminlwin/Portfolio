# Task Flow
#### Video Demo:https://youtu.be/fwacM1pnSeM
#### Description:
This Python project is a comprehensive to-do-list application that runs from the command line. The application’s core functionalities are inspired by Google Tasks, the most minimalist and cleanest one on the market. Despite the limitations of the command line, unlike a GUI, the application is designed to be as user-friendly as possible, which is made possible by the use of two main menus.
Like most to-do list applications, users are not limited to only a single list. The moment the application is run, users will be welcomed by the main menu, which supports functionalities like choosing, creating, and deleting a list. Entering 2 will ask for a name and due date for the new to-do list, for example, “Work,” “Groceries,” or “University.” Entering “3” will display a list of the user’s existing to-do lists, where the user types the number of the list they want to delete. Selecting a list will also display existing to-do lists. However, if you do not have any lists, a message will be shown, and the user will be redirected to the main top-level menu.
Once a list is selected, a secondary menu provides a full suite of task management operations.
- View all tasks: All tasks are listed with numbers, due information, and an icon indicating whether the task has been completed or not. For example, a completed task will be displayed like “✅ Cook rice,” while a task due will be displayed like “⬜ Do laundry - 5 days left.”
- Add new tasks: When adding a task, the program prompts not only for the task name but also for a due date in YYYY-MM-DD format. Entering invalid due dates will repeatedly prompt for a correct input.
- Mark a task as complete: Users can update the complete status of a task. When displaying the list, the white icon will turn green for the completed tasks, which clearly separates tasks visually.
- Delete a specific task: Unwanted or incorrectly entered tasks can be removed easily.
- Clear all completed tasks: A convenient clean-up function allows users to quickly archive finished items, keeping the active list tidy.

For a better user experience, users are displayed responses for every action, whether creating a new list or asking for confirmation to delete a list. The command-line interface also includes thoughtful user experience enhancements, such as emojis and structured menu designs, to make navigation engaging and less intimidating.

The program strongly relies on a central dictionary to store all the to-do lists and the tasks within each list. The name of each list is a key in this dictionary, and the value is a list of tasks. Each task is represented by a dictionary with three key-value pairs: the task name, the complete status, and the due date. A key design decision in the program was to always return new task lists when changes are made instead of mutating the original lists directly. For example, functions like clear_completed or delete_task create a new list with the desired changes and then reassign it to the current list. After receiving the list back in the main program, the central dictionary is saved in the JSON file.

Overall, this project is a practical and well-engineered tool that showcases proficiency in file I/O, data structures, date/time manipulation, and user-centric interface design within Python.

