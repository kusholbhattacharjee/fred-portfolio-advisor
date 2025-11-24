"""
Portfolio Advisor - Generates portfolio strategy recommendations based on Fed policy
"""
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class PortfolioAdvisor:
    """Generates portfolio recommendations based on Fed policy analysis"""

    def __init__(self, analyzer):
        """Initialize with a PolicyAnalyzer"""
        self.analyzer = analyzer

    def get_recommendation(self, indicators: Dict[str, float]) -> Dict:
        """
        Generate portfolio recommendation based on current conditions

        Args:
            indicators: Current economic indicators

        Returns:
            Dictionary with portfolio recommendation
        """
        stance_analysis = self.analyzer.analyze_policy_stance(indicators)
        stance = stance_analysis['stance']
        yc_analysis = self.analyzer.analyze_yield_curve(indicators)
        inf_analysis = self.analyzer.analyze_inflation_pressure(indicators)

        if stance == "Hawkish":
            return self._hawkish_strategy(stance_analysis, yc_analysis, inf_analysis)
        elif stance == "Dovish":
            return self._dovish_strategy(stance_analysis, yc_analysis, inf_analysis)
        else:
            return self._neutral_strategy(stance_analysis, yc_analysis, inf_analysis)

    def _hawkish_strategy(self, stance: Dict, yield_curve: Dict, inflation: Dict) -> Dict:
        """Strategy for hawkish Fed policy"""
        return {
            'strategy_name': 'Defensive Positioning',
            'risk_level': 'Moderate-High',
            'timeframe': 'Medium-term (6-12 months)',
            'allocation': {
                'Cash/Money Market': 20,
                'Short-term Bonds (< 2yr)': 30,
                'Value Stocks': 25,
                'Commodities/TIPS': 15,
                'International Equity': 10
            },
            'key_actions': [
                'Reduce portfolio duration to minimize interest rate risk',
                'Shift to value stocks and quality dividend payers',
                'Increase cash reserves for future opportunities',
                'Consider inflation-protected securities (TIPS)',
                'Reduce exposure to high-growth, high-valuation stocks'
            ],
            'rationale': (
                'With the Fed maintaining a hawkish stance, rising rates pose risks to '
                'long-duration assets. This defensive approach prioritizes capital preservation '
                'while maintaining income generation through short-term fixed income and '
                'dividend-paying equities.'
            ),
            'risks': [
                'May underperform if Fed pivots earlier than expected',
                'Cash drag on returns in stable markets',
                'Commodities can be volatile'
            ],
            'opportunities': [
                'Higher yields on short-term fixed income',
                'Value stocks tend to outperform in rising rate environments',
                'Building cash for buying opportunities'
            ]
        }

    def _dovish_strategy(self, stance: Dict, yield_curve: Dict, inflation: Dict) -> Dict:
        """Strategy for dovish Fed policy"""
        return {
            'strategy_name': 'Growth-Oriented Positioning',
            'risk_level': 'Moderate',
            'timeframe': 'Medium-term (6-12 months)',
            'allocation': {
                'Growth Stocks': 35,
                'Long-term Bonds (10+ yr)': 25,
                'REITs': 15,
                'Small-cap Equity': 15,
                'Cash/Money Market': 10
            },
            'key_actions': [
                'Extend duration in fixed income to lock in yields',
                'Increase exposure to growth and technology stocks',
                'Add REITs to benefit from lower rate environment',
                'Consider small-cap equities for higher growth potential',
                'Reduce cash allocation as rate environment improves'
            ],
            'rationale': (
                'A dovish Fed signals lower rates ahead, creating a favorable environment '
                'for growth assets. Long-duration bonds benefit from falling rates, while '
                'growth stocks and REITs tend to outperform in accommodative policy environments.'
            ),
            'risks': [
                'Growth stocks can be volatile',
                'Bond rally may be short-lived if inflation resurges',
                'REITs sensitive to economic slowdown'
            ],
            'opportunities': [
                'Growth stocks benefit from lower discount rates',
                'Capital gains potential in long-term bonds',
                'REITs offer income and appreciation potential'
            ]
        }

    def _neutral_strategy(self, stance: Dict, yield_curve: Dict, inflation: Dict) -> Dict:
        """Strategy for neutral Fed policy"""
        return {
            'strategy_name': 'Balanced Diversification',
            'risk_level': 'Moderate',
            'timeframe': 'Medium-term (6-12 months)',
            'allocation': {
                'Broad Equity Index': 35,
                'Intermediate Bonds (2-10yr)': 30,
                'Value Stocks': 15,
                'Cash/Money Market': 10,
                'Alternative Assets': 10
            },
            'key_actions': [
                'Maintain diversified portfolio across asset classes',
                'Balance between growth and value equities',
                'Use intermediate-duration bonds for income',
                'Keep modest cash reserves for flexibility',
                'Monitor Fed communications for stance changes'
            ],
            'rationale': (
                'With the Fed on hold, a balanced approach allows participation in market '
                'upside while maintaining downside protection. Diversification across asset '
                'classes provides stability as the Fed assesses economic data.'
            ),
            'risks': [
                'May lag in strong directional markets',
                'Requires active monitoring for stance changes',
                'Middle-ground approach to both risks and opportunities'
            ],
            'opportunities': [
                'Flexibility to adjust as conditions evolve',
                'Income generation from bonds and dividends',
                'Reduced volatility through diversification'
            ]
        }

    def get_scenario_analysis(self, indicators: Dict[str, float]) -> List[Dict]:
        """Generate alternative scenarios and recommendations"""
        scenarios = []

        # Scenario 1: Rates rise faster than expected
        scenarios.append({
            'scenario': 'Accelerated Rate Hikes',
            'probability': 'Low-Moderate',
            'trigger': 'Inflation remains persistently high above 4%',
            'adjustment': {
                'action': 'Increase defensive positioning',
                'changes': [
                    'Raise cash to 25-30%',
                    'Shorten bond duration further',
                    'Add defensive sectors (utilities, healthcare)',
                    'Consider inverse rate ETFs for hedging'
                ]
            }
        })

        # Scenario 2: Recession materializes
        scenarios.append({
            'scenario': 'Economic Recession',
            'probability': 'Moderate',
            'trigger': 'Yield curve inverted, unemployment rising',
            'adjustment': {
                'action': 'Shift to quality and defensive assets',
                'changes': [
                    'Increase long-term government bonds',
                    'Focus on large-cap quality stocks',
                    'Add gold as safe haven',
                    'Reduce cyclical exposure'
                ]
            }
        })

        # Scenario 3: Soft landing achieved
        scenarios.append({
            'scenario': 'Soft Landing Success',
            'probability': 'Moderate-High',
            'trigger': 'Inflation moderates without major economic damage',
            'adjustment': {
                'action': 'Gradually increase risk exposure',
                'changes': [
                    'Add growth stocks selectively',
                    'Maintain balanced bond duration',
                    'Consider cyclical sectors',
                    'Reduce cash drag over time'
                ]
            }
        })

        return scenarios

    def get_asset_class_outlook(self, indicators: Dict[str, float]) -> Dict:
        """Provide outlook for major asset classes"""
        stance_analysis = self.analyzer.analyze_policy_stance(indicators)
        stance = stance_analysis['stance']

        if stance == "Hawkish":
            return {
                'Equities': {
                    'outlook': 'Cautious',
                    'score': 5,
                    'comment': 'Headwinds from higher rates; prefer value over growth'
                },
                'Fixed Income': {
                    'outlook': 'Selective',
                    'score': 6,
                    'comment': 'Higher yields attractive, but prefer short duration'
                },
                'Cash': {
                    'outlook': 'Attractive',
                    'score': 8,
                    'comment': 'Strong yields with zero duration risk'
                },
                'Commodities': {
                    'outlook': 'Moderate',
                    'score': 6,
                    'comment': 'Inflation hedge, but demand concerns'
                },
                'REITs': {
                    'outlook': 'Weak',
                    'score': 3,
                    'comment': 'Vulnerable to higher rates'
                }
            }
        elif stance == "Dovish":
            return {
                'Equities': {
                    'outlook': 'Positive',
                    'score': 8,
                    'comment': 'Lower rates support valuations; favor growth'
                },
                'Fixed Income': {
                    'outlook': 'Positive',
                    'score': 7,
                    'comment': 'Capital gains potential as rates fall'
                },
                'Cash': {
                    'outlook': 'Weak',
                    'score': 4,
                    'comment': 'Opportunity cost as yields decline'
                },
                'Commodities': {
                    'outlook': 'Moderate',
                    'score': 5,
                    'comment': 'Mixed signals from growth concerns'
                },
                'REITs': {
                    'outlook': 'Positive',
                    'score': 7,
                    'comment': 'Benefit from lower rates and income'
                }
            }
        else:
            return {
                'Equities': {
                    'outlook': 'Neutral',
                    'score': 6,
                    'comment': 'Balanced risk-reward; maintain diversification'
                },
                'Fixed Income': {
                    'outlook': 'Neutral',
                    'score': 6,
                    'comment': 'Steady income, moderate price sensitivity'
                },
                'Cash': {
                    'outlook': 'Moderate',
                    'score': 5,
                    'comment': 'Adequate yields, maintains flexibility'
                },
                'Commodities': {
                    'outlook': 'Neutral',
                    'score': 5,
                    'comment': 'Range-bound with mixed fundamentals'
                },
                'REITs': {
                    'outlook': 'Moderate',
                    'score': 6,
                    'comment': 'Income generation with moderate risk'
                }
            }


