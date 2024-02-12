from prompt_toolkit import shortcuts, formatted_text

from app.constants import TASKS, session, DEFAULT_ASK_TASK_ID_MESSAGE
from app.pages import show_list, add_item, edit_item, search_items
from app.utils import print_window_title


def main():
    """
    Main function to run the application.
    """
    while True:
        shortcuts.clear()
        print_window_title("Main page")

        for index, task in enumerate(TASKS.values(), start=1):
            print(f"{index}. {task}")

        task_id = session.prompt(
            formatted_text.HTML(DEFAULT_ASK_TASK_ID_MESSAGE)
        )

        if task_id == "q":
            shortcuts.clear()
            break

        try:
            task_id = int(task_id)
        except ValueError:
            continue

        if task_id not in range(1, len(TASKS.values()) + 1):
            continue

        shortcuts.clear()

        print_window_title(list(TASKS.values())[task_id - 1])

        if task_id == 1:
            message = show_list(session)
            if message:
                print(message)
                yes_no = input("Do you want to back? (yes/no): ")
                if yes_no != "yes":
                    break
        elif task_id == 2:
            add_item()
        elif task_id == 3:
            edit_item()
        elif task_id == 4:
            search_items(session)


if __name__ == "__main__":
    main()
