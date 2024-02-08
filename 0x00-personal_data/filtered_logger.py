#!/usr/bin/env python3
"""
Script for handling Personal Data
"""

from typing import List
import re
import logging
from os import environ
import mysql.connector


# redacted fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """


    Keyword arguments:
    argument -- description
    Return: return_description
    """

    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Returns a Logger object for handling Personal Data
    """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False

    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    log.addHandler(stream)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    mysql connection object
    """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(user=username,
                                                            password=password,
                                                            host=host,
                                                            database=db_name)
    return connection


def main():
    """
    Main function to retrieve user data from database and print to the console
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users;")
    field_name = [i[0] for i in cur.description]

    log = get_logger()

    for row in cur:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_name))
        log.info(str_row.strip())

    cur.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for filtering PII fields
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
       constructor
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified log record as text.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
