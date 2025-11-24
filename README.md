# FRED Portfolio Advisor

A comprehensive web application that analyzes Federal Reserve policy changes and provides actionable portfolio strategy recommendations using real-time data from the Federal Reserve Economic Data (FRED) API.

## Features

- **Real-time Economic Data** - Fetches current Fed Funds Rate, Treasury yields, inflation, unemployment, and more
- **Policy Stance Analysis** - Determines if Fed is Hawkish, Neutral, or Dovish
- **Portfolio Recommendations** - Provides specific asset allocation strategies
- **Scenario Analysis** - Shows alternative strategies for different economic outcomes
- **Interactive Dashboard** - Professional visualization of all data and insights
- **Export Functionality** - Generate presentation-ready reports

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher (for frontend)
- FRED API Key (free from https://fred.stlouisfed.org/docs/api/api_key.html)

## Setup Instructions

### 1. Get Your FRED API Key

1. Visit https://fred.stlouisfed.org/
2. Create a free account
3. Go to https://fred.stlouisfed.org/docs/api/api_key.html
4. Request an API key (instant approval)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure your API key (choose one method):

# Method 1: Edit config.py directly
# Open backend/config.py and replace 'YOUR_API_KEY_HERE' with your actual key

# Method 2: Use environment variable (recommended)
# Create a .env file
cp .env.example .env
# Edit .env and add your key:
echo "FRED_API_KEY=your_actual_api_key_here" > .env
```

### 3. Test the Backend

You can test each component independently:

```bash
# Test FRED API client
python fred_client.py

# Test policy analyzer
python analyzer.py

# Test portfolio advisor
python portfolio_advisor.py
```

### 4. Run the Flask API

```bash
# Start the backend server
python app.py
```

The API will be available at `http://localhost:5000`

### 5. Frontend Setup (Coming Next)

The React frontend will be set up in the next phase.

## API Endpoints

### Health Check
```
GET /
```

### Get All Economic Indicators
```
GET /api/indicators
```

Returns current values for:
- Federal Funds Rate
- 10-Year Treasury Yield
- 2-Year Treasury Yield
- Yield Curve Spread
- CPI (Inflation)
- Core PCE
- Unemployment Rate
- GDP
- M2 Money Supply

### Get Policy Stance Analysis
```
GET /api/policy-stance
```

Returns:
- Current Fed policy stance (Hawkish/Neutral/Dovish)
- Yield curve analysis
- Inflation pressure assessment
- Rate trajectory
- Executive summary

### Get Portfolio Recommendation
```
GET /api/portfolio-recommendation
```

Returns:
- Recommended strategy
- Asset allocation percentages
- Key action items
- Risk assessment
- Alternative scenarios
- Asset class outlook

### Get Historical Data
```
GET /api/historical/<series_name>?period=2Y
```

Parameters:
- `series_name`: fed_funds_rate, treasury_10y, treasury_2y, etc.
- `period`: 1Y, 2Y, 5Y, or 10Y

### Get Complete Dashboard Data
```
GET /api/dashboard
```

Returns all data needed for the dashboard in a single call.

### Export Report
```
GET /api/export/report
```

Returns formatted report data for presentations.

## Economic Indicators Tracked

| Indicator | FRED Series | Description |
|-----------|-------------|-------------|
| Fed Funds Rate | FEDFUNDS | Primary Fed policy tool |
| 10-Year Treasury | DGS10 | Long-term market expectations |
| 2-Year Treasury | DGS2 | Near-term outlook |
| Yield Curve | T10Y2Y | Recession indicator |
| CPI | CPIAUCSL | Consumer inflation |
| Core PCE | PCEPILFE | Fed's preferred inflation gauge |
| Unemployment | UNRATE | Labor market health |
| GDP | GDPC1 | Economic growth |
| M2 Money Supply | M2SL | Liquidity measure |

## Portfolio Strategies

### Hawkish Fed (Rising Rates)
- **Strategy:** Defensive Positioning
- **Focus:** Capital preservation, short duration
- **Allocation:** Higher cash, short-term bonds, value stocks

### Neutral Fed (Stable Rates)
- **Strategy:** Balanced Diversification
- **Focus:** Diversification across asset classes
- **Allocation:** Balanced equity/bond mix

### Dovish Fed (Falling Rates)
- **Strategy:** Growth-Oriented Positioning
- **Focus:** Growth and duration
- **Allocation:** Growth stocks, long-term bonds, REITs

## Testing

Run the test suite for each component:

```bash
# Test all components
python -c "
from fred_client import FREDClient
from analyzer import PolicyAnalyzer
from portfolio_advisor import PortfolioAdvisor

client = FREDClient()
analyzer = PolicyAnalyzer(client)
advisor = PortfolioAdvisor(analyzer)

indicators = client.get_all_indicators()
print('Indicators:', indicators)

stance = analyzer.analyze_policy_stance(indicators)
print('Policy Stance:', stance['stance'])

rec = advisor.get_recommendation(indicators)
print('Recommendation:', rec['strategy_name'])
"
```

## Project Structure

```
fred-portfolio-advisor/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── fred_client.py         # FRED API integration
│   ├── analyzer.py            # Policy analysis engine
│   ├── portfolio_advisor.py   # Portfolio recommendations
│   ├── config.py              # Configuration (API key here)
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
├── frontend/                  # React app (coming soon)
└── README.md                 # This file
```

## Usage Example

```python
from fred_client import FREDClient
from analyzer import PolicyAnalyzer
from portfolio_advisor import PortfolioAdvisor

# Initialize
client = FREDClient()
analyzer = PolicyAnalyzer(client)
advisor = PortfolioAdvisor(analyzer)

# Get current data
indicators = client.get_all_indicators()

# Analyze Fed policy
stance = analyzer.analyze_policy_stance(indicators)
print(f"Fed Stance: {stance['stance']}")

# Get portfolio recommendation
recommendation = advisor.get_recommendation(indicators)
print(f"Strategy: {recommendation['strategy_name']}")
print(f"Allocation: {recommendation['allocation']}")
```

## Troubleshooting

### "API key not set" error
Make sure you've added your FRED API key to either `config.py` or `.env` file.

### Import errors
Run `pip install -r requirements.txt` to ensure all dependencies are installed.

### No data returned
FRED API may have temporary outages. Check https://fred.stlouisfed.org/

## Next Steps

1. ✅ Backend API complete
2. 🔄 Build React frontend dashboard
3. 🔄 Add data visualization with charts
4. 🔄 Implement export to PDF/PowerPoint
5. 🔄 Add dark mode

## License

MIT License - Free to use for client presentations and analysis.

## Support

For FRED API issues: https://fred.stlouisfed.org/docs/api/
For app issues: Check logs in terminal

---

**Built for urgent client presentations requiring Fed policy analysis and portfolio strategy recommendations.**
