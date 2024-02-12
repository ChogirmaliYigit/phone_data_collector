from prompt_toolkit import PromptSession

# Tasks available in the application
TASKS = {
    "show_list": "Show the list of contacts",
    "add_item": "Add a new contact",
    "edit_item": "Edit an existing contact",
    "search_items": "Search for contacts",
}

# Default message for asking task ID
DEFAULT_ASK_TASK_ID_MESSAGE = "Enter the ID of a task (<i>Press q to quit</i>): "

# Field names for user details
FIELD_NAMES = ["first_name", "last_name", "middle_name", "organization_name", "work_phone", "mobile_phone"]

# Text format for displaying user details
USER_DETAIL_TEXT = ("ID - {user_id}:\n\tFull name: {full_name}\n\tOrganization name: {organization_name}"
                    "\n\tWork phone number: {work_phone}\n\tMobile phone number: {mobile_phone}")

# Path to the data file (SQLite database)
DATA_FILE_PATH = "main.db"

# Initialize a prompt session for user input
session = PromptSession()
