import sqlite3

from typing import Iterable, Union

from app.constants import DATA_FILE_PATH


class Database:
    """
    The database class with sqlite3 engine
    """

    def __init__(self, path=DATA_FILE_PATH):
        """
        Initialize the Database object.
        :param path: Path to the SQLite database file.
        """
        self.path = path
        self.connection = sqlite3.connect(self.path)

        self.create_users_table()

    def execute(
            self,
            sql: str,
            parameters: tuple = (),
            fetchone: bool = False,
            fetchall: bool = False,
            commit: bool = False,
    ) -> Union[Iterable, None]:
        """
        Execute an SQL statement.
        :param sql: SQL statement to execute.
        :param parameters: Parameters for the SQL statement.
        :param fetchone: Whether to fetch only one result.
        :param fetchall: Whether to fetch all results.
        :param commit: Whether to commit changes to the database.
        :return: Fetched data or None.
        """
        cursor = self.connection.cursor()
        cursor.execute(sql, parameters)

        if commit:
            self.connection.commit()

        data = None
        if fetchone and fetchall:
            raise ValueError("The `fetchone` or the `fetchall` should be either True.")
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        """
        Format SQL query and parameters for searching.
        :param sql: SQL query.
        :param parameters: Parameters for the query.
        :return: Formatted SQL query and parameters.
        """
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def create_users_table(self):
        """
        Create the Users table if it doesn't exist.
        """
        sql = """
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT,
                organization_name TEXT,
                work_phone TEXT,
                mobile_phone TEXT
            );
        """
        self.execute(sql, commit=True)

    def select_all_users(self):
        """
        Select all users from the Users table.
        :return: All users.
        """
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_a_user(self, user_id: int):
        """
        Select a user by ID from the Users table.
        :param user_id: ID of the user to select.
        :return: Selected user.
        """
        sql = "SELECT * FROM Users WHERE id = ?"
        return self.execute(sql, (user_id,), fetchone=True)

    def add_user(
            self,
            first_name: str = "",
            last_name: str = "",
            middle_name: str = "",
            organization_name: str = "",
            work_phone: str = "",
            mobile_phone: str = "",
    ):
        """
        Add a new user to the Users table.
        :param first_name: First name of the user.
        :param last_name: Last name of the user.
        :param middle_name: Middle name of the user.
        :param organization_name: Organization name of the user.
        :param work_phone: Work phone number of the user.
        :param mobile_phone: Mobile phone number of the user.
        """
        sql = """
            INSERT INTO Users (
                first_name, last_name, middle_name, organization_name, work_phone, mobile_phone
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        parameters = (first_name, last_name, middle_name, organization_name, work_phone, mobile_phone)
        self.execute(sql, parameters, commit=True)

    def edit_user(self, user_id: int, **kwargs):
        """
        Edit a user in the Users table.
        :param user_id: ID of the user to edit.
        :param kwargs: Updated user information.
        """
        sql = "UPDATE Users SET "
        sql, parameters = self.format_args(sql, kwargs)
        sql += " WHERE id = ?"
        parameters += (user_id,)
        self.execute(sql, parameters, commit=True)

    def search_users(self, criteria: dict) -> Union[Iterable, None]:
        """
        Search for users based on multiple criteria.
        :param criteria: A dictionary containing the search criteria.
        :return: A list of users matching the criteria.
        """
        sql = "SELECT * FROM Users WHERE "
        conditions = []
        values = []

        for field, value in criteria.items():
            conditions.append(f"{field} LIKE ?")
            values.append(f"%{value}%")

        sql += " AND ".join(conditions)
        return self.execute(sql, tuple(values), fetchall=True)


db = Database()
