"""
Quick test script for backend components
"""
import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import config
        import fred_client
        import analyzer
        import portfolio_advisor
        import app
        print("✓ All modules imported successfully\n")
        return True
    except Exception as e:
        print(f"✗ Import error: {str(e)}\n")
        return False


def test_configuration():
    """Test configuration"""
    print("Testing configuration...")
    try:
        import config
        api_key = config.FRED_API_KEY

        if api_key == 'YOUR_API_KEY_HERE':
            print("⚠ API key not configured yet")
            print("  Please add your FRED API key to backend/config.py or backend/.env")
            print("  Get your free key at: https://fred.stlouisfed.org/docs/api/api_key.html\n")
            return False
        else:
            print(f"✓ API key configured (length: {len(api_key)} chars)\n")
            return True
    except Exception as e:
        print(f"✗ Configuration error: {str(e)}\n")
        return False


def test_fred_client():
    """Test FRED client"""
    print("Testing FRED client...")
    try:
        from fred_client import FREDClient

        # This will fail if API key not set, which is expected
        try:
            client = FREDClient()
            print("✓ FRED client initialized")

            # Try to fetch one indicator
            print("  Attempting to fetch Federal Funds Rate...")
            value = client.get_latest_value('FEDFUNDS')
            if value:
                print(f"✓ Successfully fetched data: Fed Funds Rate = {value:.2f}%\n")
                return True
            else:
                print("⚠ No data returned (may be API issue)\n")
                return False

        except ValueError as e:
            if "API key" in str(e):
                print("⚠ API key not configured")
                print(f"  {str(e)}\n")
                return False
            raise

    except Exception as e:
        print(f"✗ FRED client error: {str(e)}\n")
        return False


def test_analyzer():
    """Test analyzer"""
    print("Testing analyzer...")
    try:
        from fred_client import FREDClient
        from analyzer import PolicyAnalyzer

        client = FREDClient()
        analyzer = PolicyAnalyzer(client)
        print("✓ Policy analyzer initialized\n")
        return True
    except ValueError as e:
        if "API key" in str(e):
            print("⚠ Skipped (API key needed)\n")
            return False
        raise
    except Exception as e:
        print(f"✗ Analyzer error: {str(e)}\n")
        return False


def test_advisor():
    """Test portfolio advisor"""
    print("Testing portfolio advisor...")
    try:
        from fred_client import FREDClient
        from analyzer import PolicyAnalyzer
        from portfolio_advisor import PortfolioAdvisor

        client = FREDClient()
        analyzer = PolicyAnalyzer(client)
        advisor = PortfolioAdvisor(analyzer)
        print("✓ Portfolio advisor initialized\n")
        return True
    except ValueError as e:
        if "API key" in str(e):
            print("⚠ Skipped (API key needed)\n")
            return False
        raise
    except Exception as e:
        print(f"✗ Portfolio advisor error: {str(e)}\n")
        return False


def test_flask_app():
    """Test Flask app"""
    print("Testing Flask app...")
    try:
        from app import app
        print("✓ Flask app loaded successfully\n")
        return True
    except ValueError as e:
        if "API key" in str(e):
            print("⚠ Flask app requires API key to initialize\n")
            return False
        raise
    except Exception as e:
        print(f"✗ Flask app error: {str(e)}\n")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("FRED Portfolio Advisor - Backend Test Suite")
    print("=" * 60)
    print()

    results = {
        'Imports': test_imports(),
        'Configuration': test_configuration(),
        'FRED Client': test_fred_client(),
        'Policy Analyzer': test_analyzer(),
        'Portfolio Advisor': test_advisor(),
        'Flask App': test_flask_app()
    }

    print("=" * 60)
    print("Test Summary:")
    print("-" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name:25s}: {status}")

    print("-" * 60)
    print(f"  Total: {passed}/{total} tests passed")
    print("=" * 60)

    if not results['Configuration']:
        print()
        print("NEXT STEP: Configure your FRED API key")
        print("-" * 60)
        print("1. Get your free API key at:")
        print("   https://fred.stlouisfed.org/docs/api/api_key.html")
        print()
        print("2. Add it to one of these files:")
        print("   Option A: Edit backend/config.py")
        print("   Option B: Edit backend/.env")
        print()
        print("3. Run this test again to verify")
        print("=" * 60)

    elif results['FRED Client']:
        print()
        print("SUCCESS! Backend is ready to use.")
        print("-" * 60)
        print("Start the API server with:")
        print("  python app.py")
        print()
        print("Or test individual components:")
        print("  python fred_client.py")
        print("  python analyzer.py")
        print("  python portfolio_advisor.py")
        print("=" * 60)

    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
