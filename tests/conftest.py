import json
import os
from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession


RESOURCE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "test_data",
)


@pytest.fixture
def mock_session():
    """Mocks aiohttp.ClientSession."""
    session_mock = AsyncMock(spec=ClientSession)
    session_mock.get = AsyncMock()
    return session_mock


@pytest.fixture
def mock_api_response():
    """Returns function which mocks API response."""

    def _mock_api_response(mock_response, mock_session, status=200):
        # Mocks .get()
        mock_response_obj = AsyncMock()
        mock_response_obj.status = status
        mock_response_obj.json.return_value = mock_response
        mock_session.get.return_value = mock_response_obj

    return _mock_api_response


@pytest.fixture
def get_test_data():
    """Returns function which reads test data from file."""

    def get_file_content(file):
        abs_file = os.path.join(RESOURCE_DIR, file)
        with open(abs_file, "r") as f:
            content = f.read()
        return json.loads(content)

    return get_file_content
