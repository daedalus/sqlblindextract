"""Tests for sqlblindextract CLI module."""

import sys
from unittest.mock import Mock, patch

from click.testing import CliRunner


class MockMySQLdb:
    """Mock MySQLdb module."""

    class Error(Exception):
        """Mock MySQLdb Error."""


mock_mysqldb = MockMySQLdb()
mock_mysqldb.connect = Mock()


sys.modules["MySQLdb"] = mock_mysqldb

from sqlblindextract.cli import main


class TestCLI:
    """Tests for the CLI interface."""

    def test_main_help(self):
        """Test that CLI help works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Extract data from SQL database" in result.output

    def test_main_missing_required_args(self):
        """Test that CLI fails when required arguments are missing."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        assert result.exit_code == 2

    @patch("sqlblindextract.cli.MySQLdb.connect")
    @patch("sqlblindextract.cli.getdata")
    def test_main_successful_extraction(self, mock_getdata, mock_connect):
        """Test successful data extraction."""
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_getdata.return_value = "test_value"

        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "-u",
                "testuser",
                "-p",
                "testpass",
                "-d",
                "testdb",
                "-t",
                "testtable",
                "-f",
                "testfield",
                "-w",
                "id=1",
            ],
        )

        assert result.exit_code == 0
        assert "RECOVERED DATA: test_value" in result.output

    @patch("sqlblindextract.cli.MySQLdb.connect")
    def test_main_connection_failure(self, mock_connect):
        """Test handling of connection failure."""
        from MySQLdb import Error as MySQLError

        mock_connect.side_effect = MySQLError(2003, "Can't connect")

        runner = CliRunner()
        result = runner.invoke(
            main,
            [
                "-u",
                "testuser",
                "-p",
                "testpass",
                "-d",
                "testdb",
                "-t",
                "testtable",
                "-f",
                "testfield",
                "-w",
                "id=1",
            ],
        )

        assert result.exit_code == 1
        assert "Error: Failed to connect to database" in result.output
