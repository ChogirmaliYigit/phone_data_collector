from prompt_toolkit import PromptSession, shortcuts

from app.constants import USER_DETAIL_TEXT
from app.db import db
from app.utils import paginate_data, make_full_name, ask_user_data


def show_list(session: PromptSession):
    """
    Show the list of users.
    :param session: Prompt session for pagination.
    """
    data = db.select_all_users()
    result = [
        USER_DETAIL_TEXT.format(
            user_id=user[0],
            full_name=make_full_name(user),
            organization_name=user[4],
            work_phone=user[5],
            mobile_phone=user[6]
        ).strip()
        for user in data
    ]

    if result:
        paginate_data(session, result)

    else:
        return "There is no data to display."


def add_item():
    """
    Add a new user to the database.
    """
    while True:
        shortcuts.clear()
        user_data = ask_user_data("Enter the following information about user to create (Press q to quit)")

        if user_data == "q":
            break

        if isinstance(user_data, dict) and user_data:
            db.add_user(**user_data)


def edit_item():
    """
    Edit an existing user in the database.
    """
    while True:
        user_id = input("Enter the ID of the user whose information you want to update (Press q to quit): ")
        if user_id == "q":
            shortcuts.clear()
            break

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            continue

        user = db.select_a_user(user_id)
        if not user:
            shortcuts.clear()
            print("User not found, try again.")
            continue

        print("Current user data:")
        print(
            USER_DETAIL_TEXT.format(
                user_id=user[0],
                full_name=make_full_name(user),
                organization_name=user[4],
                work_phone=user[5],
                mobile_phone=user[6]
            ).strip()
        )

        user_data = ask_user_data("Enter new information about user to update. "
                                  "If you do not want to change any fields, please leave them blank! (Press q to quit)")

        if user_data == "q":
            break

        if isinstance(user_data, dict) and user_data:
            db.edit_user(user[0], **user_data)
        shortcuts.clear()


def search_items(session: PromptSession):
    """
    Search for users based on provided criteria.
    :param session: Prompt session for pagination.
    """
    while True:
        user_data = ask_user_data("Only enter the necessary information about user to search! (Press q to quit)")

        if user_data == "q":
            break

        if isinstance(user_data, dict) and user_data:
            result = [
                USER_DETAIL_TEXT.format(
                    user_id=user[0],
                    full_name=make_full_name(user),
                    organization_name=user[4],
                    work_phone=user[5],
                    mobile_phone=user[6]
                ).strip()
                for user in db.search_users(user_data)
            ]
            paginate_data(session, result)
            shortcuts.clear()
        else:
            shortcuts.clear()
            print("Users not found by your search, try again.")
