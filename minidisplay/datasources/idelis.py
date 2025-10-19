"""
Idelis Transport Data Source

This module implements the IdelisTransportSource class that fetches bus arrival
data from the Idelis API, refactoring the original fetch_arrival_data function
to work with the new DataSource abstraction layer.
"""

import json
import os
import time
import requests
from typing import Optional, Dict, Any
from nob import Nob

from .base import DataSource


class IdelisTransportSource(DataSource):
    """
    Data source for Idelis public transport API.

    This class refactors the original fetch_arrival_data function to implement
    the DataSource interface, maintaining exactly the same behavior and error
    handling patterns as the original implementation.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Idelis transport data source.

        Args:
            config: Configuration dictionary containing Idelis API parameters:
                - api_url: The Idelis API endpoint URL
                - api_code: The stop code for the bus stop
                - api_ligne: The bus line number
                - api_next: Number of next passages to fetch
        """
        super().__init__("Idelis Transport", config)
        self.api_url = config.get("api_url")
        self.api_code = config.get("api_code")
        self.api_ligne = config.get("api_ligne")
        self.api_next = config.get("api_next", 3)

    def fetch_data(self) -> Optional[Nob]:
        """
        Fetch arrival data from the Idelis API.

        Returns:
            Nob object containing the fetched data, or None if fetching failed
            following the exact same error handling pattern as the original
            fetch_arrival_data function.

        Note:
            This method implements the same error handling pattern as the original:
            try:
                # API call with same parameters
                response = requests.request(...)
                return Nob(response.json())
            except requests.RequestException as e:
                print(f"Error fetching data from API: {e}")
                return None
        """
        # Clear previous errors
        self._clear_error()

        # Check for API token (same as original)
        api_token = os.getenv("IDELIS_API_TOKEN")
        if not api_token:
            error_msg = "IDELIS_API_TOKEN environment variable not set."
            self._set_error(error_msg)
            # Note: Original function exits here, but we return None for consistency
            return None

        try:
            # Exact same API call as original fetch_arrival_data function
            response = requests.request(
                method='get',
                url=self.api_url,
                data=json.dumps({
                    "code": self.api_code,
                    "ligne": self.api_ligne,
                    "next": self.api_next
                }),
                headers={'X-Auth-Token': api_token}
            )
            response.raise_for_status()

            # Record successful fetch time
            self._set_last_fetch_time(time.time())

            # Return Nob object (same as original)
            return Nob(response.json())

        except requests.RequestException as e:
            # Exact same error handling as original
            error_msg = f"Error fetching data from API: {e}"
            self._set_error(error_msg)
            return None

    def is_available(self) -> bool:
        """
        Check if the Idelis data source is available.

        Returns:
            True if API token is set and API URL is configured, False otherwise
        """
        has_token = bool(os.getenv("IDELIS_API_TOKEN"))
        has_config = bool(self.api_url and self.api_code and self.api_ligne)
        return has_token and has_config

    def get_refresh_interval(self) -> int:
        """
        Get the recommended refresh interval for Idelis data.

        Returns:
            60 seconds - bus arrival data changes frequently
        """
        return 60

    def get_mock_data(self, mock_time) -> Optional[Nob]:
        """
        Generate mock data for testing purposes.

        This replicates the original fetch_mock_arrival_data function behavior
        to maintain compatibility with existing testing workflows.

        Args:
            mock_time: datetime object to use for generating mock data

        Returns:
            Nob object containing mock data, or None if generation failed
        """
        try:
            import datetime
            mock_passages = []
            for i in range(3):
                mock_time_obj = (mock_time + datetime.timedelta(minutes=10 * (i + 1))).time()
                mock_passages.append({"arrivee": mock_time_obj.strftime("%H:%M")})
            return Nob({"passages": mock_passages})
        except Exception as e:
            error_msg = f"Error generating mock data: {e}"
            self._set_error(error_msg)
            return None