if __name__ == "__main__":
    """Test the portfolio advisor"""
    from fred_client import FREDClient
    from analyzer import PolicyAnalyzer

    print("Testing Portfolio Advisor...")
    print("=" * 60)

    try:
        client = FREDClient()
        analyzer = PolicyAnalyzer(client)
        advisor = PortfolioAdvisor(analyzer)

        # Get current indicators
        indicators = client.get_all_indicators()

        # Test recommendation
        print("\nPortfolio Recommendation:")
        print("-" * 60)
        rec = advisor.get_recommendation(indicators)
        print(f"  Strategy: {rec['strategy_name']}")
        print(f"  Risk Level: {rec['risk_level']}")
        print(f"  Timeframe: {rec['timeframe']}")
        print(f"\n  Asset Allocation:")
        for asset, pct in rec['allocation'].items():
            print(f"    {asset:30s}: {pct:>3d}%")

        print(f"\n  Top 3 Actions:")
        for i, action in enumerate(rec['key_actions'][:3], 1):
            print(f"    {i}. {action}")

        # Test scenario analysis
        print("\n\nAlternative Scenarios:")
        print("-" * 60)
        scenarios = advisor.get_scenario_analysis(indicators)
        for scenario in scenarios:
            print(f"  {scenario['scenario']} (Probability: {scenario['probability']})")
            print(f"    Trigger: {scenario['trigger']}")

        # Test asset class outlook
        print("\n\nAsset Class Outlook:")
        print("-" * 60)
        outlook = advisor.get_asset_class_outlook(indicators)
        for asset, details in outlook.items():
            print(f"  {asset:15s}: {details['outlook']:10s} (Score: {details['score']}/10)")
            print(f"    {details['comment']}")

        print("\n✓ Portfolio advisor tests completed successfully")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
