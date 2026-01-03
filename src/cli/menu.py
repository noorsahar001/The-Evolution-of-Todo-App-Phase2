def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Todo App Menu ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Task Completion")
    print("6. Exit")
    print()


def get_user_choice() -> str:
    """Get and return the user's menu choice."""
    return input("Enter your choice: ").strip()
