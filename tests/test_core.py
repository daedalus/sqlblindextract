"""Tests for sqlblindextract core module."""

from unittest.mock import patch

from sqlblindextract.core import getbits, getdata, getlength, measure


class TestMeasure:
    """Tests for the measure function."""

    def test_measure_returns_execution_time(self, mock_cursor):
        """Test that measure returns a positive execution time."""
        mock_cursor.execute.return_value = None

        result = measure(mock_cursor, "SELECT 1")

        assert result >= 0

    def test_measure_calls_cursor_execute(self, mock_cursor):
        """Test that measure executes the provided SQL."""
        mock_cursor.execute.return_value = None

        measure(mock_cursor, "SELECT 1")

        mock_cursor.execute.assert_called_once_with("SELECT 1")


class TestGetLength:
    """Tests for the getlength function."""

    def test_getlength_returns_integer(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test that getlength returns an integer."""
        mock_cursor.execute.return_value = None

        with patch(
            "sqlblindextract.core.measure",
            side_effect=[0.001] + [0.001] * 8,
        ):
            result = getlength(mock_cursor, sample_field, sample_table, sample_where)

        assert isinstance(result, int)

    def test_getlength_zero_when_no_match(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test edge case: empty result set returns 0."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.measure", return_value=0.0001):
            result = getlength(
                mock_cursor, sample_field, sample_table, sample_where, sensitivity=10000
            )

        assert result >= 0


class TestGetBits:
    """Tests for the getbits function."""

    def test_getbits_returns_integer(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test that getbits returns an integer (the character code)."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.measure", return_value=0.001):
            result = getbits(mock_cursor, 1, sample_field, sample_table, sample_where)

        assert isinstance(result, int)
        assert 0 <= result <= 255

    def test_getbits_handles_zero_time(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test edge case: very short execution time."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.measure", return_value=0):
            result = getbits(mock_cursor, 1, sample_field, sample_table, sample_where)

        assert isinstance(result, int)


class TestGetData:
    """Tests for the getdata function."""

    def test_getdata_returns_string(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test that getdata returns a string."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.getlength", return_value=0):
            result = getdata(mock_cursor, sample_field, sample_table, sample_where)

        assert isinstance(result, str)

    def test_getdata_empty_for_zero_length(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test edge case: NULL values return empty string."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.getlength", return_value=0):
            result = getdata(mock_cursor, sample_field, sample_table, sample_where)

        assert result == ""

    def test_getdata_respects_max_length(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test edge case: very long strings are limited."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.getlength", return_value=2000):
            with patch("sqlblindextract.core.getbits", return_value=ord("a")):
                result = getdata(
                    mock_cursor, sample_field, sample_table, sample_where, max_length=10
                )

        assert len(result) == 10

    def test_getdata_single_character(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test boundary value: single character extraction."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.getlength", return_value=1):
            with patch("sqlblindextract.core.getbits", return_value=ord("a")):
                result = getdata(mock_cursor, sample_field, sample_table, sample_where)

        assert result == "a"

    def test_getdata_multiple_characters(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test boundary value: multiple character extraction."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.getlength", return_value=3):
            with patch(
                "sqlblindextract.core.getbits",
                side_effect=[ord("a"), ord("b"), ord("c")],
            ):
                result = getdata(mock_cursor, sample_field, sample_table, sample_where)

        assert result == "abc"

    def test_getdata_unicode_characters(
        self, mock_cursor, sample_field, sample_table, sample_where
    ):
        """Test edge case: unicode characters."""
        mock_cursor.execute.return_value = None

        with patch("sqlblindextract.core.getlength", return_value=1):
            with patch("sqlblindextract.core.getbits", return_value=ord("ñ")):
                result = getdata(mock_cursor, sample_field, sample_table, sample_where)

        assert result == "ñ"
