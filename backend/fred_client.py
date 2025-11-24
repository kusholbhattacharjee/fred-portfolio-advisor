"""
FRED API Client - Handles all interactions with the Federal Reserve Economic Data API
"""
from fredapi import Fred
from datetime import datetime, timedelta
import pandas as pd
import config
from typing import Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FREDClient:
    """Wrapper for FRED API with caching and error handling"""

    def __init__(self, api_key: str = None):
        """Initialize FRED client with API key"""
        self.api_key = api_key or config.FRED_API_KEY
        if self.api_key == 'YOUR_API_KEY_HERE':
            raise ValueError(
                "Please set your FRED API key in config.py or .env file. "
                "Get your free API key at: https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        self.fred = Fred(api_key=self.api_key)
        self._cache = {}
        self._cache_time = {}

    def _is_cache_valid(self, series_id: str) -> bool:
        """Check if cached data is still valid"""
        if series_id not in self._cache_time:
            return False
        elapsed = (datetime.now() - self._cache_time[series_id]).total_seconds()
        return elapsed < config.CACHE_DURATION

    def get_series(self, series_id: str, observation_start: str = None,
                   observation_end: str = None) -> pd.Series:
        """
        Fetch a data series from FRED

        Args:
            series_id: FRED series identifier
            observation_start: Start date (YYYY-MM-DD)
            observation_end: End date (YYYY-MM-DD)

        Returns:
            Pandas Series with the data
        """
        cache_key = f"{series_id}_{observation_start}_{observation_end}"

        if self._is_cache_valid(cache_key):
            logger.info(f"Using cached data for {series_id}")
            return self._cache[cache_key]

        try:
            logger.info(f"Fetching {series_id} from FRED API")
            data = self.fred.get_series(
                series_id,
                observation_start=observation_start,
                observation_end=observation_end
            )
            self._cache[cache_key] = data
            self._cache_time[cache_key] = datetime.now()
            return data
        except Exception as e:
            logger.error(f"Error fetching {series_id}: {str(e)}")
            raise

    def get_latest_value(self, series_id: str) -> Optional[float]:
        """Get the most recent value for a series"""
        try:
            data = self.get_series(series_id)
            if data is not None and len(data) > 0:
                # Get the last non-null value
                return float(data.dropna().iloc[-1])
            return None
        except Exception as e:
            logger.error(f"Error getting latest value for {series_id}: {str(e)}")
            return None

    def get_series_info(self, series_id: str) -> Dict:
        """Get metadata about a series"""
        try:
            info = self.fred.get_series_info(series_id)
            return info.to_dict() if hasattr(info, 'to_dict') else info
        except Exception as e:
            logger.error(f"Error getting info for {series_id}: {str(e)}")
            return {}

    def get_recent_data(self, series_id: str, years: int = 2) -> pd.Series:
        """Get recent data for a series"""
        start_date = (datetime.now() - timedelta(days=365*years)).strftime('%Y-%m-%d')
        return self.get_series(series_id, observation_start=start_date)

    def get_all_indicators(self) -> Dict[str, float]:
        """Fetch all configured economic indicators"""
        indicators = {}
        for name, series_id in config.FRED_SERIES.items():
            try:
                value = self.get_latest_value(series_id)
                indicators[name] = value
                logger.info(f"{name}: {value}")
            except Exception as e:
                logger.error(f"Failed to fetch {name}: {str(e)}")
                indicators[name] = None
        return indicators

    def get_historical_data(self, series_name: str, period: str = '2Y') -> Dict:
        """
        Get historical data for a series

        Args:
            series_name: Name of the series (from config.FRED_SERIES)
            period: Time period (1Y, 2Y, 5Y, 10Y)

        Returns:
            Dictionary with dates and values
        """
        if series_name not in config.FRED_SERIES:
            raise ValueError(f"Unknown series: {series_name}")

        series_id = config.FRED_SERIES[series_name]

        # Parse period
        years = int(period[:-1]) if period.endswith('Y') else 2
        data = self.get_recent_data(series_id, years=years)

        # Convert to dictionary format
        result = {
            'dates': [d.strftime('%Y-%m-%d') for d in data.index],
            'values': [float(v) if pd.notna(v) else None for v in data.values],
            'series_name': series_name,
            'series_id': series_id
        }
        return result

    def get_rate_changes(self, series_id: str, months: int = 12) -> List[Dict]:
        """Calculate rate changes over time"""
        data = self.get_recent_data(series_id, years=months//12 + 1)
        changes = []

        for i in range(1, len(data)):
            if pd.notna(data.iloc[i]) and pd.notna(data.iloc[i-1]):
                change = data.iloc[i] - data.iloc[i-1]
                if abs(change) >= config.RATE_CHANGE_THRESHOLD:
                    changes.append({
                        'date': data.index[i].strftime('%Y-%m-%d'),
                        'value': float(data.iloc[i]),
                        'change': float(change),
                        'previous': float(data.iloc[i-1])
                    })

        return changes


if __name__ == "__main__":
    """Test the FRED client"""
    print("Testing FRED Client...")
    print("=" * 60)

    try:
        client = FREDClient()
        print("✓ FRED Client initialized successfully")
        print()

        # Test getting all indicators
        print("Fetching all economic indicators...")
        indicators = client.get_all_indicators()
        print()
        print("Current Economic Indicators:")
        print("-" * 60)
        for name, value in indicators.items():
            if value is not None:
                print(f"  {name:20s}: {value:>10.2f}")
            else:
                print(f"  {name:20s}: {'N/A':>10s}")

        print()
        print("✓ All indicators fetched successfully")

        # Test historical data
        print()
        print("Fetching historical Federal Funds Rate...")
        hist_data = client.get_historical_data('fed_funds_rate', '1Y')
        print(f"✓ Retrieved {len(hist_data['dates'])} data points")
        print(f"  Latest value: {hist_data['values'][-1]:.2f}%")

    except ValueError as e:
        print(f"✗ Configuration Error: {str(e)}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
