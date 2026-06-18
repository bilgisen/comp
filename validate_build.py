#!/usr/bin/env python3
"""
HissePro COMP Engine - Build Validation Script
Validates that all imports and core functionality work before deployment.
"""

import sys
import traceback

def test_imports():
    """Test all core imports to ensure the package is properly configured."""
    print("🔧 Testing core imports...")
    
    try:
        # Core imports
        from core.config import settings
        from core.database import get_db, init_db, Base
        from core.cache import CacheManager
        print("  ✅ Core modules imported successfully")
        
        # Model imports
        from models.company import Company, CompanyMetrics
        from models.financial import CompanyRatio, FinancialStatementRaw
        from models.benchmark import SectorBenchmark, SectorBenchmarkPeer
        print("  ✅ Model classes imported successfully")
        
        # Service imports
        from services.isyatirim_client import IsYatirimClient
        from services.ratio_calculator import RatioCalculator
        from services.sector_benchmarks import SectorBenchmarkService
        from services.comparison_service import ComparisonService
        from services.trend_analysis import TrendAnalysisService
        from services.ai_context_builder import AIContextBuilder
        from services.scheduler import SchedulerService
        print("  ✅ Service classes imported successfully")
        
        # Router imports
        from routers.companies import router as companies_router
        from routers.sectors import router as sectors_router
        from routers.admin import router as admin_router
        from routers.ai_context import router as ai_router
        print("  ✅ Router modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        traceback.print_exc()
        return False

def test_main_app():
    """Test main FastAPI application creation."""
    print("\n🚀 Testing main application...")
    
    try:
        from main import app
        print(f"  ✅ FastAPI app created successfully: {type(app)}")
        
        # Check if routes are registered
        routes = [route.path for route in app.routes]
        expected_routes = ["/health", "/api/v1/companies", "/api/v1/sectors", "/api/v1/admin"]
        
        for expected in expected_routes:
            if any(expected in route for route in routes):
                print(f"  ✅ Route group '{expected}' registered")
            else:
                print(f"  ⚠️  Route group '{expected}' not found")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Main app error: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Test configuration loading."""
    print("\n⚙️ Testing configuration...")
    
    try:
        from core.config import settings
        print(f"  ✅ Settings loaded: {type(settings)}")
        print(f"  ✅ Database URL configured: {'Yes' if settings.database_url else 'No'}")
        print(f"  ✅ Redis URL configured: {'Yes' if settings.redis_url else 'No'}")
        return True
        
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all validation tests."""
    print("🏗️ HissePro COMP Engine - Build Validation")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Main App", test_main_app),
        ("Configuration", test_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {name} test failed")
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())