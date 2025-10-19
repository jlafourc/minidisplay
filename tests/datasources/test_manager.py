"""
Unit tests for the data-source abstraction layer.
"""

import os
import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class MockNob:
    def __init__(self, data):
        self.data = data

    def find(self, path):
        value = self.data.get(path)
        if isinstance(value, dict):
            return MockNob(value)
        return value

    def __getitem__(self, key):
        return self.data[key]

    def __bool__(self):
        return bool(self.data)

    def __getattr__(self, item):
        value = self.data.get(item)
        if isinstance(value, dict):
            return MockNob(value)
        return value


sys.modules.setdefault("nob", type("MockNobModule", (), {"Nob": MockNob})())

from minidisplay.datasources import (  # noqa: E402  - depends on mocked module
    DataSource,
    DataSourceManager,
    IdelisTransportSource,
)


class SampleDataSource(DataSource):
    def fetch_data(self):
        return MockNob({"test": "data"})

    def is_available(self):
        return True

    def get_refresh_interval(self):
        return 60


class TestDataSourceBase(unittest.TestCase):
    def test_data_source_initialization(self):
        config = {"test": "value"}
        source = SampleDataSource("Test Source", config)

        self.assertEqual(source.name, "Test Source")
        self.assertEqual(source.config, config)
        self.assertIsNone(source.last_error)
        self.assertIsNone(source.last_fetch_time)

    def test_data_source_error_handling(self):
        source = SampleDataSource("Test Source", {})

        source._set_error("Test error")
        self.assertEqual(source.last_error, "Test error")

        source._clear_error()
        self.assertIsNone(source.last_error)

    def test_data_source_timestamp_handling(self):
        source = SampleDataSource("Test Source", {})
        timestamp = 1234567890.0

        source._set_last_fetch_time(timestamp)
        self.assertEqual(source.last_fetch_time, timestamp)


class TestIdelisTransportSource(unittest.TestCase):
    def setUp(self):
        self.config = {
            "api_url": "https://api.idelis.fr/GetStopMonitoring",
            "api_code": "LAGUTS_1",
            "api_ligne": "5",
            "api_next": 3,
        }
        self.source = IdelisTransportSource(self.config)

    def test_idelis_source_initialization(self):
        self.assertEqual(self.source.name, "Idelis Transport")
        self.assertEqual(self.source.api_url, self.config["api_url"])
        self.assertEqual(self.source.api_code, self.config["api_code"])
        self.assertEqual(self.source.api_ligne, self.config["api_ligne"])
        self.assertEqual(self.source.api_next, self.config["api_next"])

    def test_idelis_source_availability_with_token(self):
        with patch.dict(os.environ, {"IDELIS_API_TOKEN": "test_token"}):
            self.assertTrue(self.source.is_available())

    def test_idelis_source_availability_without_token(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(self.source.is_available())

    def test_idelis_source_refresh_interval(self):
        self.assertEqual(self.source.get_refresh_interval(), 60)

    def test_idelis_source_mock_data_generation(self):
        mock_time = datetime.now()
        mock_data = self.source.get_mock_data(mock_time)

        self.assertIsNotNone(mock_data)
        self.assertIsInstance(mock_data, MockNob)

    @patch("requests.request")
    def test_idelis_source_successful_fetch(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"passages": [{"arrivee": "14:30"}]}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        with patch.dict(os.environ, {"IDELIS_API_TOKEN": "test_token"}):
            result = self.source.fetch_data()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, MockNob)
        self.assertIsNone(self.source.last_error)

    def test_idelis_source_error_handling(self):
        self.source._set_error("Test error")
        self.assertEqual(self.source.last_error, "Test error")

        self.source._clear_error()
        self.assertIsNone(self.source.last_error)


class TestDataSourceManager(unittest.TestCase):
    def setUp(self):
        self.config = {
            "api_url": "https://api.idelis.fr/GetStopMonitoring",
            "api_code": "LAGUTS_1",
            "api_ligne": "5",
            "api_next": 3,
        }
        self.manager = DataSourceManager(self.config)

    def test_manager_initialization(self):
        self.assertEqual(self.manager.config, self.config)
        self.assertEqual(len(self.manager.data_sources), 0)

    def test_manager_initializes_data_sources(self):
        self.manager.initialize_data_sources()

        self.assertEqual(len(self.manager.data_sources), 1)
        self.assertIn("idelis", self.manager.data_sources)
        self.assertIsInstance(self.manager.data_sources["idelis"], IdelisTransportSource)

    def test_manager_get_data_source(self):
        self.manager.initialize_data_sources()

        source = self.manager.get_data_source("idelis")
        self.assertIsNotNone(source)
        self.assertIsInstance(source, IdelisTransportSource)

        self.assertIsNone(self.manager.get_data_source("nonexistent"))

    def test_manager_get_available_sources(self):
        self.manager.initialize_data_sources()

        with patch.dict(os.environ, {"IDELIS_API_TOKEN": "test_token"}):
            available = self.manager.get_available_sources()
            self.assertIn("idelis", available)

    def test_manager_get_status(self):
        self.manager.initialize_data_sources()
        with patch.dict(os.environ, {"IDELIS_API_TOKEN": "test_token"}):
            status = self.manager.get_status()

        self.assertEqual(status["total_sources"], 1)
        self.assertIn("idelis", status["sources"])

    def test_manager_fetch_from_source(self):
        self.manager.initialize_data_sources()

        with patch.object(
            IdelisTransportSource,
            "is_available",
            return_value=True,
        ), patch.object(
            IdelisTransportSource,
            "fetch_data",
            return_value=MockNob({"passages": []}),
        ):
            data = self.manager.fetch_from_source("idelis")
            self.assertIsNotNone(data)

    def test_manager_fetch_primary_data(self):
        self.manager.initialize_data_sources()

        with patch.object(
            IdelisTransportSource,
            "is_available",
            return_value=True,
        ), patch.object(
            IdelisTransportSource,
            "fetch_data",
            return_value=MockNob({"passages": []}),
        ):
            self.assertIsNotNone(self.manager.fetch_primary_data())

    def test_manager_get_mock_data(self):
        self.manager.initialize_data_sources()
        mock_time = datetime.now()

        with patch.object(
            IdelisTransportSource,
            "get_mock_data",
            return_value=MockNob({"passages": []}),
        ):
            data = self.manager.get_mock_data("idelis", mock_time)
            self.assertIsNotNone(data)
