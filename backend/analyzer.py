"""
Policy Analyzer - Analyzes Federal Reserve policy stance and economic conditions
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import config
import logging

logger = logging.getLogger(__name__)


class PolicyAnalyzer:
    """Analyzes Fed policy stance and economic conditions"""

    def __init__(self, fred_client):
        """Initialize with a FRED client"""
        self.fred_client = fred_client

    def analyze_policy_stance(self, indicators: Dict[str, float]) -> Dict:
        """
        Determine current Fed policy stance (Hawkish, Neutral, Dovish)

        Args:
            indicators: Dictionary of current economic indicators

        Returns:
            Dictionary with policy stance analysis
        """
        fed_funds = indicators.get('fed_funds_rate')
        inflation = self._calculate_inflation_rate(indicators.get('cpi'))
        unemployment = indicators.get('unemployment')
        yield_curve = indicators.get('yield_curve')

        # Get rate momentum
        rate_momentum = self._calculate_rate_momentum('fed_funds_rate')

        # Determine stance based on multiple factors
        hawkish_signals = 0
        dovish_signals = 0

        # Signal 1: Rate trajectory
        if rate_momentum > 0.1:  # Rising rates
            hawkish_signals += 2
        elif rate_momentum < -0.1:  # Falling rates
            dovish_signals += 2

        # Signal 2: Inflation vs target
        if inflation and inflation > config.INFLATION_TARGET + 1:
            hawkish_signals += 2
        elif inflation and inflation < config.INFLATION_TARGET:
            dovish_signals += 1

        # Signal 3: Yield curve
        if yield_curve and yield_curve < config.YIELD_CURVE_INVERSION_THRESHOLD:
            dovish_signals += 1  # Inverted = recession risk = potential easing

        # Signal 4: Unemployment
        if unemployment and unemployment > 5.0:
            dovish_signals += 1
        elif unemployment and unemployment < 4.0:
            hawkish_signals += 1

        # Determine overall stance
        if hawkish_signals > dovish_signals + 1:
            stance = "Hawkish"
            color = "red"
            description = "Tightening policy to combat inflation"
        elif dovish_signals > hawkish_signals + 1:
            stance = "Dovish"
            color = "green"
            description = "Accommodative policy to support growth"
        else:
            stance = "Neutral"
            color = "yellow"
            description = "Balanced approach, monitoring data"

        return {
            'stance': stance,
            'color': color,
            'description': description,
            'confidence': abs(hawkish_signals - dovish_signals) * 10,
            'hawkish_signals': hawkish_signals,
            'dovish_signals': dovish_signals,
            'rate_momentum': rate_momentum,
            'analysis_date': datetime.now().isoformat()
        }

    def _calculate_rate_momentum(self, series_name: str, months: int = 6) -> float:
        """Calculate rate change momentum over recent months"""
        try:
            series_id = config.FRED_SERIES.get(series_name)
            if not series_id:
                return 0.0

            data = self.fred_client.get_recent_data(series_id, years=1)
            if len(data) < 2:
                return 0.0

            # Calculate change over last 6 months
            recent = data.last(f'{months}M')
            if len(recent) >= 2:
                change = float(recent.iloc[-1] - recent.iloc[0])
                return change
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating momentum: {str(e)}")
            return 0.0

    def _calculate_inflation_rate(self, cpi_value: float) -> float:
        """Calculate year-over-year inflation rate from CPI"""
        try:
            series_id = config.FRED_SERIES['cpi']
            data = self.fred_client.get_recent_data(series_id, years=2)

            if len(data) < 12:
                return None

            # Get YoY change
            current = data.iloc[-1]
            year_ago = data.iloc[-13] if len(data) >= 13 else data.iloc[-12]

            inflation_rate = ((current - year_ago) / year_ago) * 100
            return float(inflation_rate)
        except Exception as e:
            logger.error(f"Error calculating inflation: {str(e)}")
            return None

    def analyze_yield_curve(self, indicators: Dict[str, float]) -> Dict:
        """Analyze yield curve for recession signals"""
        spread = indicators.get('yield_curve')

        if spread is None:
            return {
                'status': 'Unknown',
                'description': 'Data unavailable',
                'recession_risk': 'Unknown'
            }

        if spread < 0:
            status = "Inverted"
            description = "10-year yield below 2-year (recession warning)"
            recession_risk = "High"
        elif spread < 0.5:
            status = "Flat"
            description = "Yield curve flattening (caution)"
            recession_risk = "Moderate"
        else:
            status = "Normal"
            description = "Positive slope (healthy economy)"
            recession_risk = "Low"

        return {
            'status': status,
            'spread': spread,
            'description': description,
            'recession_risk': recession_risk
        }

    def analyze_inflation_pressure(self, indicators: Dict[str, float]) -> Dict:
        """Analyze inflation pressure relative to Fed target"""
        inflation = self._calculate_inflation_rate(indicators.get('cpi'))

        if inflation is None:
            return {
                'status': 'Unknown',
                'description': 'Data unavailable'
            }

        distance_from_target = inflation - config.INFLATION_TARGET

        if inflation > config.INFLATION_TARGET + 2:
            status = "High Pressure"
            description = f"Inflation {distance_from_target:.1f}pp above target"
            color = "red"
        elif inflation > config.INFLATION_TARGET + 0.5:
            status = "Elevated"
            description = f"Inflation {distance_from_target:.1f}pp above target"
            color = "orange"
        elif inflation < config.INFLATION_TARGET - 0.5:
            status = "Below Target"
            description = f"Inflation {abs(distance_from_target):.1f}pp below target"
            color = "blue"
        else:
            status = "Near Target"
            description = "Inflation close to Fed's 2% target"
            color = "green"

        return {
            'status': status,
            'current_rate': inflation,
            'target': config.INFLATION_TARGET,
            'distance_from_target': distance_from_target,
            'description': description,
            'color': color
        }

    def get_rate_trajectory(self) -> Dict:
        """Analyze recent rate changes and trajectory"""
        try:
            changes = self.fred_client.get_rate_changes(
                config.FRED_SERIES['fed_funds_rate'],
                months=24
            )

            if not changes:
                return {
                    'recent_changes': [],
                    'trajectory': 'Stable',
                    'total_change': 0
                }

            # Calculate total change
            if len(changes) > 0:
                total_change = changes[-1]['value'] - changes[0]['previous']
            else:
                total_change = 0

            # Determine trajectory
            if len(changes) >= 2:
                recent_changes = changes[-3:]
                avg_change = sum(c['change'] for c in recent_changes) / len(recent_changes)

                if avg_change > 0.1:
                    trajectory = "Rising"
                elif avg_change < -0.1:
                    trajectory = "Falling"
                else:
                    trajectory = "Stable"
            else:
                trajectory = "Stable"

            return {
                'recent_changes': changes[-10:],  # Last 10 changes
                'trajectory': trajectory,
                'total_change': total_change,
                'num_changes': len(changes)
            }
        except Exception as e:
            logger.error(f"Error analyzing trajectory: {str(e)}")
            return {
                'recent_changes': [],
                'trajectory': 'Unknown',
                'total_change': 0
            }

    def generate_summary(self, indicators: Dict[str, float]) -> str:
        """Generate a one-sentence summary of current conditions"""
        stance_analysis = self.analyze_policy_stance(indicators)
        stance = stance_analysis['stance']
        inflation = self._calculate_inflation_rate(indicators.get('cpi'))
        fed_funds = indicators.get('fed_funds_rate')

        if stance == "Hawkish":
            return (f"Fed maintains {stance.lower()} stance with rates at {fed_funds:.2f}% "
                    f"as inflation remains at {inflation:.1f}%, above the 2% target.")
        elif stance == "Dovish":
            return (f"Fed signals {stance.lower()} pivot with rates at {fed_funds:.2f}% "
                    f"as economic concerns mount.")
        else:
            return (f"Fed holds {stance.lower()} position at {fed_funds:.2f}% "
                    f"while monitoring inflation at {inflation:.1f}%.")


if __name__ == "__main__":
    """Test the analyzer"""
    from fred_client import FREDClient

    print("Testing Policy Analyzer...")
    print("=" * 60)

    try:
        client = FREDClient()
        analyzer = PolicyAnalyzer(client)

        # Get current indicators
        print("Fetching current indicators...")
        indicators = client.get_all_indicators()

        # Test policy stance analysis
        print("\nPolicy Stance Analysis:")
        print("-" * 60)
        stance = analyzer.analyze_policy_stance(indicators)
        print(f"  Stance: {stance['stance']} ({stance['confidence']}% confidence)")
        print(f"  Description: {stance['description']}")
        print(f"  Rate Momentum: {stance['rate_momentum']:.2f}")

        # Test yield curve analysis
        print("\nYield Curve Analysis:")
        print("-" * 60)
        yc_analysis = analyzer.analyze_yield_curve(indicators)
        print(f"  Status: {yc_analysis['status']}")
        print(f"  Spread: {yc_analysis.get('spread', 'N/A')}")
        print(f"  Recession Risk: {yc_analysis['recession_risk']}")

        # Test inflation analysis
        print("\nInflation Analysis:")
        print("-" * 60)
        inf_analysis = analyzer.analyze_inflation_pressure(indicators)
        print(f"  Status: {inf_analysis['status']}")
        print(f"  Current: {inf_analysis.get('current_rate', 'N/A'):.2f}%")
        print(f"  Target: {inf_analysis.get('target', 'N/A')}%")

        # Test summary
        print("\nExecutive Summary:")
        print("-" * 60)
        summary = analyzer.generate_summary(indicators)
        print(f"  {summary}")

        print("\n✓ Analyzer tests completed successfully")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
