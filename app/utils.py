from typing import Union

from prompt_toolkit import PromptSession, formatted_text, shortcuts

from app.constants import FIELD_NAMES


def ask_user_data(print_text: str) -> Union[dict, str]:
    """
    Ask the user for data input.
    :param print_text: Text to print before asking for input.
    :return: A dictionary containing user data or 'q' if the user quits.
    """
    user_data = {}

    print(print_text)

    for field in FIELD_NAMES:
        field_input = input(f"{field.title()}: ")
        if field_input == "q":
            user_data = "q"
            break
        user_data[field] = field_input

    if isinstance(user_data, str):
        return user_data

    return {k: v for k, v in user_data.items() if v}


def paginate_data(session: PromptSession, data: Union[list, tuple], page_size=10):
    """
    Paginate and display data to the user.
    :param session: Prompt session for pagination.
    :param data: Data to paginate and display.
    :param page_size: Number of items per page.
    """
    num_pages = (len(data) + page_size - 1) // page_size
    current_page = 0

    while True:
        shortcuts.clear()
        print_data = data[current_page * page_size: (current_page + 1) * page_size]

        for item in print_data:
            print(item)

        page_text = (f"<i>Page {current_page + 1} of {num_pages}. "
                     f"Press q to quit, n for next page, p for previous page: </i>")
        user_input = session.prompt(formatted_text.HTML(page_text))

        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'n':
            current_page = min(current_page + 1, num_pages - 1)
        elif user_input.lower() == 'p':
            current_page = max(current_page - 1, 0)


def print_window_title(text: str):
    """
    Print a window title with equal signs above and below.
    :param text: Text to display in the window title.
    """
    print("=" * 15, text, "=" * 15)


def make_full_name(user):
    """
    Generate a full name from user data.
    :param user: User data containing first name, last name, and middle name.
    :return: The full name generated from the user data.
    """
    return f"{user[1].strip()} {user[2].strip()} {user[3].strip()}".strip()
