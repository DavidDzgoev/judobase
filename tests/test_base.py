from unittest.mock import patch

import pytest
from aiohttp import ClientSession

from judobase import Competition, Contest, Country, CountryShort, Judoka
from judobase.base import BASE_URL, CompetitionAPI, ContestAPI, CountryAPI, JudokaAPI, _Base


class TestBase:
    """Test cases for the _Base class."""

    @pytest.mark.asyncio
    async def test_aenter_aexit(self):
        """Test that the context manager properly creates and closes the session."""
        async with _Base() as client:
            assert isinstance(client._session, ClientSession)
            assert not client._session.closed
        assert client._session.closed

        client = _Base()
        assert not client._session.closed
        await client.close_session()

        async with client:
            assert not client._session.closed
        assert client._session.closed

    @pytest.mark.asyncio
    async def test_get_json_success(self, mock_session, mock_api_response):
        """Test _get_json with a successful API response."""
        mock_api_response(mock_response={"data": "test_response"}, mock_session=mock_session)

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with _Base() as client:
                result = await client._get_json({"key": "value"})

                assert result == {"data": "test_response"}
                mock_session.get.assert_called_once_with(
                    f"{BASE_URL}get_json",
                    timeout=10,
                    params={"key": "value"},
                )

    @pytest.mark.asyncio
    async def test_get_json_failure(self, mock_session, mock_api_response):
        """Test _get_json with a successful API response."""
        mock_api_response(
            status=500, mock_response={"data": "test_response"}, mock_session=mock_session
        )

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with _Base() as client:
                with pytest.raises(ConnectionError):
                    await client._get_json({"key": "value"})


class TestCompetitionAPI:
    """Test cases for the Competition API class."""

    @pytest.mark.asyncio
    async def test_get_competition_list(self, mock_session, mock_api_response, get_test_data):
        """Test get_competition_list response."""
        test_data = get_test_data("get_competition_list.json")
        mock_api_response(mock_response=test_data["mock_response"], mock_session=mock_session)

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with CompetitionAPI() as client:
                result = await client.get_competition_list()
                assert result == [Competition(**comp) for comp in test_data["expected"]]

    @pytest.mark.asyncio
    async def test_get_competition_info(self, mock_session, mock_api_response, get_test_data):
        """Test get_competition_info response."""
        test_data = get_test_data("get_competition_info.json")
        mock_api_response(mock_response=test_data["mock_response"], mock_session=mock_session)

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with CompetitionAPI() as client:
                result = await client.get_competition_info("test_id")
                assert result == Competition(**test_data["expected"])


class TestContestAPI:
    """Test cases for the Contest API class."""

    @pytest.mark.asyncio
    async def test_find_contests(self, mock_session, mock_api_response, get_test_data):
        """Test find_contests response."""
        test_data = get_test_data("find_contests.json")
        mock_api_response(mock_response=test_data["mock_response"], mock_session=mock_session)

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with ContestAPI() as client:
                result = await client.find_contests()
                assert result == [Contest(**comp) for comp in test_data["expected"]]


class TestJudokaAPI:
    """Test cases for the Judoka API class."""

    @pytest.mark.asyncio
    async def test_get_judoka_info(self, mock_session, mock_api_response, get_test_data):
        """Test get_judoka_info response."""
        test_data = get_test_data("get_judoka_info.json")
        mock_api_response(mock_response=test_data["mock_response"], mock_session=mock_session)

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with JudokaAPI() as client:
                result = await client.get_judoka_info("test_id")
                assert result == Judoka(**test_data["expected"])


class TestCountryAPI:
    """Test cases for the Judoka API class."""

    @pytest.mark.asyncio
    async def test_get_country_info(self, mock_session, mock_api_response, get_test_data):
        """Test get_country_info response."""
        test_data = get_test_data("get_country_info.json")
        mock_api_response(mock_response=test_data["mock_response"], mock_session=mock_session)

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with CountryAPI() as client:
                result = await client.get_country_info("test_id")
                assert result == Country(**test_data["expected"])

    @pytest.mark.asyncio
    async def test_get_country_list(self, mock_session, mock_api_response, get_test_data):
        """Test get_country_list response."""
        test_data = get_test_data("get_country_list.json")
        mock_api_response(mock_response=test_data["mock_response"], mock_session=mock_session)

        with patch("judobase.base.ClientSession", return_value=mock_session):
            async with CountryAPI() as client:
                result = await client.get_country_list()
                assert result == [CountryShort(**country) for country in test_data["expected"]]
