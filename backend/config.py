"""
Configuration file for FRED Portfolio Advisor
"""
import os
from dotenv import load_dotenv

load_dotenv()

# FRED API Configuration
# PUT YOUR FRED API KEY HERE (or set it in .env file as FRED_API_KEY=your_key)
FRED_API_KEY = os.getenv('FRED_API_KEY', 'YOUR_API_KEY_HERE')

# Key economic indicators from FRED
FRED_SERIES = {
    'fed_funds_rate': 'FEDFUNDS',
    'treasury_10y': 'DGS10',
    'treasury_2y': 'DGS2',
    'yield_curve': 'T10Y2Y',
    'cpi': 'CPIAUCSL',
    'core_pce': 'PCEPILFE',
    'unemployment': 'UNRATE',
    'gdp': 'GDPC1',
    'm2_money_supply': 'M2SL',
}

# Analysis thresholds
INFLATION_TARGET = 2.0
YIELD_CURVE_INVERSION_THRESHOLD = 0.0
RATE_CHANGE_THRESHOLD = 0.25  # 25 basis points

# Cache settings (in seconds)
CACHE_DURATION = 900  # 15 minutes
