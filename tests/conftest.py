"""Pytest configuration and fixtures."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_cursor():
    """Create a mock database cursor."""
    return Mock()


@pytest.fixture
def sample_field():
    """Sample field name for testing."""
    return "username"


@pytest.fixture
def sample_table():
    """Sample table name for testing."""
    return "users"


@pytest.fixture
def sample_where():
    """Sample WHERE clause for testing."""
    return "id=1"


@pytest.fixture
def default_iters():
    """Default iteration count for testing."""
    return 500000


@pytest.fixture
def default_sensitivity():
    """Default sensitivity threshold for testing."""
    return 100
