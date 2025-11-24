"""
Flask API for FRED Portfolio Advisor
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import logging

from fred_client import FREDClient
from analyzer import PolicyAnalyzer
from portfolio_advisor import PortfolioAdvisor
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize components
try:
    fred_client = FREDClient()
    analyzer = PolicyAnalyzer(fred_client)
    advisor = PortfolioAdvisor(analyzer)
    logger.info("Application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize application: {str(e)}")
    raise


@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'FRED Portfolio Advisor API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    """Get all current economic indicators"""
    try:
        logger.info("Fetching current indicators")
        indicators = fred_client.get_all_indicators()

        # Calculate additional metrics
        inflation_rate = analyzer._calculate_inflation_rate(indicators.get('cpi'))

        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'indicators': indicators,
            'calculated': {
                'inflation_rate': inflation_rate
            }
        }
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error fetching indicators: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/policy-stance', methods=['GET'])
def get_policy_stance():
    """Get current Fed policy stance analysis"""
    try:
        logger.info("Analyzing policy stance")
        indicators = fred_client.get_all_indicators()

        stance = analyzer.analyze_policy_stance(indicators)
        yield_curve = analyzer.analyze_yield_curve(indicators)
        inflation_pressure = analyzer.analyze_inflation_pressure(indicators)
        rate_trajectory = analyzer.get_rate_trajectory()
        summary = analyzer.generate_summary(indicators)

        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'policy_stance': stance,
            'yield_curve': yield_curve,
            'inflation_pressure': inflation_pressure,
            'rate_trajectory': rate_trajectory,
            'executive_summary': summary
        }
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error analyzing policy stance: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/portfolio-recommendation', methods=['GET'])
def get_portfolio_recommendation():
    """Get portfolio strategy recommendation"""
    try:
        logger.info("Generating portfolio recommendation")
        indicators = fred_client.get_all_indicators()

        recommendation = advisor.get_recommendation(indicators)
        scenarios = advisor.get_scenario_analysis(indicators)
        asset_outlook = advisor.get_asset_class_outlook(indicators)

        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'recommendation': recommendation,
            'alternative_scenarios': scenarios,
            'asset_class_outlook': asset_outlook
        }
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/historical/<series_name>', methods=['GET'])
def get_historical_data(series_name):
    """
    Get historical data for a specific series
    Query params: period (1Y, 2Y, 5Y, 10Y)
    """
    try:
        period = request.args.get('period', '2Y')
        logger.info(f"Fetching historical data for {series_name}, period: {period}")

        data = fred_client.get_historical_data(series_name, period)

        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        return jsonify(response)
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error fetching historical data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get all data needed for dashboard in one call"""
    try:
        logger.info("Fetching complete dashboard data")

        # Get all components
        indicators = fred_client.get_all_indicators()
        inflation_rate = analyzer._calculate_inflation_rate(indicators.get('cpi'))

        stance = analyzer.analyze_policy_stance(indicators)
        yield_curve = analyzer.analyze_yield_curve(indicators)
        inflation_pressure = analyzer.analyze_inflation_pressure(indicators)
        rate_trajectory = analyzer.get_rate_trajectory()
        summary = analyzer.generate_summary(indicators)

        recommendation = advisor.get_recommendation(indicators)
        scenarios = advisor.get_scenario_analysis(indicators)
        asset_outlook = advisor.get_asset_class_outlook(indicators)

        # Get recent historical data for charts
        fed_funds_history = fred_client.get_historical_data('fed_funds_rate', '2Y')
        treasury_10y_history = fred_client.get_historical_data('treasury_10y', '2Y')
        treasury_2y_history = fred_client.get_historical_data('treasury_2y', '2Y')

        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'last_update': datetime.now().strftime('%B %d, %Y at %I:%M %p'),

            # Summary
            'executive_summary': summary,

            # Current indicators
            'indicators': {
                **indicators,
                'inflation_rate': inflation_rate
            },

            # Analysis
            'policy_stance': stance,
            'yield_curve': yield_curve,
            'inflation_pressure': inflation_pressure,
            'rate_trajectory': rate_trajectory,

            # Recommendations
            'recommendation': recommendation,
            'alternative_scenarios': scenarios,
            'asset_class_outlook': asset_outlook,

            # Historical data for charts
            'historical_data': {
                'fed_funds_rate': fed_funds_history,
                'treasury_10y': treasury_10y_history,
                'treasury_2y': treasury_2y_history
            }
        }

        return jsonify(response)
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/report', methods=['GET'])
def export_report():
    """Generate exportable report data"""
    try:
        logger.info("Generating export report")
        indicators = fred_client.get_all_indicators()

        stance = analyzer.analyze_policy_stance(indicators)
        recommendation = advisor.get_recommendation(indicators)
        asset_outlook = advisor.get_asset_class_outlook(indicators)
        summary = analyzer.generate_summary(indicators)

        report = {
            'generated_at': datetime.now().isoformat(),
            'report_date': datetime.now().strftime('%B %d, %Y'),
            'title': 'Federal Reserve Policy Analysis & Portfolio Strategy',
            'summary': summary,
            'policy_stance': stance['stance'],
            'recommendation': recommendation['strategy_name'],
            'key_actions': recommendation['key_actions'],
            'allocation': recommendation['allocation'],
            'asset_outlook': asset_outlook,
            'indicators': indicators
        }

        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("FRED Portfolio Advisor API")
    print("=" * 60)
    print("\nStarting server...")
    print("\nAPI Endpoints:")
    print("  GET  /                              - Health check")
    print("  GET  /api/indicators                - Current indicators")
    print("  GET  /api/policy-stance             - Policy analysis")
    print("  GET  /api/portfolio-recommendation  - Strategy recommendation")
    print("  GET  /api/historical/<series>       - Historical data")
    print("  GET  /api/dashboard                 - Complete dashboard data")
    print("  GET  /api/export/report             - Export report")
    print("\nServer running on http://localhost:5001")
    print("=" * 60)
    print()

    app.run(debug=True, host='0.0.0.0', port=5001)
