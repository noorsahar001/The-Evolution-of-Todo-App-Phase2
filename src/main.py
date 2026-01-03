from src.services.task_service import TaskService
from src.cli.menu import display_menu, get_user_choice
from src.cli.commands import (
    add_task_command,
    view_tasks_command,
    update_task_command,
    delete_task_command,
    toggle_task_command,
)


def main() -> None:
    """Main application entry point."""
    service = TaskService()

    while True:
        try:
            display_menu()
            choice = get_user_choice()

            if choice == "1":
                add_task_command(service)
            elif choice == "2":
                view_tasks_command(service)
            elif choice == "3":
                update_task_command(service)
            elif choice == "4":
                delete_task_command(service)
            elif choice == "5":
                toggle_task_command(service)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
