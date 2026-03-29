"""Command-line interface for sqlblindextract."""

import click
import MySQLdb  # type: ignore[import-untyped]

from sqlblindextract.core import getdata


@click.command()
@click.option(
    "--host",
    "-h",
    default="localhost",
    help="Database host (default: localhost)",
)
@click.option(
    "--user",
    "-u",
    required=True,
    help="Database user",
)
@click.option(
    "--password",
    "-p",
    required=True,
    help="Database password",
)
@click.option(
    "--db",
    "-d",
    required=True,
    help="Database name",
)
@click.option(
    "--table",
    "-t",
    required=True,
    help="Table name",
)
@click.option(
    "--field",
    "-f",
    required=True,
    help="Field name to extract",
)
@click.option(
    "--where",
    "-w",
    "where_clause",
    required=True,
    help="WHERE clause condition",
)
@click.option(
    "--iters",
    default=500000,
    type=int,
    help="Number of benchmark iterations (default: 500000)",
)
@click.option(
    "--sensitivity",
    default=100,
    type=int,
    help="Time sensitivity threshold (default: 100)",
)
def main(
    host: str,
    user: str,
    password: str,
    db: str,
    table: str,
    field: str,
    where_clause: str,
    iters: int,
    sensitivity: int,
) -> int:
    """Extract data from SQL database using blind injection timing techniques.

    This tool measures query execution time differences to infer data values
    bit by bit through timing-based blind SQL injection.

    Example:
        sqlblindextract -u root -p password -d mysql -t user -f password -w "user='root' limit 1"
    """
    try:
        connection = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=db,
        )
    except MySQLdb.Error as e:
        click.echo(f"Error: Failed to connect to database: {e}", err=True)
        return 1

    try:
        cursor = connection.cursor()

        click.echo(f"Extracting {field} from {table} where {where_clause}...")
        click.echo(f"Using iters={iters}, sensitivity={sensitivity}")

        result = getdata(
            cursor=cursor,
            field=field,
            table=table,
            where=where_clause,
            iters=iters,
            sensitivity=sensitivity,
        )

        click.echo(f"RECOVERED DATA: {result}")

        return 0

    except MySQLdb.Error as e:
        click.echo(f"Error: Database error: {e}", err=True)
        return 1
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    finally:
        connection.close()
