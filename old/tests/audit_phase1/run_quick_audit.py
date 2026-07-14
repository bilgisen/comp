"""
Quick Audit Runner - CORE TESTS
Runs essential audit tests and generates summary report
"""
import sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

print("\n" + "="*70)
print("FINANCIAL ENGINE QUICK AUDIT")
print("="*70)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# Test 1: Data Quality
print("\n\n")
print("="*70)
print("TEST 1: DATA QUALITY CHECK")
print("="*70)
try:
    from test_data_quality import DataQualityAuditor
    auditor1 = DataQualityAuditor()
    auditor1.run_audit()
    print("\n✅ Data Quality Check COMPLETED")
except Exception as e:
    print(f"\n❌ Data Quality Check FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 2: Ratio Accuracy
print("\n\n")
print("="*70)
print("TEST 2: RATIO CALCULATION ACCURACY")
print("="*70)
try:
    from test_ratio_accuracy import RatioAccuracyAuditor
    auditor2 = RatioAccuracyAuditor()
    auditor2.run_audit()
    print("\n✅ Ratio Accuracy Check COMPLETED")
except Exception as e:
    print(f"\n❌ Ratio Accuracy Check FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 3: Benchmark Accuracy
print("\n\n")
print("="*70)
print("TEST 3: BENCHMARK CALCULATION ACCURACY")
print("="*70)
try:
    from test_benchmark_accuracy import BenchmarkAccuracyAuditor
    auditor3 = BenchmarkAccuracyAuditor()
    auditor3.run_audit()
    print("\n✅ Benchmark Accuracy Check COMPLETED")
except Exception as e:
    print(f"\n❌ Benchmark Accuracy Check FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# Final Summary
print("\n\n")
print("="*70)
print("AUDIT COMPLETED")
print("="*70)
print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()
print("Review the results above for:")
print("  • Data quality and coverage issues")
print("  • Ratio calculation accuracy")
print("  • Benchmark calculation accuracy")
print()
print("="*70)
