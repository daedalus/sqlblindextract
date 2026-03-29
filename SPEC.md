# SPEC.md — sqlblindextract

## Purpose

A tool for extracting data from SQL databases using blind injection timing-based techniques. It measures query execution time differences to infer data values bit by bit.

## Scope

### In Scope
- Blind SQL injection data extraction via timing attacks
- Bit-by-bit character extraction from database fields
- Length detection of field values
- Configurable timing sensitivity and iteration count
- Support for MySQL databases via MySQLdb

### Not In Scope
- Web application scanning
- Automated SQL injection vulnerability detection
- Other database backends (PostgreSQL, SQLite, etc.)
- Defense/mitigation tools

## Public API / Interface

### CLI Entry Point
```
sqlblindextract --host HOST --user USER --password PASSWD --db DATABASE --table TABLE --field FIELD --where WHERE
```

### Core Functions

#### `measure(cursor, sql: str) -> float`
- Executes a SQL query and returns execution time in seconds
- Preconditions: cursor must be valid, SQL must be a string
- Error behavior: Raises exception if query fails

#### `getlength(cursor, field: str, table: str, where: str, iters: int, sensitivity: int) -> int`
- Returns the length of a field value using blind injection
- Preconditions: field, table, where must be valid SQL identifiers/conditions
- Error behavior: Raises exception on SQL errors

#### `getbits(cursor, pos: int, field: str, table: str, where: str, iters: int, sensitivity: int) -> int`
- Extracts a single character's bitmask at given position
- Preconditions: pos >= 1, valid field/table/where
- Error behavior: Raises exception on SQL errors

#### `getdata(cursor, field: str, table: str, where: str, iters: int, sensitivity: int) -> str`
- Extracts the complete value from a field
- Preconditions: valid field, table, where conditions
- Error behavior: Raises exception on SQL errors

### CLI Options
- `--host`, `-h`: Database host (default: localhost)
- `--user`, `-u`: Database user
- `--password`, `-p`: Database password
- `--db`, `-d`: Database name
- `--table`, `-t`: Table name
- `--field`, `-f`: Field name to extract
- `--where`, `-w`: WHERE clause condition
- `--iters`: Number of benchmark iterations (default: 500000)
- `--sensitivity`: Time sensitivity threshold (default: 100)

## Data Formats

### Input
- Database connection parameters (host, user, password, db)
- Table and field names
- WHERE clause condition string

### Output
- Extracted string value from the target field

## Edge Cases

1. **Empty result set**: WHERE clause matches no rows - should handle gracefully
2. **NULL values**: Field contains NULL - should return empty string
3. **Very long strings**: Field value exceeds reasonable length - limit to 1000 chars
4. **Special characters**: Field contains special/chinese/unicode characters - handle via UTF-8
5. **Connection timeout**: Database connection fails - raise descriptive exception
6. **Very short execution times**: Query too fast to measure reliably - warn user
7. **Permission denied**: User lacks SELECT permission - raise descriptive error

## Performance & Constraints

- Time complexity: O(n * m) where n = string length, m = bits per character
- Default iterations: 500,000 (configurable)
- Maximum extractable length: 1000 characters
- Requires MySQL database with BENCHMARK() function support
- Only works with MySQL databases

