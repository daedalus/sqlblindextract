# sqlblindextract

> A tool for blind SQL injection data extraction using timing-based techniques.

[![PyPI](https://img.shields.io/pypi/v/sqlblindextract.svg)](https://pypi.org/project/sqlblindextract/)
[![Python](https://img.shields.io/pypi/pyversions/sqlblindextract.svg)](https://pypi.org/project/sqlblindextract/)
[![Coverage](https://codecov.io/gh/daedalus/sqlblindextract/branch/main/graph/badge.svg)](https://codecov.io/gh/daedalus/sqlblindextract)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install sqlblindextract
```

## Usage

```python
import MySQLdb
from sqlblindextract import getdata

db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="mysql")
cursor = db.cursor()

result = getdata(cursor, "password", "user", "user='root' limit 1")
print(result)
```

## CLI

```bash
sqlblindextract --help
```

```
Usage: sqlblindextract [OPTIONS]

  Extract data from SQL database using blind injection timing techniques.

Options:
  -h, --host TEXT        Database host (default: localhost)
  -u, --user TEXT        Database user  [required]
  -p, --password TEXT    Database password  [required]
  -d, --db TEXT          Database name  [required]
  -t, --table TEXT       Table name  [required]
  -f, --field TEXT       Field name to extract  [required]
  -w, --where TEXT       WHERE clause condition  [required]
  --iters INTEGER        Number of benchmark iterations (default: 500000)
  --sensitivity INTEGER  Time sensitivity threshold (default: 100)
  --help                 Show this message and exit.
```

## API

### `measure(cursor, sql: str) -> float`

Execute a SQL query and return execution time in seconds.

### `getlength(cursor, field: str, table: str, where: str, iters: int = 500000, sensitivity: int = 100) -> int`

Extract the length of a field value using blind injection timing.

### `getbits(cursor, pos: int, field: str, table: str, where: str, iters: int = 500000, sensitivity: int = 100) -> int`

Extract a single character's bitmask at given position.

### `getdata(cursor, field: str, table: str, where: str, iters: int = 500000, sensitivity: int = 100, max_length: int = 1000) -> str`

Extract the complete value from a field using blind injection.

## Development

```bash
git clone https://github.com/daedalus/sqlblindextract.git
cd sqlblindextract
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

