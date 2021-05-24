import sqlite3

from data import sql_commands

DB_NAME = "user_register_app"


class MethodsDb:
    """
    Class implement database methods
    """

    def __init__(self):
        self.conn = None

    def start_conn(self):
        """
        Start database connection and create database if it does not exist

        Returns
        -------
        None
        """
        self.conn = sqlite3.connect(DB_NAME)

    def close_conn(self):
        """
        Close database connection
        Returns
        -------
        None
        """
        self.conn.close()

    def check_exist_tables(self):
        """
        Ger exist table names

        Returns
        -------
        list: table names
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_commands.SELECT_TABLE_NAMES)
        return cursor.fetchall()

    def create_tables(self):
        """
        Create user table if it does not exist

        Returns
        -------
        None
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_commands.SELECT_TABLE_NAMES)
        tables = []
        for table in cursor.fetchall():
            tables.append(table[0])

        if 'users' not in tables:
            self.create_table_users(cursor)

    def create_table_users(self, cursor):
        """
        Create tables

        Parameters
        ----------
        cursor : Connection cursor

        Returns
        -------
        None
        """
        cursor.execute(sql_commands.CREATE_USER_TABLE)

    def inset_user(
            self, name:str, birth_date:str, cpf:str, cep:str, type_location:str,
            street_location:str, number:str, complement:str, district:str,
            city:str, state:str, email:str, cursor:str
    ):
        """
        Insert user in database

        Parameters
        ----------
        name : User name
        birth_date : User birth date
        cpf : User CPF
        cep : User CEP
        type_location : User type localtion
        street_location : User street location name
        number : User address number
        complement : Addressc complement
        district : User district name
        city : User city name
        state : User UF
        email : User e-mail
        cursor : Connection cursor

        Returns
        -------
        bool: successful insertion or not
        """
        sql_command = (sql_commands.INSERT_USER % (name, birth_date,
                       cpf, cep, type_location, street_location, number,
                       complement, district, city, state, email))
        try:
            cursor.execute(sql_command)
            return True
        except sqlite3.IntegrityError as er:
            print(f"ERROR: {er}.")
            return False


