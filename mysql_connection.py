import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared

import secret_config


class MySQL:
    def __init__(self):
        self.cnx = mysql.connector.connect(user=secret_config.db_user, password=secret_config.db_password,
                                           host=secret_config.db_host, database=secret_config.db_name,
                                           use_pure=True)

    def query(self, query, params):
        cursor = self.cnx.cursor(cursor_class=MySQLCursorPrepared)
        cursor.execute(query, params)

        result = []
        try:
            result = cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            # no result
            pass

        cursor.close()
        # commit in case of changes
        self.cnx.commit()

        return result

    def close(self):
        self.cnx.close()
