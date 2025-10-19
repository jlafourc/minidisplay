"""
Abstract Base Class for Data Sources

This module defines the DataSource abstract base class that all data sources
must implement to be compatible with the Mini Display system.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from nob import Nob


class DataSource(ABC):
    """
    Abstract base class for all data sources.

    This class defines the standard interface that all data sources must implement
    to be compatible with the Mini Display system. Each data source is responsible
    for fetching data from a specific provider and making it available in a
    standardized format.
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize the data source.

        Args:
            name: Human-readable name for this data source
            config: Configuration dictionary specific to this data source
        """
        self.name = name
        self.config = config
        self._last_error: Optional[str] = None
        self._last_fetch_time: Optional[float] = None

    @abstractmethod
    def fetch_data(self) -> Optional[Nob]:
        """
        Fetch data from the source.

        Returns:
            Nob object containing the fetched data, or None if fetching failed
            following the existing error handling pattern from the codebase.

        Note:
            This method should follow the existing error handling pattern:
            try:
                # API call or data processing
                response = ...
                return Nob(response.json())
            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
                return None
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the data source is currently available.

        Returns:
            True if the source is available, False otherwise
        """
        pass

    @abstractmethod
    def get_refresh_interval(self) -> int:
        """
        Get the recommended refresh interval in seconds.

        Returns:
            Number of seconds to wait between fetches
        """
        pass

    @property
    def last_error(self) -> Optional[str]:
        """
        Get the last error message from this data source.

        Returns:
            Last error message, or None if no error occurred
        """
        return self._last_error

    @property
    def last_fetch_time(self) -> Optional[float]:
        """
        Get the timestamp of the last successful fetch.

        Returns:
            Unix timestamp of last fetch, or None if no successful fetch
        """
        return self._last_fetch_time

    def _set_error(self, error_message: str) -> None:
        """
        Set the last error message.

        Args:
            error_message: Error message to store
        """
        self._last_error = error_message
        print(f"DataSource {self.name}: {error_message}")

    def _clear_error(self) -> None:
        """Clear the last error message."""
        self._last_error = None

    def _set_last_fetch_time(self, timestamp: float) -> None:
        """
        Set the timestamp of the last successful fetch.

        Args:
            timestamp: Unix timestamp
        """
        self._last_fetch_time = timestamp

    def __str__(self) -> str:
        """String representation of the data source."""
        return f"DataSource({self.name})"

    def __repr__(self) -> str:
        """Detailed string representation of the data source."""
        return f"DataSource(name='{self.name}', available={self.is_available()}, last_error={self.last_error})"