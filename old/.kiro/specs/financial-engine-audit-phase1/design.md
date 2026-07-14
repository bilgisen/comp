# Design Document: Financial Engine Audit Phase 1

## Overview

The Financial Engine Audit Phase 1 system is a comprehensive testing and validation framework designed to verify the correctness, reliability, and data quality of the HissePro Financial Analysis Engine. The system performs deep analysis of sector classifications, ratio calculations, benchmark computations, and data integrity across 14 sectors and 620+ Turkish public companies.

### Purpose

This audit system serves three primary purposes:

1. **Verification**: Validate that financial calculations (ratios, benchmarks, TTM) produce mathematically correct results
2. **Quality Assurance**: Assess data completeness, mapping coverage, and classification accuracy
3. **Documentation**: Generate comprehensive audit reports that identify issues and provide actionable recommendations for Phase 2 improvements

### Scope

The audit system tests the following components of the Financial Analysis Engine:

- **Data Layer**: Financial statement fetching, storage, and item code mapping
- **Calculation Layer**: Ratio calculation formulas and TTM aggregation logic
- **Benchmark Layer**: F1-F5 filter pipeline and statistical computations
- **Classification Layer**: Sector assignments and financial group mappings
- **Integration Layer**: Bootstrap process orchestration and data flow

### Key Principles

1. **Separation of Concerns**: Test suite modules are independent and can be executed individually
2. **Dual Testing Strategy**: Property-based tests for universal logic + integration tests for data validation
3. **Synthetic Data Generation**: Use both synthetic and real data to validate correctness
4. **Comprehensive Reporting**: ASCII tables, statistics, and visualizations in Markdown format
5. **Non-Destructive**: Audit operates in read-only mode (except for test database fixtures)


## Architecture

### System Architecture Diagram

```mermaid
graph TB
    subgraph "Test Orchestrator"
        TO[Test Runner]
        TP[Test Parser]
        RG[Report Generator]
    end
    
    subgraph "Test Suite Modules"
        T1[Sector Classification Tests]
        T2[Item Code Mapping Tests]
        T3[Ratio Formula Tests]
        T4[Ratio Calculation Tests]
        T5[TTM Calculation Tests]
        T6[Filter Pipeline Tests]
        T7[Economic Bounds Tests]
        T8[Benchmark Accuracy Tests]
        T9[Reliability Assessment Tests]
        T10[Data Quality Tests]
        T11[Bootstrap Process Tests]
        T12[Sector-Specific Ratio Tests]
    end
    
    subgraph "Data Sources"
        DB[(Production Database)]
        SD[Synthetic Data Generator]
        TD[Test Fixtures]
    end
    
    subgraph "Utilities"
        PP[Pretty Printer]
        VA[Validation Algorithms]
        SG[Statistics Generator]
    end
    
    TO --> T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 & T9 & T10 & T11 & T12
    T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 & T9 & T10 & T11 & T12 --> DB
    T3 & T6 & T8 & T9 --> SD
    T4 & T5 & T10 --> TD
    T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 & T9 & T10 & T11 & T12 --> VA
    TO --> TP --> RG
    RG --> PP & SG
```

### Architecture Layers

**1. Test Orchestration Layer**
- **Test Runner**: Executes test modules in sequence or parallel, manages test lifecycle
- **Test Parser**: Extracts test results, assertion failures, and metrics from test output
- **Report Generator**: Aggregates results and generates comprehensive audit report

**2. Test Suite Layer**
- **Classification Tests**: Verify sector assignments and financial group mappings
- **Mapping Tests**: Validate item code to semantic name coverage
- **Formula Tests**: Verify ratio formula correctness and edge case handling
- **Calculation Tests**: Validate actual ratio calculations against expected values
- **Filter Tests**: Verify F1-F5 pipeline logic with synthetic peer data
- **Statistical Tests**: Validate benchmark calculations (median, percentiles)
- **Quality Tests**: Assess data completeness and integrity

**3. Data Layer**
- **Production Database**: Read-only access to companies, financial_statements_raw, company_ratios, sector_benchmarks
- **Synthetic Data Generator**: Creates controlled test data with known properties
- **Test Fixtures**: Pre-defined test cases for specific scenarios

**4. Utility Layer**
- **Pretty Printer**: Formats tables, charts, and statistics for reports
- **Validation Algorithms**: Reusable validation logic (bounds checking, statistical tests)
- **Statistics Generator**: Calculates metrics (pass rates, coverage, distributions)


## Components and Interfaces

### Test Suite Modules

#### 1. Sector Classification Test Module

**Purpose**: Validate sector_main and financial_group mappings for all companies

**Interface**:
```python
class SectorClassificationTests:
    def test_load_companies(db: Session) -> List[Company]
    def test_valid_sector_main(companies: List[Company]) -> ValidationResult
    def test_banking_financial_group(companies: List[Company]) -> ValidationResult
    def test_industrial_financial_group(companies: List[Company]) -> ValidationResult
    def test_classification_errors(companies: List[Company]) -> List[ClassificationError]
    def generate_report() -> SectorClassificationReport
```

**Key Algorithms**:
- Sector validation: Check if `sector_main` ∈ VALID_SECTORS (14 sectors)
- Financial group validation: Map sector_main → expected financial_group set
- Error detection: Flag mismatches between sector and financial group

**Test Data Requirements**:
- Read-only access to `companies` table
- Sample size: All active companies (~620)

#### 2. Item Code Mapping Test Module

**Purpose**: Verify item code mapping coverage and identify unmapped codes

**Interface**:
```python
class ItemCodeMappingTests:
    def test_sample_companies(db: Session, n_banking: int = 5, n_industrial: int = 5) -> List[str]
    def test_retrieve_item_codes(db: Session, ticker: str) -> Set[str]
    def test_resolve_mappings(mapper: ItemCodeMapper, item_codes: Set[str]) -> MappingResult
    def calculate_coverage(mapped: int, total: int) -> float
    def identify_unmapped(item_codes: Set[str], mapped: Set[str]) -> List[UnmappedCode]
    def generate_report() -> MappingCoverageReport
```

**Key Algorithms**:
- Coverage calculation: `coverage = (mapped_codes / total_codes) × 100`
- Frequency analysis: Count occurrences of each unmapped code
- Grouping: Aggregate unmapped codes by financial_group

**Test Data Requirements**:
- Sample: 10 companies (5 UFRS_K, 5 XI_29)
- Join: `financial_statements_raw` ⋈ `companies` ⋈ `item_code_mappings`

#### 3. Ratio Formula Validation Test Module

**Purpose**: Verify ratio formulas are mathematically correct and handle edge cases

**Interface**:
```python
class RatioFormulaTests:
    def test_load_ratio_configs() -> Dict[str, RatioConfig]
    def test_formula_callable(config: RatioConfig) -> bool
    def test_formula_with_synthetic_data(config: RatioConfig, data: Dict[str, float]) -> TestResult
    def test_division_by_zero(config: RatioConfig) -> TestResult
    def test_null_handling(config: RatioConfig) -> TestResult
    def test_ttm_aggregation(config: RatioConfig, periods: List[Dict]) -> TestResult
    def generate_report() -> FormulaValidationReport
```

**Key Algorithms**:
- Formula testing: Apply formula to controlled inputs, verify output within tolerance
- Edge case generation: Create test cases with zero denominators, None values
- TTM validation: Verify sum for income statement items, average for balance sheet items

**Test Data Requirements**:
- Synthetic financial data with known relationships:
  - `current_assets = 1000`, `current_liabilities = 500` → `current_ratio = 2.0`
  - `revenue_q1 = 100`, `revenue_q2 = 110`, `revenue_q3 = 105`, `revenue_q4 = 115` → `revenue_ttm = 430`


#### 4. Ratio Calculation Correctness Test Module

**Purpose**: Validate calculated ratios against manually verified expected values

**Interface**:
```python
class RatioCalculationTests:
    def test_select_reference_companies() -> List[str]  # 1 bank, 2 industrial
    def test_manual_calculation(ticker: str, period_key: str) -> Dict[str, float]
    def test_system_calculation(calculator: RatioCalculator, ticker: str, period_key: str) -> Dict[str, float]
    def compare_ratios(expected: Dict, actual: Dict, tolerance: float = 0.02) -> ComparisonResult
    def generate_report() -> RatioCorrectnessReport
```

**Key Algorithms**:
- Percentage difference: `diff = |actual - expected| / expected × 100`
- Tolerance check: Flag if `diff > tolerance_threshold` (2%)
- Specific ratio validations:
  - `current_ratio = current_assets / current_liabilities`
  - `debt_to_equity = total_debt / shareholders_equity`
  - `roe = net_income_ttm / shareholders_equity_avg`

**Test Data Requirements**:
- Reference companies with complete financial data (manually verified)
- Ground truth: Manually calculated ratio values

#### 5. TTM Calculation Test Module

**Purpose**: Verify Trailing Twelve Months aggregation logic

**Interface**:
```python
class TTMCalculationTests:
    def test_select_companies_with_history(min_quarters: int = 4) -> List[str]
    def test_manual_ttm_calculation(ticker: str, item: str) -> float
    def test_system_ttm_calculation(calculator: RatioCalculator, ticker: str) -> float
    def test_banking_exclusion(ticker: str, sector: str) -> bool
    def test_industrial_inclusion(ticker: str, sector: str) -> bool
    def test_minimum_period_requirement(available_periods: int) -> bool
    def generate_report() -> TTMValidationReport
```

**Key Algorithms**:
- Manual TTM for revenue: `sum(last_4_quarters.revenue)`
- System TTM validation: Compare manual vs system calculation within 1% tolerance
- Sector-specific logic:
  - UFRS_K (Banking): Use annual data directly (period = 12)
  - XI_29 (Industrial): Sum last 4 quarterly values
- Minimum periods: Require at least 3 of 4 quarters with non-null data

**Test Data Requirements**:
- Companies with ≥4 quarters of historical data
- Ground truth: Manual quarterly summations

#### 6. Filter Pipeline Test Module

**Purpose**: Verify F1-F5 filter pipeline correctly validates peer data

**Interface**:
```python
class FilterPipelineTests:
    def test_create_synthetic_peers(scenario: str) -> List[PeerData]
    def test_f1_null_filter(peers: List[PeerData]) -> FilterResult
    def test_f2_period_filter(peers: List[PeerData], min_periods: int) -> FilterResult
    def test_f3_economic_bounds(peers: List[PeerData], bounds: Tuple[float, float]) -> FilterResult
    def test_f4_winsorization(peers: List[PeerData]) -> FilterResult
    def test_f5_peer_count(peers: List[PeerData], min_peers: int = 3) -> FilterResult
    def test_full_pipeline(peers: List[PeerData]) -> PipelineResult
    def generate_report() -> FilterPipelineReport
```

**Key Algorithms**:
- **F1 Filter**: Exclude if `value is None` or `not math.isfinite(value)`
- **F2 Filter**: Exclude if `available_periods < min_periods`
- **F3 Filter**: Exclude if `value < min_bound` or `value > max_bound`
- **F4 Filter**: Winsorize: `value = clip(value, P5, P95)` (don't exclude)
- **F5 Filter**: Reject benchmark if `len(included) < 3`

**Synthetic Test Scenarios**:
1. All valid data → All pass F1-F5
2. NULL values → Caught by F1
3. Insufficient periods → Caught by F2
4. Outliers beyond bounds → Caught by F3
5. Extreme outliers → Winsorized by F4
6. Too few peers → Rejected by F5


#### 7. Economic Bounds Validation Test Module

**Purpose**: Verify economic bounds are appropriate and correctly applied

**Interface**:
```python
class EconomicBoundsTests:
    def test_load_bounds() -> Dict[str, Dict[str, Tuple[float, float]]]
    def test_bounds_consistency(bounds: Dict) -> ValidationResult
    def test_banking_sector_bounds(bounds: Dict) -> ValidationResult
    def test_default_bounds_coverage(bounds: Dict) -> ValidationResult
    def test_boundary_edge_cases(ratio_code: str, bounds: Tuple[float, float]) -> TestResult
    def identify_missing_bounds(ratio_codes: List[str], bounds: Dict) -> List[str]
    def generate_report() -> EconomicBoundsReport
```

**Key Algorithms**:
- Consistency check: Verify `min_val < max_val` for all bounds
- Boundary testing: Create test values at `[min - ε, min, max, max + ε]`
- F3 validation: Verify filter correctly includes/excludes based on bounds

**Test Cases**:
```python
# Example: current_ratio bounds (0.1, 15.0)
test_values = [0.09, 0.1, 7.5, 15.0, 15.1]
expected = [EXCLUDE, INCLUDE, INCLUDE, INCLUDE, EXCLUDE]
```

#### 8. Benchmark Accuracy Test Module

**Purpose**: Verify benchmark statistical calculations are correct

**Interface**:
```python
class BenchmarkAccuracyTests:
    def test_select_sectors(min_peers: int = 10) -> List[str]
    def test_retrieve_ratio_values(sector: str, period: str, ratio: str) -> List[float]
    def test_manual_median(values: List[float]) -> float
    def test_manual_percentiles(values: List[float]) -> Tuple[float, float]  # P25, P75
    def test_system_benchmark(calculator: BenchmarkCalculator, sector: str) -> BenchmarkResult
    def compare_calculations(manual: Dict, system: Dict, tolerance: float = 0.1) -> ComparisonResult
    def test_weighted_median(values: List[float], weights: List[float]) -> float
    def generate_report() -> BenchmarkAccuracyReport
```

**Key Algorithms**:
- **Equal-weight median**: `median_ew = np.median(values)`
- **Market-cap weighted median**: Custom weighted quantile algorithm
- **Percentiles**: `p25 = np.percentile(values, 25)`, `p75 = np.percentile(values, 75)`
- **Weighted quantile**:
  ```python
  def weighted_quantile(values, weights, q):
      sorted_indices = np.argsort(values)
      cumulative = 0.0
      for i in sorted_indices:
          cumulative += weights[i] / sum(weights)
          if cumulative >= q:
              return values[i]
  ```

**Validation**:
- Compare manual numpy calculations vs system calculations
- Tolerance: 0.1 (acceptable difference due to floating point)

#### 9. Reliability Assessment Test Module

**Purpose**: Verify reliability classifications are correct

**Interface**:
```python
class ReliabilityAssessmentTests:
    def test_create_peer_sets(sizes: List[int]) -> List[List[PeerData]]
    def test_insufficient_reliability(n_peers: int) -> ReliabilityResult
    def test_low_reliability(n_peers: int) -> ReliabilityResult
    def test_medium_reliability(n_peers: int) -> ReliabilityResult
    def test_high_reliability(n_peers: int) -> ReliabilityResult
    def test_benchmark_rejection(n_peers: int) -> bool
    def generate_report() -> ReliabilityReport
```

**Key Algorithms**:
- Reliability classification:
  ```python
  def assess_reliability(n_peers: int) -> Tuple[str, bool]:
      if n_peers < 3:
          return ("INSUFFICIENT", False)  # can_compute = False
      elif n_peers <= 4:
          return ("LOW", True)
      elif n_peers <= 9:
          return ("MEDIUM", True)
      else:  # n_peers >= 10
          return ("HIGH", True)
  ```

**Test Cases**:
- `n = 2` → INSUFFICIENT, can_compute = False
- `n = 3` → LOW, can_compute = True
- `n = 7` → MEDIUM, can_compute = True
- `n = 15` → HIGH, can_compute = True


#### 10. Data Quality Test Module

**Purpose**: Assess data completeness and identify quality issues

**Interface**:
```python
class DataQualityTests:
    def test_count_rows_per_ticker(db: Session) -> Dict[str, int]
    def test_identify_sparse_data(row_counts: Dict[str, int], min_periods: int = 4) -> List[str]
    def test_calculate_null_percentages(db: Session, fields: List[str]) -> Dict[str, float]
    def test_identify_duplicates(db: Session) -> List[DuplicateRecord]
    def test_companies_with_ratios(db: Session) -> ValidationResult
    def test_sectors_with_benchmarks(db: Session) -> ValidationResult
    def generate_report() -> DataQualityReport
```

**Key Algorithms**:
- NULL percentage: `null_pct = (null_count / total_count) × 100`
- Duplicate detection: `GROUP BY ticker, period_key, item_code HAVING COUNT(*) > 1`
- Completeness checks:
  - Every active company should have ≥1 ratio calculated
  - Every sector with active companies should have ≥1 benchmark
- Critical field threshold: Flag if NULL percentage > 20%

**Test Data Requirements**:
- Full scan of `financial_statements_raw`
- Aggregate queries on `company_ratios` and `sector_benchmarks`

#### 11. Bootstrap Process Test Module

**Purpose**: Verify bootstrap orchestration executes correctly

**Interface**:
```python
class BootstrapProcessTests:
    def test_setup_test_sector(db: Session) -> List[str]  # 5 test companies
    def test_phase1_fetch(engine: BootstrapEngine, tickers: List[str]) -> FetchResult
    def test_phase2_ratios(engine: BootstrapEngine, tickers: List[str]) -> RatioResult
    def test_phase3_benchmarks(engine: BootstrapEngine, sector: str) -> BenchmarkResult
    def test_fetch_log_creation(db: Session, ticker: str) -> FetchLog
    def test_api_failure_handling(engine: BootstrapEngine, mock_api: MockAPI) -> ErrorResult
    def test_rate_limiting(engine: BootstrapEngine) -> RateLimitResult
    def generate_report() -> BootstrapReport
```

**Key Algorithms**:
- Phase verification:
  1. Fetch: Verify `financial_statements_raw` rows inserted
  2. Ratios: Verify `company_ratios` rows inserted
  3. Benchmarks: Verify `sector_benchmarks` rows inserted
- Rate limiting validation: Ensure ≤20 requests per 60 seconds
- Error handling: Verify graceful degradation on API failures

**Test Data Requirements**:
- Isolated test database or test transaction
- Mock API for controlled failure scenarios

#### 12. Sector-Specific Ratio Test Module

**Purpose**: Verify correct ratios are applied per sector

**Interface**:
```python
class SectorSpecificRatioTests:
    def test_select_banking_companies(db: Session, n: int = 3) -> List[str]
    def test_select_industrial_companies(db: Session, n: int = 3) -> List[str]
    def test_banking_ratios_calculated(calculator: RatioCalculator, ticker: str) -> Set[str]
    def test_banking_ratios_excluded(calculator: RatioCalculator, ticker: str) -> Set[str]
    def test_industrial_ratios_calculated(calculator: RatioCalculator, ticker: str) -> Set[str]
    def test_industrial_ratios_excluded(calculator: RatioCalculator, ticker: str) -> Set[str]
    def generate_ratio_application_matrix() -> pd.DataFrame
    def generate_report() -> SectorRatioReport
```

**Key Algorithms**:
- Sector detection: Map `sector_main` → ratio configuration set
- Ratio set validation:
  - Banking (UFRS_K): `BANKING_RATIOS` (net_interest_margin, loan_to_deposit, npl_ratio, capital_adequacy, etc.)
  - Industrial (XI_29): `DEFAULT_RATIOS` (current_ratio, inventory_turnover, receivables_turnover, etc.)
- Exclusion validation:
  - Banking should NOT have `inventory_turnover`
  - Industrial should NOT have `loan_to_deposit`

**Expected Ratio Matrix**:
```
Ratio Code            | Banking | Industrial
---------------------|---------|------------
current_ratio        |    ✗    |     ✓
net_interest_margin  |    ✓    |     ✗
loan_to_deposit      |    ✓    |     ✗
inventory_turnover   |    ✗    |     ✓
```


### Audit Report Generator

**Purpose**: Aggregate test results and generate comprehensive audit report

**Interface**:
```python
class AuditReportGenerator:
    def __init__(self, test_results: Dict[str, TestModuleResult]):
        self.results = test_results
        self.printer = PrettyPrinter()
        
    def generate_executive_summary() -> str
    def calculate_health_score() -> float  # 0-100
    def generate_detailed_findings() -> str
    def generate_priority_matrix() -> str
    def generate_conclusions() -> str
    def generate_recommendations() -> str
    def save_report(path: Path) -> None
```

**Report Structure**:
```markdown
# Financial Engine Audit Report - Phase 1
Generated: 2024-01-15 14:30:00 UTC

## Executive Summary
- Overall Health Score: 87/100
- Critical Issues: 2
- High Priority: 5
- Medium Priority: 12
- Low Priority: 8

## Detailed Findings
### 1. Sector Classification (PASS)
### 2. Item Code Mapping (WARNING - 78% coverage)
### 3. Ratio Formula Validation (PASS)
...

## Priority Matrix
| Issue | Severity | Impact | Requirement |
|-------|----------|--------|-------------|
| ...   | ...      | ...    | ...         |

## Conclusions
...

## Recommendations for Phase 2
...
```

### Pretty Printer Utility

**Purpose**: Format audit data into readable tables, charts, and statistics

**Interface**:
```python
class PrettyPrinter:
    def format_table(data: List[Dict], columns: List[str], align: Dict[str, str]) -> str
    def format_comparison_table(expected: Dict, actual: Dict, deltas: Dict) -> str
    def format_statistics(data: List[float]) -> str  # min, max, mean, median, std
    def format_histogram(data: List[float], bins: int = 10) -> str  # ASCII histogram
    def format_percentage(value: float, decimals: int = 2) -> str
    def format_number(value: float, thousands_sep: bool = True) -> str
    def colorize(text: str, status: str) -> str  # PASS=green, FAIL=red, WARNING=yellow
```

**Example Output**:
```
┌────────────┬──────────┬──────────┬─────────┐
│ Sector     │ Expected │ Actual   │ Delta % │
├────────────┼──────────┼──────────┼─────────┤
│ Banking    │   15.50  │   15.48  │  -0.13  │
│ Industrial │    8.20  │    8.25  │  +0.61  │
└────────────┴──────────┴──────────┴─────────┘

Statistics:
  Min:    5.20
  Max:   18.75
  Mean:  12.34
  Median:11.90
  StdDev: 3.45

Distribution:
  5-7   : ████░░░░░░ (20%)
  7-9   : ████████░░ (40%)
  9-11  : ██████░░░░ (30%)
  11-13 : ██░░░░░░░░ (10%)
```

### Test Result Parser

**Purpose**: Parse test output and extract results, metrics, and failures

**Interface**:
```python
class TestResultParser:
    def parse_test_output(output: str) -> TestSummary
    def extract_test_names(output: str) -> List[str]
    def extract_test_statuses(output: str) -> Dict[str, str]  # name -> PASS/FAIL
    def extract_assertion_failures(output: str) -> List[AssertionFailure]
    def calculate_pass_rate(results: Dict[str, str]) -> float
    def group_by_requirement(results: Dict[str, str]) -> Dict[int, List[TestResult]]
    def identify_critical_failures(results: List[AssertionFailure]) -> List[AssertionFailure]
    def generate_test_summary_report(summary: TestSummary) -> str
```

**AssertionFailure Structure**:
```python
@dataclass
class AssertionFailure:
    test_name: str
    requirement_id: int
    expected: Any
    actual: Any
    message: str
    traceback: str
```


## Data Models

### Test Result Data Models

```python
@dataclass
class ValidationResult:
    """Generic validation result"""
    passed: bool
    total_checked: int
    failures: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]

@dataclass
class ClassificationError:
    """Sector classification error"""
    ticker: str
    company_name: str
    sector_main: str
    financial_group: str
    expected_financial_group: Set[str]
    error_type: str  # "INVALID_SECTOR" | "MISMATCHED_GROUP"

@dataclass
class MappingResult:
    """Item code mapping result"""
    total_codes: int
    mapped_codes: int
    coverage_percentage: float
    unmapped_codes: List[UnmappedCode]

@dataclass
class UnmappedCode:
    """Unmapped item code"""
    item_code: str
    financial_group: str
    frequency: int
    sample_desc_tr: Optional[str]

@dataclass
class TestResult:
    """Individual test result"""
    test_name: str
    requirement_id: int
    status: str  # "PASS" | "FAIL" | "WARNING" | "SKIP"
    execution_time_ms: int
    error_message: Optional[str]
    metrics: Dict[str, Any]

@dataclass
class ComparisonResult:
    """Comparison between expected and actual values"""
    ratio_code: str
    expected: float
    actual: float
    difference: float
    percentage_diff: float
    within_tolerance: bool
    tolerance: float
```

### Report Data Models

```python
@dataclass
class SectorClassificationReport:
    """Sector classification test report"""
    total_companies: int
    correctly_classified: int
    misclassified: int
    accuracy_percentage: float
    errors: List[ClassificationError]
    valid_sectors: List[str]
    sector_distribution: Dict[str, int]

@dataclass
class MappingCoverageReport:
    """Item code mapping coverage report"""
    sample_companies: List[str]
    coverage_by_group: Dict[str, float]  # financial_group -> coverage %
    overall_coverage: float
    unmapped_top20: List[UnmappedCode]
    recommendation: str

@dataclass
class FormulaValidationReport:
    """Ratio formula validation report"""
    total_formulas: int
    passed_formulas: int
    failed_formulas: List[str]
    edge_case_results: Dict[str, TestResult]
    ttm_validation_results: Dict[str, TestResult]
    recommendation: str

@dataclass
class FilterPipelineReport:
    """F1-F5 filter pipeline report"""
    total_peers_input: int
    f1_excluded: int  # NULL/infinite
    f2_excluded: int  # Insufficient periods
    f3_excluded: int  # Economic bounds
    f4_winsorized: int  # Outliers
    f5_rejected: int  # Peer count too low
    final_peers: int
    exclusion_rates: Dict[str, float]

@dataclass
class BenchmarkAccuracyReport:
    """Benchmark calculation accuracy report"""
    sectors_tested: List[str]
    comparisons: List[ComparisonResult]
    median_accuracy: float
    percentile_accuracy: float
    weighted_median_accuracy: float
    recommendation: str

@dataclass
class TestSummary:
    """Overall test execution summary"""
    total_tests: int
    passed: int
    failed: int
    warnings: int
    skipped: int
    pass_rate: float
    execution_time_seconds: float
    timestamp: datetime
    results_by_requirement: Dict[int, List[TestResult]]
```


### Database Schema

The audit system reads from the following production database tables:

#### companies
```sql
CREATE TABLE companies (
    ticker VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(200),
    sector_main VARCHAR(100) NOT NULL,  -- 14 valid sectors
    financial_group VARCHAR(20) NOT NULL,  -- UFRS_K, UFRS_F, UFRS_S, XI_29
    market_cap NUMERIC(20, 2),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_companies_sector ON companies(sector_main);
CREATE INDEX idx_companies_group ON companies(financial_group);
CREATE INDEX idx_companies_active ON companies(is_active);
```

**Valid Sectors** (14):
1. Bankacılık & Finans
2. Teknoloji & İletişim
3. Gıda & İçecek
4. Perakende Ticaret
5. Otomotiv
6. İnşaat & İnşaat Malzemeleri
7. Enerji
8. Kimya & Petrol
9. Metal Ana Sanayi
10. Turizm
11. Tekstil & Deri
12. Ulaştırma & Lojistik
13. Holdingler
14. Diğer

#### financial_statements_raw
```sql
CREATE TABLE financial_statements_raw (
    ticker VARCHAR(10) NOT NULL REFERENCES companies(ticker),
    period_key VARCHAR(20) NOT NULL,  -- '2024Q3', '2024Q4'
    year INTEGER NOT NULL,
    period INTEGER NOT NULL,  -- 3, 6, 9, 12
    financial_group VARCHAR(20) NOT NULL,
    item_code VARCHAR(20) NOT NULL,
    item_desc_tr VARCHAR(500),
    item_desc_en VARCHAR(500),
    value_try NUMERIC(20, 2),
    fetched_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    CONSTRAINT uq_statements_ticker_period_item 
        UNIQUE (ticker, period_key, item_code)
);

CREATE INDEX idx_statements_ticker_period ON financial_statements_raw(ticker, period_key);
CREATE INDEX idx_statements_item_code ON financial_statements_raw(item_code);
CREATE INDEX idx_statements_year_period ON financial_statements_raw(year, period);
```

#### company_ratios
```sql
CREATE TABLE company_ratios (
    ticker VARCHAR(10) NOT NULL REFERENCES companies(ticker),
    period_key VARCHAR(20) NOT NULL,
    ratio_code VARCHAR(50) NOT NULL,
    ratio_value NUMERIC(12, 6),
    is_ttm BOOLEAN NOT NULL DEFAULT FALSE,
    calculation_method VARCHAR(100),
    data_quality_score NUMERIC(3, 2),  -- 0.0 to 1.0
    computed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    CONSTRAINT uq_ratios_ticker_period_code 
        UNIQUE (ticker, period_key, ratio_code)
);

CREATE INDEX idx_ratios_ticker_code ON company_ratios(ticker, ratio_code);
CREATE INDEX idx_ratios_period_code ON company_ratios(period_key, ratio_code);
```

#### sector_benchmarks
```sql
CREATE TABLE sector_benchmarks (
    sector_main VARCHAR(100) NOT NULL,
    ratio_code VARCHAR(50) NOT NULL,
    period_key VARCHAR(20) NOT NULL,
    median_ew NUMERIC(12, 6) NOT NULL,  -- Equal-weight median
    median_wt NUMERIC(12, 6) NOT NULL,  -- Market-cap weighted median
    p25 NUMERIC(12, 6) NOT NULL,  -- 25th percentile
    p75 NUMERIC(12, 6) NOT NULL,  -- 75th percentile
    n_peers INTEGER NOT NULL,  -- Number of peers included
    n_excluded INTEGER NOT NULL,  -- Number of peers excluded by filters
    reliability VARCHAR(20) NOT NULL,  -- HIGH, MEDIUM, LOW, INSUFFICIENT
    computed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_stale BOOLEAN NOT NULL DEFAULT FALSE,
    
    CONSTRAINT uq_benchmark_sector_ratio_period 
        UNIQUE (sector_main, ratio_code, period_key)
);

CREATE INDEX idx_benchmark_sector_period ON sector_benchmarks(sector_main, period_key);
CREATE INDEX idx_benchmark_ratio ON sector_benchmarks(ratio_code);
```

#### item_code_mappings
```sql
CREATE TABLE item_code_mappings (
    financial_group VARCHAR(20) NOT NULL,
    item_code VARCHAR(20) NOT NULL,
    semantic_name VARCHAR(100) NOT NULL,
    description_tr VARCHAR(500),
    description_en VARCHAR(500),
    statement_type VARCHAR(20) NOT NULL,  -- balance_sheet, income_statement
    category VARCHAR(20) NOT NULL,  -- asset, liability, revenue, expense
    is_primary BOOLEAN NOT NULL DEFAULT TRUE,
    priority INTEGER NOT NULL DEFAULT 1000,
    
    CONSTRAINT uq_mappings_group_code UNIQUE (financial_group, item_code),
    CONSTRAINT uq_mappings_group_semantic UNIQUE (financial_group, semantic_name)
);

CREATE INDEX idx_mappings_semantic ON item_code_mappings(semantic_name);
```


## Data Flow

### Overall Data Flow Diagram

```mermaid
sequenceDiagram
    participant TO as Test Orchestrator
    participant TM as Test Module
    participant DB as Production Database
    participant SD as Synthetic Data Gen
    participant VA as Validation Algorithms
    participant TP as Test Parser
    participant RG as Report Generator
    participant PP as Pretty Printer
    
    TO->>TM: Execute Test Module
    TM->>DB: Query Production Data
    DB-->>TM: Return Data
    TM->>SD: Generate Synthetic Data
    SD-->>TM: Return Test Data
    TM->>VA: Validate Data
    VA-->>TM: Return ValidationResult
    TM-->>TO: Return TestResult
    TO->>TP: Parse Test Output
    TP-->>TO: Return TestSummary
    TO->>RG: Generate Report
    RG->>PP: Format Tables/Charts
    PP-->>RG: Return Formatted Output
    RG-->>TO: Save Audit Report
```

### Test Execution Flow

1. **Initialization**
   - Load configuration (database connection, test parameters)
   - Initialize test modules
   - Setup logging and reporting

2. **Test Execution** (Sequential or Parallel)
   - **Requirement 1**: Sector Classification Tests
     - Query: `SELECT ticker, sector_main, financial_group FROM companies WHERE is_active = TRUE`
     - Validate: Check sector_main against valid list, verify financial_group matches sector
     - Output: ValidationResult with errors list
   
   - **Requirement 2**: Item Code Mapping Tests
     - Query: `SELECT DISTINCT item_code FROM financial_statements_raw WHERE ticker IN (samples)`
     - Lookup: Resolve each item_code via ItemCodeMapper
     - Calculate: Coverage percentage, identify unmapped codes
     - Output: MappingResult with coverage statistics
   
   - **Requirement 3**: Ratio Formula Tests
     - Load: DEFAULT_RATIOS and BANKING_RATIOS configurations
     - Generate: Synthetic financial data with known relationships
     - Execute: Apply each ratio formula to synthetic data
     - Validate: Compare results against expected values within tolerance
     - Output: FormulaValidationReport with pass/fail per formula
   
   - **Requirement 4**: Ratio Calculation Tests
     - Select: Reference companies (GARAN for banking, THYAO + EREGL for industrial)
     - Calculate: Manual ratio values from raw data
     - Execute: System ratio calculation via RatioCalculator
     - Compare: Manual vs system with 2% tolerance
     - Output: ComparisonResult with deltas
   
   - **Requirement 5**: TTM Calculation Tests
     - Query: Companies with ≥4 quarters data
     - Calculate: Manual TTM = sum(last 4 quarters revenue)
     - Execute: System TTM calculation
     - Validate: Compare within 1% tolerance
     - Verify: Banking exclusion (use annual), industrial inclusion (use quarterly)
     - Output: TTM ValidationReport
   
   - **Requirement 6**: Filter Pipeline Tests
     - Generate: Synthetic peer data with NULL, outliers, insufficient periods
     - Execute: F1-F5 pipeline on synthetic data
     - Validate: Each filter stage produces expected exclusions
     - Track: Exclusion counts per stage
     - Output: FilterPipelineReport with stage statistics
   
   - **Requirement 7**: Economic Bounds Tests
     - Load: ECONOMIC_BOUNDS configuration
     - Validate: min < max for all bounds
     - Generate: Boundary test cases (min-ε, min, max, max+ε)
     - Execute: F3 filter with boundary values
     - Verify: Correct inclusion/exclusion decisions
     - Output: EconomicBoundsReport
   
   - **Requirement 8**: Benchmark Accuracy Tests
     - Query: Peer ratio values for selected sectors
     - Calculate: Manual median_ew, p25, p75 using numpy
     - Execute: System benchmark calculation
     - Compare: Manual vs system within 0.1 tolerance
     - Output: BenchmarkAccuracyReport
   
   - **Requirement 9**: Reliability Assessment Tests
     - Generate: Peer sets with n=[2,3,5,10,15]
     - Execute: Reliability assessment for each
     - Validate: Correct classification (INSUFFICIENT, LOW, MEDIUM, HIGH)
     - Verify: can_compute flag correctness
     - Output: ReliabilityReport
   
   - **Requirement 10**: Data Quality Tests
     - Query: Count rows per ticker
     - Identify: Companies with < 4 periods
     - Calculate: NULL percentages for critical fields
     - Detect: Duplicates via GROUP BY
     - Verify: All active companies have ratios, all sectors have benchmarks
     - Output: DataQualityReport
   
   - **Requirement 11**: Bootstrap Process Tests
     - Setup: Test sector with 5 companies
     - Execute: Phase 1 (fetch), Phase 2 (ratios), Phase 3 (benchmarks)
     - Verify: Each phase inserts expected rows
     - Validate: Fetch logs created, rate limiting respected
     - Output: BootstrapReport
   
   - **Requirement 12**: Sector-Specific Ratio Tests
     - Select: 3 banking + 3 industrial companies
     - Execute: Ratio calculation for each
     - Verify: Banking has banking ratios, not industrial ratios
     - Verify: Industrial has industrial ratios, not banking ratios
     - Generate: Ratio application matrix
     - Output: SectorRatioReport

3. **Result Aggregation**
   - Parse test output
   - Extract pass/fail status, metrics, assertion failures
   - Calculate overall pass rate
   - Group results by requirement

4. **Report Generation**
   - Calculate health score (weighted by requirement criticality)
   - Generate executive summary
   - Format detailed findings with tables and charts
   - Create priority matrix (severity × impact)
   - Write conclusions and recommendations
   - Save to `AUDIT_REPORT.md` with timestamp


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

The following properties define universal behaviors that must hold for the audit system. These properties will be implemented as property-based tests, each running a minimum of 100 iterations with randomly generated inputs to ensure comprehensive coverage.

### Property 1: Sector Validation Correctness

*For any* company record, the sector validation function SHALL accept the record if and only if the sector_main value is one of the 14 valid main sectors.

**Validates: Requirements 1.2**

**Test Strategy**: Generate random company records with both valid and invalid sector_main values. Verify that validation accepts all valid sectors and rejects all invalid sectors.

### Property 2: Banking Financial Group Classification

*For any* company record where sector_main equals "Bankacılık & Finans", the financial_group SHALL be one of {UFRS_K, UFRS_F, UFRS_S}.

**Validates: Requirements 1.3**

**Test Strategy**: Generate random banking company records. Verify that financial_group is always in the allowed set for banking companies.

### Property 3: Industrial Financial Group Classification

*For any* company record where sector_main is not "Bankacılık & Finans", the financial_group SHALL equal XI_29.

**Validates: Requirements 1.4**

**Test Strategy**: Generate random non-banking company records. Verify that financial_group is always XI_29 for industrial companies.

### Property 4: Classification Error Detection

*For any* company record where the sector_main and financial_group combination is invalid, the validation function SHALL flag it as a classification error.

**Validates: Requirements 1.5**

**Test Strategy**: Generate company records with mismatched sector-financial_group combinations. Verify that all mismatches are detected and flagged.

### Property 5: Ratio Formula Type Correctness

*For any* ratio configuration, the formula function SHALL be callable and return either a numeric value or None when provided with valid financial data.

**Validates: Requirements 3.2**

**Test Strategy**: For each ratio configuration, generate random valid financial data dictionaries. Verify that formula returns correct type (float or None) and never raises exceptions for valid inputs.

### Property 6: Ratio Calculation Accuracy

*For any* synthetic financial data with known mathematical relationships, the calculated ratio value SHALL match the expected value within 0.01 tolerance.

**Validates: Requirements 3.4**

**Test Strategy**: Generate financial data with specific known relationships (e.g., current_assets=1000, current_liabilities=500). Calculate ratios and verify results match expectations (current_ratio=2.0).

### Property 7: TTM Aggregation Correctness

*For any* set of quarterly income statement values, the TTM calculation SHALL equal the sum of the last 4 quarters' values when at least 3 of 4 quarters have non-null data.

**Validates: Requirements 3.7, 5.4**

**Test Strategy**: Generate random quarterly revenue data. Calculate TTM manually and via system. Verify they match within 1% tolerance.

### Property 8: F1 Filter NULL Exclusion

*For any* peer data set, the F1 filter SHALL exclude all peers with NULL or non-finite ratio values and include all peers with finite numeric values.

**Validates: Requirements 6.2**

**Test Strategy**: Generate peer data with mix of valid values, NULL, infinity, and NaN. Verify F1 filter correctly excludes invalid values and preserves valid ones.

### Property 9: F2 Filter Period Validation

*For any* peer data set and minimum period threshold, the F2 filter SHALL exclude all peers with available_periods less than the threshold and include all peers meeting the threshold.

**Validates: Requirements 6.3**

**Test Strategy**: Generate peers with varying period counts (0 to 10). Apply F2 filter with threshold=3. Verify exclusion logic.

### Property 10: F3 Filter Economic Bounds

*For any* ratio value and economic bounds (min_val, max_val), the F3 filter SHALL include the value if min_val ≤ value ≤ max_val and exclude otherwise.

**Validates: Requirements 6.4, 7.6**

**Test Strategy**: Generate random ratio values both inside and outside specified bounds. Verify F3 filter makes correct inclusion/exclusion decisions.


### Property 11: F4 Winsorization Application

*For any* peer data set with at least 5 values, the F4 filter SHALL apply winsorization by clipping values below P5 to P5 and values above P95 to P95, without excluding any peers.

**Validates: Requirements 6.5**

**Test Strategy**: Generate distributions with known outliers. Apply F4 filter. Verify outliers are clipped to P5/P95 percentiles and peer count remains unchanged.

### Property 12: F5 Peer Count Threshold

*For any* peer data set, the F5 validation SHALL set can_compute=True if n_peers ≥ 3 and can_compute=False if n_peers < 3.

**Validates: Requirements 6.6**

**Test Strategy**: Generate peer sets with sizes ranging from 0 to 20. Verify F5 correctly sets can_compute flag based on threshold.

### Property 13: Statistical Median Calculation

*For any* list of numeric values, the calculated median_ew SHALL equal the result of numpy.median() within 0.01 tolerance.

**Validates: Requirements 8.3, 8.6**

**Test Strategy**: Generate random distributions of ratio values. Calculate median manually with numpy and via system. Compare results.

### Property 14: Statistical Percentile Calculation

*For any* list of numeric values, the calculated p25 and p75 SHALL equal numpy.percentile(values, 25) and numpy.percentile(values, 75) respectively within 0.01 tolerance.

**Validates: Requirements 8.4, 8.6**

**Test Strategy**: Generate random distributions. Calculate percentiles manually and via system. Verify they match.

### Property 15: Reliability Classification by Peer Count

*For any* peer count n, the reliability assessment SHALL classify as INSUFFICIENT if n<3, LOW if 3≤n≤4, MEDIUM if 5≤n≤9, and HIGH if n≥10.

**Validates: Requirements 9.2, 9.3, 9.4, 9.5**

**Test Strategy**: Generate peer counts from 0 to 20. Verify reliability classification follows specified thresholds exactly.

### Property 16: Reliability Can-Compute Flag

*For any* peer count n, the can_compute flag SHALL be False if n<3 and True if n≥3.

**Validates: Requirements 9.2, 9.6**

**Test Strategy**: Generate peer counts. Verify can_compute flag is set correctly based on n≥3 threshold.

### Property 17: Banking Ratio Set Application

*For any* banking company (sector_main = "Bankacılık & Finans"), the ratio calculation SHALL apply BANKING_RATIOS configuration and SHALL NOT include inventory_turnover.

**Validates: Requirements 12.3, 12.4**

**Test Strategy**: Generate banking company records. Execute ratio calculation. Verify banking-specific ratios are calculated and industrial-specific ratios are not.

### Property 18: Industrial Ratio Set Application

*For any* industrial company (sector_main ≠ "Bankacılık & Finans"), the ratio calculation SHALL apply DEFAULT_RATIOS configuration and SHALL NOT include loan_to_deposit.

**Validates: Requirements 12.7, 12.8**

**Test Strategy**: Generate industrial company records. Execute ratio calculation. Verify industrial ratios are calculated and banking ratios are not.

### Property 19: Item Code Mapping Round-Trip Consistency

*For any* item_code that successfully maps to a semantic_name, and that semantic_name reverse-maps back to an item_code, the forward and reverse mapping SHALL be consistent (semantic_name → item_code' → semantic_name = original semantic_name).

**Validates: Requirements 16.5, 16.6**

**Test Strategy**: Select mapped item codes. Map to semantic names. Reverse map back. Verify consistency holds for all mappable codes.

### Property 20: Economic Bounds Consistency

*For any* ratio's economic bounds (min_val, max_val), the constraint min_val < max_val SHALL hold.

**Validates: Requirements 7.2**

**Test Strategy**: Load all economic bounds from configuration. Verify min < max for every ratio's bounds definition.

### Property Reflection

After analyzing all properties identified in the prework, the following consolidations were made:

- **Properties 2 & 3** (Banking and Industrial classification) remain separate as they test different logical branches
- **Properties 8, 9, 10** (F1, F2, F3 filters) remain separate as each tests a distinct filter stage with different logic
- **Properties 13 & 14** (Median and Percentile) remain separate as they test different statistical calculations
- **Properties 15 & 16** (Reliability classification and can_compute flag) remain separate as they test two distinct outputs of the same function
- **Properties 17 & 18** (Banking and Industrial ratio sets) remain separate as they test different sector branches

All properties provide unique validation value and cannot be logically reduced without losing test coverage.


## Error Handling

### Error Categories

The audit system identifies and handles four categories of errors:

1. **Data Errors**: Issues with production data (missing values, duplicates, invalid formats)
2. **Calculation Errors**: Discrepancies between expected and actual calculations
3. **Configuration Errors**: Invalid or inconsistent configuration (bounds, mappings)
4. **System Errors**: Database connection failures, API timeouts, unexpected exceptions

### Error Handling Strategy

#### Data Errors

**Detection**:
- NULL value percentage exceeding thresholds
- Duplicate records in financial statements
- Companies without ratios
- Sectors without benchmarks
- Item codes without mappings

**Response**:
- Log error with details (ticker, period, item_code)
- Continue processing remaining data
- Report in Data Quality section of audit report
- Classify severity: CRITICAL (>20% NULL), HIGH (10-20%), MEDIUM (<10%)

**Example**:
```python
def handle_data_error(error: DataError):
    logger.warning(f"Data error: {error.message}")
    error_tracker.record(error)
    # Continue processing
    return None  # Skip this record
```

#### Calculation Errors

**Detection**:
- Ratio value differs from expected by >2% tolerance
- TTM calculation differs from manual by >1% tolerance
- Benchmark median differs from numpy by >0.1 tolerance
- Division by zero in ratio formulas
- Non-finite results (infinity, NaN)

**Response**:
- Capture expected vs actual values
- Calculate percentage difference
- Log comparison details
- Flag test as FAIL if outside tolerance
- Report in Calculation Correctness section

**Example**:
```python
def handle_calculation_error(expected: float, actual: float, tolerance: float):
    diff_pct = abs(actual - expected) / expected * 100
    if diff_pct > tolerance:
        logger.error(f"Calculation error: expected={expected}, actual={actual}, diff={diff_pct:.2f}%")
        return TestResult(status="FAIL", metrics={"diff_pct": diff_pct})
    return TestResult(status="PASS")
```

#### Configuration Errors

**Detection**:
- Economic bounds with min ≥ max
- Missing ratio configurations
- Invalid sector names
- Unmapped item codes

**Response**:
- Validate configuration at startup
- Fail fast if critical configuration is invalid
- Warn if optional configuration is missing
- Report in Configuration Validation section

**Example**:
```python
def validate_economic_bounds(bounds: Dict[str, Tuple[float, float]]):
    errors = []
    for ratio_code, (min_val, max_val) in bounds.items():
        if min_val >= max_val:
            errors.append(f"{ratio_code}: min ({min_val}) >= max ({max_val})")
    if errors:
        raise ConfigurationError("Invalid economic bounds:\n" + "\n".join(errors))
```

#### System Errors

**Detection**:
- Database connection failures
- Query timeouts
- API rate limit exceeded
- Unexpected exceptions during test execution

**Response**:
- Retry transient errors (connection, timeout) up to 3 times
- Log full traceback for debugging
- Fail gracefully and continue with remaining tests
- Report system errors in separate section

**Example**:
```python
def handle_system_error(error: Exception, test_name: str):
    logger.error(f"System error in {test_name}: {error}", exc_info=True)
    if is_transient_error(error):
        return retry_with_backoff(test_name, max_retries=3)
    else:
        return TestResult(status="ERROR", error_message=str(error))
```

### Error Reporting

All errors are aggregated and included in the audit report with the following structure:

```markdown
## Error Summary

### Critical Errors (2)
1. Data Quality: NULL values in total_assets exceed 20% threshold (23.5%)
2. Calculation: TTM revenue calculation off by 12.3% for THYAO 2024Q3

### High Priority Errors (5)
1. Configuration: loan_to_deposit ratio missing economic bounds for Banking sector
2. Data Quality: 47 unmapped item codes in XI_29 financial_group
...

### Medium Priority Errors (12)
...

### Low Priority Warnings (8)
...
```

### Graceful Degradation

The audit system is designed to continue execution even when individual tests fail:

1. **Test Isolation**: Each test module is independent; failure in one does not affect others
2. **Transaction Rollback**: Database reads are non-transactional; no rollback needed
3. **Partial Results**: If a test module fails, remaining modules still execute
4. **Report Generation**: Report is generated even if some tests fail, with ERROR status indicated

**Execution Order** (least to most critical):
1. Bootstrap Process Tests (can fail without affecting other tests)
2. Data Quality Tests (diagnostic, not critical)
3. Sector Classification Tests
4. Item Code Mapping Tests
5. Ratio Formula Tests
6. Filter Pipeline Tests
7. Benchmark Accuracy Tests (most critical)


## Testing Strategy

### Dual Testing Approach

The audit system uses a complementary dual testing strategy:

1. **Property-Based Tests**: Verify universal properties hold across all inputs
2. **Integration Tests**: Validate specific scenarios with real data

Both approaches are necessary for comprehensive coverage. Property-based tests ensure logic is correct across the input space, while integration tests verify the system works with real production data.

### Property-Based Testing

**Scope**: Business logic, validation rules, statistical calculations, filter pipeline logic

**Framework**: Python Hypothesis library

**Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Seed for reproducibility: Use fixed seed for CI/CD, random seed for local development
- Shrinking enabled: Hypothesis will minimize failing examples

**Test Tag Format**:
```python
# Feature: financial-engine-audit-phase1, Property 8: F1 Filter NULL Exclusion
@given(peer_data=st.lists(st.floats(allow_nan=True, allow_infinity=True) | st.none(), min_size=10))
def test_f1_filter_null_exclusion(peer_data):
    """For any peer data set, F1 filter SHALL exclude NULL and non-finite values"""
    ...
```

**Property Test Examples**:

```python
from hypothesis import given, strategies as st
import math

# Property 1: Sector Validation
@given(sector_main=st.text(min_size=1, max_size=100))
def test_sector_validation_correctness(sector_main):
    """Feature: financial-engine-audit-phase1, Property 1: Sector Validation Correctness"""
    VALID_SECTORS = ["Bankacılık & Finans", "Teknoloji & İletişim", ...]  # All 14
    is_valid = validate_sector(sector_main)
    expected_valid = sector_main in VALID_SECTORS
    assert is_valid == expected_valid

# Property 6: Ratio Calculation Accuracy
@given(
    current_assets=st.floats(min_value=1, max_value=1e9),
    current_liabilities=st.floats(min_value=1, max_value=1e9)
)
def test_current_ratio_accuracy(current_assets, current_liabilities):
    """Feature: financial-engine-audit-phase1, Property 6: Ratio Calculation Accuracy"""
    data = {"current_assets": current_assets, "current_liabilities": current_liabilities}
    calculated = calculate_ratio("current_ratio", data)
    expected = current_assets / current_liabilities
    assert abs(calculated - expected) < 0.01

# Property 10: F3 Filter Economic Bounds
@given(
    value=st.floats(min_value=-100, max_value=100),
    min_bound=st.floats(min_value=-50, max_value=0),
    max_bound=st.floats(min_value=0, max_value=50)
)
def test_f3_economic_bounds(value, min_bound, max_bound):
    """Feature: financial-engine-audit-phase1, Property 10: F3 Filter Economic Bounds"""
    assume(min_bound < max_bound)  # Precondition
    included = f3_filter(value, min_bound, max_bound)
    expected = min_bound <= value <= max_bound
    assert included == expected
```

### Integration Testing

**Scope**: End-to-end workflows, database operations, real data validation, API interactions

**Framework**: pytest

**Test Data**:
- Real production data (read-only queries)
- Test fixtures (pre-defined companies with known characteristics)
- Sample datasets (representative subset of production data)

**Integration Test Examples**:

```python
import pytest
from sqlalchemy.orm import Session

@pytest.fixture
def db_session():
    """Provide database session for tests"""
    session = SessionLocal()
    yield session
    session.close()

def test_ratio_calculation_garan(db_session: Session):
    """Integration test: Verify GARAN banking ratios match manually calculated values"""
    ticker = "GARAN"
    period_key = "2024Q3"
    
    # Manually calculated expected values
    expected = {
        "loan_to_deposit": 1.15,
        "npl_ratio": 0.023,
        "roe": 0.18
    }
    
    # System calculation
    calculator = RatioCalculator(db_session)
    results = calculator.calculate_company_ratios(ticker, period_key)
    actual = {r.ratio_code: r.ratio_value for r in results if r.success}
    
    # Compare
    for ratio_code, expected_value in expected.items():
        actual_value = actual[ratio_code]
        diff_pct = abs(actual_value - expected_value) / expected_value * 100
        assert diff_pct < 2.0, f"{ratio_code}: {actual_value} vs {expected_value} ({diff_pct:.2f}%)"

def test_bootstrap_process_single_sector(db_session: Session):
    """Integration test: Verify bootstrap executes for test sector"""
    test_sector = "Teknoloji & İletişim"
    test_companies = ["ASELS", "LOGO", "ARENA", "ESCOM", "INDES"]
    
    engine = BootstrapEngine(sectors=[test_sector])
    
    # Phase 1: Fetch
    fetch_result = engine._phase_fetch()
    assert fetch_result.successful_fetches >= 3  # At least 3/5 succeed
    
    # Phase 2: Ratios
    ratio_result = engine._phase_calculate_ratios()
    assert ratio_result.total_ratios_calculated > 0
    
    # Phase 3: Benchmarks
    benchmark_result = engine._phase_calculate_benchmarks()
    assert benchmark_result.total_benchmarks_created > 0
```

### Test Data Strategy

#### Synthetic Data Generation

**Purpose**: Create controlled test data with known properties for property-based tests

**Generators**:

```python
from hypothesis import strategies as st

# Financial data generator
financial_data = st.fixed_dictionaries({
    "current_assets": st.floats(min_value=1e3, max_value=1e9),
    "current_liabilities": st.floats(min_value=1e3, max_value=1e9),
    "total_assets": st.floats(min_value=1e4, max_value=1e10),
    "total_liabilities": st.floats(min_value=1e3, max_value=1e10),
    "shareholders_equity": st.floats(min_value=1e3, max_value=1e9),
    "revenue_ttm": st.floats(min_value=1e4, max_value=1e10),
    "net_income_ttm": st.floats(min_value=-1e8, max_value=1e9),
})

# Peer data generator (for filter tests)
peer_data = st.lists(
    st.fixed_dictionaries({
        "ticker": st.text(min_size=3, max_size=6, alphabet=st.characters(whitelist_categories=('Lu',))),
        "ratio_value": st.one_of(
            st.none(),  # NULL values
            st.floats(allow_nan=True, allow_infinity=True),  # Valid and invalid floats
        ),
        "market_cap": st.floats(min_value=1e6, max_value=1e11),
        "available_periods": st.integers(min_value=0, max_value=12)
    }),
    min_size=5,
    max_size=50
)

# Company record generator
company_record = st.fixed_dictionaries({
    "ticker": st.text(min_size=3, max_size=6, alphabet=st.characters(whitelist_categories=('Lu',))),
    "sector_main": st.sampled_from(VALID_SECTORS + ["Invalid Sector", "Fake Sector"]),
    "financial_group": st.sampled_from(["UFRS_K", "UFRS_F", "UFRS_S", "XI_29", "INVALID"]),
})
```

#### Real Data Sampling

**Purpose**: Validate system with actual production data

**Sampling Strategy**:
- **Stratified sampling**: Ensure representation from all 14 sectors
- **Reference companies**: Select well-known companies with complete data (GARAN, THYAO, EREGL, PETKM, etc.)
- **Edge cases**: Include companies with sparse data, recent IPOs, delisted companies

**Sample Selection**:
```python
def select_test_sample(db: Session) -> List[str]:
    """Select representative sample of companies for testing"""
    samples = []
    
    # 1 banking company with complete data
    samples.append("GARAN")  # Garanti BBVA
    
    # 2 industrial companies with complete data
    samples.extend(["THYAO", "EREGL"])  # Türk Hava Yolları, Ereğli Demir Çelik
    
    # 1 company per remaining sector (stratified)
    for sector in VALID_SECTORS:
        if sector != "Bankacılık & Finans":  # Already have GARAN
            company = db.query(Company.ticker)\
                .filter(Company.sector_main == sector)\
                .filter(Company.is_active == True)\
                .order_by(Company.market_cap.desc())\
                .first()
            if company:
                samples.append(company.ticker)
    
    return samples
```


### Test Execution

**Test Runner**: pytest with custom plugins

**Execution Modes**:
1. **Sequential**: Run all tests in order (default for full audit)
2. **Parallel**: Run independent test modules in parallel (faster, use pytest-xdist)
3. **Selective**: Run specific requirements only (for debugging)

**Command Examples**:
```bash
# Full audit (sequential)
pytest tests/audit/ -v --tb=short --report=AUDIT_REPORT.md

# Fast audit (parallel)
pytest tests/audit/ -n auto -v

# Specific requirement
pytest tests/audit/test_sector_classification.py -v

# Property tests only
pytest tests/audit/ -m property -v

# Integration tests only
pytest tests/audit/ -m integration -v
```

**Test Markers**:
```python
@pytest.mark.property
@pytest.mark.requirement_1
def test_sector_validation():
    ...

@pytest.mark.integration
@pytest.mark.requirement_4
@pytest.mark.slow
def test_ratio_calculation_accuracy():
    ...
```

### Test Configuration

Configuration is managed via `tests/audit/config.yaml`:

```yaml
# Database connection
database:
  url: "postgresql://user:pass@localhost:5432/hissepro"
  pool_size: 5
  read_only: true

# Test execution
execution:
  mode: sequential  # sequential | parallel | selective
  parallel_workers: 4
  timeout_seconds: 300

# Property-based test settings
hypothesis:
  max_examples: 100
  deadline_ms: 10000  # 10 seconds per test case
  seed: null  # null for random, integer for reproducibility

# Tolerance thresholds
tolerances:
  ratio_calculation: 0.02  # 2%
  ttm_calculation: 0.01  # 1%
  benchmark_statistical: 0.1  # 0.1 absolute

# Data quality thresholds
data_quality:
  null_percentage_critical: 20.0
  null_percentage_warning: 10.0
  minimum_periods: 4
  mapping_coverage_threshold: 80.0

# Sample sizes
samples:
  mapping_test_companies: 10
  reference_companies: 3
  sector_benchmark_min_peers: 10

# Economic bounds (sector-specific)
economic_bounds:
  _default:
    current_ratio: [0.1, 15.0]
    debt_to_equity: [-2.0, 25.0]
    roe: [-1.0, 1.5]
    # ... (all default ratios)
  
  "Bankacılık & Finans":
    loan_to_deposit: [0.3, 2.5]
    npl_ratio: [0.0, 0.25]
    capital_adequacy: [0.08, 0.4]
    # ... (all banking ratios)

# Reporting
reporting:
  output_path: "AUDIT_REPORT.md"
  include_timestamps: true
  include_traceback: false  # Only for errors
  table_format: "ascii"  # ascii | markdown | html
  
# Logging
logging:
  level: INFO
  file: "audit_execution.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Unit Tests vs Integration Tests Balance

**Unit Tests** (Property-Based):
- **What**: Test individual functions and business logic in isolation
- **How**: Use synthetic data with known properties
- **Coverage**: Universal behaviors, edge cases, boundary conditions
- **Speed**: Fast (milliseconds per test)
- **Examples**: Filter logic, validation rules, formula correctness

**Integration Tests**:
- **What**: Test component interactions and workflows with real data
- **How**: Use production database (read-only) and sample companies
- **Coverage**: Data flow, database queries, end-to-end scenarios
- **Speed**: Slower (seconds to minutes per test)
- **Examples**: Ratio calculation for specific companies, bootstrap process, data quality checks

**Balance Principle**:
- Unit tests provide **breadth**: Many inputs, comprehensive logic coverage
- Integration tests provide **depth**: Real-world scenarios, data validation
- Both are essential: Unit tests catch logic bugs, integration tests catch integration issues

**Test Count Distribution** (Target):
- Property-based unit tests: ~20 tests × 100 iterations = 2000 test cases
- Integration tests: ~15 tests with real data
- Total: ~2015 test executions per full audit run

### Mocking Strategy

**What to Mock**:
- External API calls (İş Yatırım API) in bootstrap tests
- Time-dependent functions (datetime.now()) for reproducibility
- Random number generators (for deterministic synthetic data when needed)

**What NOT to Mock**:
- Database queries (use real test database or read-only production)
- Calculation logic (test the actual implementation)
- Configuration loading (test with actual config files)

**Mock Examples**:

```python
from unittest.mock import Mock, patch

# Mock API for bootstrap tests
@patch('services.isyatirim_client.fetch_mali_tablo')
def test_bootstrap_api_failure_handling(mock_fetch):
    mock_fetch.return_value = APIResult(success=False, error="API timeout")
    
    engine = BootstrapEngine(sectors=["Test Sector"])
    result = engine._phase_fetch()
    
    assert result.failed_fetches > 0
    assert "API timeout" in result.error_messages

# Mock time for reproducibility
@patch('datetime.datetime')
def test_period_calculation(mock_datetime):
    mock_datetime.utcnow.return_value = datetime(2024, 5, 15)
    
    periods = calculate_periods_to_fetch()
    
    # Expected: 2024Q1 (latest with reporting lag)
    assert periods[0] == (2024, 3)
```


## Key Algorithms

### F1-F5 Filter Pipeline

The benchmark calculation filter pipeline is a 5-stage process that validates peer data quality:

```python
def run_filter_pipeline(
    peers: List[PeerData], 
    ratio_code: str, 
    sector_main: str,
    min_periods: int = 1
) -> FilterResult:
    """
    Execute F1-F5 filter pipeline for peer validation
    
    Returns:
        FilterResult with included/excluded peers and reliability assessment
    """
    included = []
    excluded = []
    
    for peer in peers:
        # F1: NULL / Infinite values filter
        if peer.value is None or not math.isfinite(peer.value):
            excluded.append({
                "ticker": peer.ticker,
                "value": peer.value,
                "reason": "F1_NULL_OR_INFINITE"
            })
            continue
        
        # F2: Minimum reporting periods filter (data quality)
        if peer.available_periods < min_periods:
            excluded.append({
                "ticker": peer.ticker,
                "value": peer.value,
                "reason": f"F2_INSUFFICIENT_PERIODS({peer.available_periods})"
            })
            continue
        
        # F3: Economic validity filter (sector-specific bounds)
        is_valid, reason = check_economic_bounds(
            ratio_code, peer.value, sector_main
        )
        if not is_valid:
            excluded.append({
                "ticker": peer.ticker,
                "value": peer.value,
                "reason": f"F3_{reason}"
            })
            continue
        
        # Passed F1-F3, add to included list
        included.append({
            "ticker": peer.ticker,
            "value": peer.value,
            "market_cap": peer.market_cap
        })
    
    # F4: Statistical outlier removal (Winsorization at P5-P95)
    if len(included) >= 5:
        values = [p["value"] for p in included]
        p5 = np.percentile(values, 5)
        p95 = np.percentile(values, 95)
        
        # Apply winsorization (clip, don't exclude)
        for peer in included:
            if peer["value"] < p5:
                peer["value"] = p5
                peer["winsorized"] = "P5"
            elif peer["value"] > p95:
                peer["value"] = p95
                peer["winsorized"] = "P95"
    
    # F5: Minimum peer count validation
    n_peers = len(included)
    reliability = assess_reliability(n_peers)
    can_compute = n_peers >= 3
    
    return FilterResult(
        included=included,
        excluded=excluded,
        n_peers=n_peers,
        reliability=reliability,
        can_compute=can_compute
    )
```

**Algorithm Complexity**:
- **Time**: O(n) for F1-F3 filtering + O(n log n) for F4 percentile calculation = O(n log n)
- **Space**: O(n) for included/excluded lists

**Edge Cases**:
- Empty input: Returns n_peers=0, can_compute=False
- All peers excluded by F1-F3: Returns empty included list, can_compute=False
- Fewer than 5 peers: Skips F4 winsorization
- Exactly 3 peers: can_compute=True, reliability=LOW

### TTM Calculation Algorithm

Trailing Twelve Months (TTM) calculation aggregates quarterly or annual data:

```python
def calculate_ttm_values(
    periods_data: Dict[Tuple[int, int], Dict[str, float]],
    financial_group: str
) -> Dict[str, float]:
    """
    Calculate TTM values for income statement items
    
    Args:
        periods_data: {(year, period): {item: value}} mapping
        financial_group: UFRS_K (banking) or XI_29 (industrial)
    
    Returns:
        {item_ttm: value} mapping for TTM calculations
    """
    ttm_data = {}
    
    # Banking: Use annual data directly (period = 12)
    if financial_group in ["UFRS_K", "UFRS_F", "UFRS_S"]:
        annual_periods = [(y, p) for (y, p) in periods_data.keys() if p == 12]
        if not annual_periods:
            return ttm_data
        
        latest_annual = max(annual_periods)
        for item, value in periods_data[latest_annual].items():
            if item in INCOME_STATEMENT_ITEMS:
                ttm_data[f"{item}_ttm"] = value
        
        return ttm_data
    
    # Industrial: Sum last 4 quarters
    sorted_periods = sorted(periods_data.keys(), reverse=True)
    if len(sorted_periods) < 4:
        return ttm_data
    
    last_4_periods = sorted_periods[:4]
    
    # Sum income statement items over 4 quarters
    for item in INCOME_STATEMENT_ITEMS:
        ttm_value = 0
        periods_with_data = 0
        
        for period_key in last_4_periods:
            period_data = periods_data[period_key]
            if item in period_data and period_data[item] is not None:
                ttm_value += period_data[item]
                periods_with_data += 1
        
        # Require at least 3 of 4 quarters with data
        if periods_with_data >= 3:
            ttm_data[f"{item}_ttm"] = ttm_value
    
    return ttm_data
```

**Algorithm Characteristics**:
- **Sector-Specific Logic**: Banking uses annual, industrial uses quarterly
- **Minimum Data Requirement**: 3 of 4 quarters for industrial
- **Items Affected**: Only income statement items (revenue, net_income, operating_income, etc.)
- **Balance Sheet Handling**: Uses average of last 2 periods (not TTM)

**Example**:
```python
# Industrial company (XI_29)
periods_data = {
    (2024, 9): {"revenue": 250, "net_income": 20},
    (2024, 6): {"revenue": 230, "net_income": 18},
    (2024, 3): {"revenue": 210, "net_income": 15},
    (2023, 12): {"revenue": 270, "net_income": 22},
}

# TTM calculation
revenue_ttm = 250 + 230 + 210 + 270 = 960
net_income_ttm = 20 + 18 + 15 + 22 = 75

# Banking company (UFRS_K)
periods_data = {
    (2024, 12): {"revenue": 1000, "net_income": 80},
    (2023, 12): {"revenue": 950, "net_income": 75},
}

# TTM calculation
revenue_ttm = 1000  # Use latest annual directly
net_income_ttm = 80
```


### Benchmark Calculation Algorithm

Benchmark calculation computes equal-weight and market-cap weighted medians:

```python
def calculate_benchmarks(
    filter_result: FilterResult,
    sector_main: str,
    ratio_code: str,
    period_key: str
) -> BenchmarkResult:
    """
    Calculate sector benchmarks after filtering
    
    Args:
        filter_result: Output from F1-F5 pipeline
        sector_main: Sector name
        ratio_code: Ratio identifier
        period_key: Period identifier (e.g., "2024Q3")
    
    Returns:
        BenchmarkResult with median_ew, median_wt, p25, p75
    """
    values = [p["value"] for p in filter_result.included]
    market_caps = [p["market_cap"] for p in filter_result.included]
    
    # Equal-weight median (standard median)
    median_ew = float(np.median(values))
    
    # Market-cap weighted median (weighted quantile at 0.5)
    median_wt = weighted_quantile(values, market_caps, 0.5)
    
    # Percentiles (always equal-weight)
    p25 = float(np.percentile(values, 25))
    p75 = float(np.percentile(values, 75))
    
    return BenchmarkResult(
        sector_main=sector_main,
        ratio_code=ratio_code,
        period_key=period_key,
        median_ew=median_ew,
        median_wt=median_wt,
        p25=p25,
        p75=p75,
        n_peers=filter_result.n_peers,
        n_excluded=len(filter_result.excluded),
        reliability=filter_result.reliability,
        computed_at=datetime.utcnow()
    )


def weighted_quantile(
    values: List[float],
    weights: List[float],
    quantile: float
) -> float:
    """
    Calculate weighted quantile using cumulative weight method
    
    Args:
        values: Data values
        weights: Corresponding weights (e.g., market caps)
        quantile: Target quantile (0.5 for median)
    
    Returns:
        Weighted quantile value
    
    Algorithm:
        1. Normalize weights to sum to 1
        2. Sort values with corresponding weights
        3. Calculate cumulative weights
        4. Find first value where cumulative weight >= quantile
    
    Example:
        values = [10, 20, 30, 40, 50]
        weights = [1, 1, 3, 1, 1]  # Middle value has 3x weight
        weighted_median = 30 (due to higher weight)
        
        Equal-weight median would be 30 as well (coincidentally)
        But for different weights:
        weights = [1, 1, 1, 1, 5]  # Last value has 5x weight
        weighted_median = 50
    """
    if not values or not weights:
        return 0.0
    
    # Normalize weights
    total_weight = sum(weights)
    if total_weight == 0:
        # Fall back to equal-weight if all weights are zero
        return float(np.percentile(values, quantile * 100))
    
    normalized_weights = [w / total_weight for w in weights]
    
    # Sort by values, carrying weights along
    sorted_indices = np.argsort(values)
    sorted_values = [values[i] for i in sorted_indices]
    sorted_weights = [normalized_weights[i] for i in sorted_indices]
    
    # Calculate cumulative weights
    cumulative = 0.0
    for i, (value, weight) in enumerate(zip(sorted_values, sorted_weights)):
        cumulative += weight
        if cumulative >= quantile:
            return float(value)
    
    # Fallback: return last value
    return float(sorted_values[-1])
```

**Algorithm Complexity**:
- **Time**: O(n log n) for sorting, O(n) for cumulative sum = O(n log n)
- **Space**: O(n) for sorted arrays

**Comparison: Equal-Weight vs Market-Cap Weighted**:
```
Example: ROE values for Technology sector

Company  | ROE   | Market Cap (TRY)
---------|-------|------------------
ASELS    | 15%   | 50 billion
LOGO     | 8%    | 2 billion
ARENA    | 12%   | 1 billion
ESCOM    | 6%    | 500 million
INDES    | 10%   | 300 million

Equal-weight median: 10% (middle value when sorted)
Market-cap weighted median: ~14% (ASELS dominates due to size)

Use Cases:
- median_ew: Fair comparison (each company equal)
- median_wt: Market-representative (larger companies more influential)
```

### Round-Trip Mapping Verification

Verify item code mapping consistency:

```python
def verify_mapping_round_trip(
    mapper: ItemCodeMapper,
    financial_group: str
) -> RoundTripResult:
    """
    Verify forward and reverse mapping consistency
    
    Algorithm:
        1. Get all mapped item_codes for financial_group
        2. For each item_code:
           a. Map item_code → semantic_name (forward)
           b. Map semantic_name → item_code (reverse)
           c. Check if forward(reverse(semantic_name)) == semantic_name
        3. Calculate consistency rate
    
    Property:
        For all mapped item_codes, forward ∘ reverse should be identity
        i.e., map_to_semantic(map_to_item_code(semantic_name)) == semantic_name
    
    Note: This is a round-trip property test
    """
    mappings = mapper.get_all_mappings(financial_group)
    consistent = 0
    inconsistent = []
    
    for item_code, semantic_name in mappings.items():
        # Forward: item_code → semantic_name
        forward = mapper.get_semantic_name(item_code, financial_group)
        
        if forward != semantic_name:
            inconsistent.append({
                "item_code": item_code,
                "expected_semantic": semantic_name,
                "actual_semantic": forward,
                "type": "FORWARD_MISMATCH"
            })
            continue
        
        # Reverse: semantic_name → item_code
        reverse = mapper.get_item_code(semantic_name, financial_group)
        
        if reverse is None:
            inconsistent.append({
                "item_code": item_code,
                "semantic_name": semantic_name,
                "type": "NO_REVERSE_MAPPING"
            })
            continue
        
        # Round-trip: semantic_name → item_code → semantic_name
        round_trip = mapper.get_semantic_name(reverse, financial_group)
        
        if round_trip == semantic_name:
            consistent += 1
        else:
            inconsistent.append({
                "item_code": item_code,
                "semantic_name": semantic_name,
                "reverse_item_code": reverse,
                "round_trip_semantic": round_trip,
                "type": "ROUND_TRIP_MISMATCH"
            })
    
    total = len(mappings)
    consistency_rate = (consistent / total * 100) if total > 0 else 0
    
    return RoundTripResult(
        total_mappings=total,
        consistent=consistent,
        inconsistent_mappings=inconsistent,
        consistency_rate=consistency_rate
    )
```

**Expected Consistency**: ≥95% (some one-to-many mappings may be intentional)


## Report Format

### Audit Report Structure

The audit report is generated in Markdown format with the following sections:

```markdown
# Financial Engine Audit Report - Phase 1

**Generated**: 2024-01-15 14:30:00 UTC  
**System**: HissePro Financial Analysis Engine  
**Audit Period**: 2024Q1 - 2024Q3  
**Database**: production (read-only)

---

## Executive Summary

### Overall Health Score: 87/100

The Financial Analysis Engine demonstrates **strong overall performance** with 87% health score. The system correctly processes financial data across 14 sectors and 620+ companies. Key strengths include accurate ratio calculations and robust filter pipeline logic. Primary areas for improvement are item code mapping coverage (78%) and handling of sparse historical data.

### Issue Summary

| Severity  | Count | Examples |
|-----------|-------|----------|
| CRITICAL  | 2     | NULL values >20% in total_assets field |
| HIGH      | 5     | Item code mapping coverage below 80% |
| MEDIUM    | 12    | TTM calculation warnings for specific companies |
| LOW       | 8     | Minor data quality issues |

### Pass Rate by Category

```
Classification Tests:    ████████████████████ 100% (5/5)
Mapping Tests:           ████████████████░░░░  78% (7/9)
Formula Tests:           ████████████████████ 100% (12/12)
Calculation Tests:       ███████████████████░  96% (25/26)
Filter Pipeline Tests:   ████████████████████ 100% (8/8)
Benchmark Tests:         ███████████████████░  94% (15/16)
Data Quality Tests:      ████████████░░░░░░░░  67% (8/12)
```

---

## Detailed Findings

### 1. Sector Classification Tests (PASS)

**Status**: ✅ PASS  
**Health Score**: 100/100  
**Requirement**: 1

#### Summary
All 620 active companies have valid sector classifications. No mismatches detected between sector_main and financial_group assignments.

#### Metrics
- Total companies: 620
- Correctly classified: 620 (100%)
- Misclassified: 0
- Invalid sector_main: 0

#### Sector Distribution
┌────────────────────────────────┬───────┬─────────┐
│ Sector                         │ Count │ % Total │
├────────────────────────────────┼───────┼─────────┤
│ Bankacılık & Finans            │   47  │   7.6%  │
│ Teknoloji & İletişim           │   32  │   5.2%  │
│ Gıda & İçecek                  │   28  │   4.5%  │
│ Perakende Ticaret              │   41  │   6.6%  │
│ İnşaat & İnşaat Malzemeleri    │   58  │   9.4%  │
│ Holdingler                     │   89  │  14.4%  │
│ ... (remaining 8 sectors)      │  325  │  52.4%  │
└────────────────────────────────┴───────┴─────────┘

#### Financial Group Validation
- Banking companies (47): All have UFRS_K/F/S ✅
- Industrial companies (573): All have XI_29 ✅

**Recommendation**: No action required. Sector classification is accurate.

---

### 2. Item Code Mapping Tests (WARNING)

**Status**: ⚠️ WARNING  
**Health Score**: 78/100  
**Requirement**: 2

#### Summary
Item code mapping coverage is **78%**, below the 80% threshold. 47 unique item codes are unmapped in XI_29 financial group, primarily related to detailed expense breakdowns and footnote items.

#### Coverage by Financial Group
┌──────────────────┬─────────────┬────────────┬───────────┐
│ Financial Group  │ Total Codes │ Mapped     │ Coverage  │
├──────────────────┼─────────────┼────────────┼───────────┤
│ UFRS_K (Banking) │     182     │    168     │   92.3%   │
│ XI_29 (Industrial│     247     │    193     │   78.1%   │
└──────────────────┴─────────────┴────────────┴───────────┘

#### Top 20 Unmapped Item Codes
┌───────────┬──────────────────────────────────────┬───────────┐
│ Item Code │ Description (TR)                     │ Frequency │
├───────────┼──────────────────────────────────────┼───────────┤
│ 5.01.051  │ Pazarlama Satış Dağıtım Giderleri    │    247    │
│ 5.01.052  │ Genel Yönetim Giderleri              │    238    │
│ 5.01.053  │ Araştırma Geliştirme Giderleri       │    156    │
│ 5.02.010  │ Diğer Faaliyetlerden Gelir/Gider     │    189    │
│ ... (16 more)                                             │
└───────────┴──────────────────────────────────────┴───────────┘

**Recommendation**: HIGH priority. Expand XI_29 item code mappings to achieve ≥80% coverage. Focus on high-frequency unmapped codes first.

---

### 3. Ratio Formula Validation Tests (PASS)

**Status**: ✅ PASS  
**Health Score**: 100/100  
**Requirement**: 3

#### Summary
All ratio formulas (17 default + 7 banking = 24 total) passed validation tests. Formulas correctly handle edge cases including division by zero, NULL values, and TTM aggregation.

#### Test Results by Category
┌──────────────────────────┬────────┬────────┬──────────┐
│ Test Category            │ Passed │ Failed │ Coverage │
├──────────────────────────┼────────┼────────┼──────────┤
│ Formula Callability      │   24   │   0    │   100%   │
│ Synthetic Data Accuracy  │   24   │   0    │   100%   │
│ Division by Zero Handling│   24   │   0    │   100%   │
│ NULL Handling            │   24   │   0    │   100%   │
│ TTM Aggregation Logic    │    8   │   0    │   100%   │
└──────────────────────────┴────────┴────────┴──────────┘

#### Property Test Coverage
- Total property tests: 5
- Iterations per test: 100
- Total test cases: 500
- All passed ✅

**Recommendation**: No action required. Ratio formulas are mathematically correct.

---

### 4. Ratio Calculation Correctness Tests (PASS)

**Status**: ✅ PASS (with 1 WARNING)  
**Health Score**: 96/100  
**Requirement**: 4

#### Summary
Ratio calculations match manually verified expected values within 2% tolerance for reference companies. One warning detected for THYAO operating_margin (2.3% difference, likely due to data timing).

#### Reference Company Results

**GARAN (Banking)**
┌───────────────────────┬──────────┬──────────┬─────────┬────────┐
│ Ratio                 │ Expected │ Actual   │ Delta   │ Status │
├───────────────────────┼──────────┼──────────┼─────────┼────────┤
│ loan_to_deposit       │   1.150  │   1.148  │  -0.17% │   ✅   │
│ npl_ratio             │   0.023  │   0.023  │   0.00% │   ✅   │
│ roe                   │   0.180  │   0.182  │  +1.11% │   ✅   │
│ capital_adequacy      │   0.165  │   0.165  │   0.00% │   ✅   │
└───────────────────────┴──────────┴──────────┴─────────┴────────┘

**THYAO (Industrial - Airline)**
┌───────────────────────┬──────────┬──────────┬─────────┬────────┐
│ Ratio                 │ Expected │ Actual   │ Delta   │ Status │
├───────────────────────┼──────────┼──────────┼─────────┼────────┤
│ current_ratio         │   0.850  │   0.847  │  -0.35% │   ✅   │
│ debt_to_equity        │   4.200  │   4.189  │  -0.26% │   ✅   │
│ operating_margin      │   0.125  │   0.122  │  -2.40% │   ⚠️   │
│ roe                   │   0.320  │   0.325  │  +1.56% │   ✅   │
└───────────────────────┴──────────┴──────────┴─────────┴────────┘

**Recommendation**: MEDIUM priority. Investigate THYAO operating_margin calculation timing. Otherwise, calculations are accurate.

---

[Continue with remaining test modules...]

---

## Priority Matrix

Issues ranked by severity × impact:

| Rank | Issue | Severity | Impact | Requirement | Action |
|------|-------|----------|--------|-------------|--------|
| 1 | NULL values in total_assets >20% | CRITICAL | HIGH | 10.3 | Data quality fix |
| 2 | XI_29 mapping coverage 78% | HIGH | HIGH | 2.4 | Expand mappings |
| 3 | TTM calculation failures (3 companies) | HIGH | MEDIUM | 5.8 | Investigate data |
| ... | ... | ... | ... | ... | ... |

---

## Conclusions

The Financial Analysis Engine demonstrates strong core functionality with 87% overall health score. Key findings:

1. **Strengths**:
   - Sector classification is 100% accurate across all companies
   - Ratio formulas are mathematically correct and handle edge cases properly
   - Filter pipeline logic correctly validates peer data
   - Benchmark statistical calculations match reference implementations

2. **Areas for Improvement**:
   - Item code mapping coverage needs expansion (78% → 80%+ target)
   - Data quality issues with NULL values in some critical fields
   - TTM calculations fail for companies with sparse historical data

3. **System Reliability**:
   - Filter pipeline effectively excludes invalid data (F1-F5 stages)
   - Benchmark reliability classifications are accurate
   - Ratio calculations consistent across sectors

---

## Recommendations for Phase 2

### High Priority
1. **Expand XI_29 Item Code Mappings**: Add mappings for 47 unmapped codes, prioritize high-frequency codes
2. **Data Quality Improvements**: Address NULL value issues in total_assets and other critical fields
3. **TTM Calculation Robustness**: Improve handling of companies with incomplete quarterly data

### Medium Priority
4. **Bootstrap Process Error Handling**: Enhance API failure recovery and retry logic
5. **Documentation**: Add inline documentation for complex ratio formulas
6. **Performance**: Optimize benchmark calculations for large peer sets

### Low Priority
7. **Monitoring**: Add real-time data quality monitoring dashboard
8. **Testing**: Expand integration test coverage for edge cases
9. **Reporting**: Add visual charts to benchmark reports

---

**End of Audit Report**
```

This structure provides comprehensive audit reporting with clear status indicators, detailed metrics, comparison tables, and actionable recommendations.


## Configuration

### Test Thresholds

**Tolerance Levels**:
```python
TOLERANCES = {
    # Ratio calculation comparison
    "ratio_calculation_percentage": 2.0,  # 2% tolerance
    
    # TTM calculation comparison
    "ttm_calculation_percentage": 1.0,  # 1% tolerance
    
    # Statistical benchmark comparison
    "benchmark_absolute": 0.1,  # 0.1 absolute difference
    
    # Formula validation
    "formula_accuracy": 0.01,  # 0.01 absolute difference
}
```

**Data Quality Thresholds**:
```python
DATA_QUALITY = {
    # NULL percentage thresholds
    "null_critical": 20.0,  # >20% is CRITICAL
    "null_warning": 10.0,   # >10% is WARNING
    
    # Minimum data requirements
    "minimum_periods": 4,  # Minimum quarters of data
    "minimum_peers": 3,    # Minimum peers for benchmark
    
    # Coverage thresholds
    "mapping_coverage_target": 80.0,  # Target mapping coverage %
    "round_trip_consistency": 95.0,   # Target round-trip consistency %
}
```

**Sample Sizes**:
```python
SAMPLE_SIZES = {
    "mapping_test_banking": 5,      # Banking companies for mapping test
    "mapping_test_industrial": 5,   # Industrial companies for mapping test
    "reference_companies": 3,        # Reference companies for accuracy tests
    "bootstrap_test_companies": 5,   # Companies for bootstrap test
    "sector_benchmark_min_peers": 10,# Minimum peers for benchmark accuracy test
}
```

### Economic Bounds Configuration

Economic bounds define valid ranges for ratios by sector:

```python
ECONOMIC_BOUNDS = {
    # Default bounds for industrial companies
    "_default": {
        # Liquidity ratios
        "current_ratio": (0.1, 15.0),
        "acid_test_ratio": (0.05, 12.0),
        
        # Leverage ratios
        "debt_to_equity": (-2.0, 25.0),
        "debt_ratio": (0.0, 15.0),
        "net_debt_to_equity": (-5.0, 30.0),
        
        # Profitability margins
        "gross_margin": (-0.50, 0.95),
        "operating_margin": (-0.50, 0.80),
        "net_margin": (-2.00, 0.60),
        "ebitda_margin": (-0.50, 0.80),
        
        # Return ratios
        "roe": (-1.00, 1.50),
        "roa": (-0.30, 0.40),
        
        # Valuation ratios
        "pe_ratio": (0.0, 150.0),
        "pb_ratio": (0.0, 20.0),
        "ev_ebitda": (0.0, 60.0),
        
        # Efficiency ratios
        "asset_turnover": (0.0, 5.0),
        "inventory_turnover": (0.0, 50.0),
        "receivables_turnover": (0.0, 50.0),
    },
    
    # Banking sector specific bounds
    "Bankacılık & Finans": {
        # Banking profitability
        "net_interest_margin": (-0.02, 0.12),
        "cost_income_ratio": (0.0, 1.5),
        
        # Banking asset quality
        "loan_to_deposit": (0.30, 2.50),
        "npl_ratio": (0.0, 0.25),
        
        # Banking capital
        "capital_adequacy": (0.08, 0.40),
        
        # Banking returns
        "roe": (-0.30, 0.50),
        "roa": (-0.05, 0.08),
        
        # Banking valuation
        "pe_ratio": (0.0, 25.0),
        "pb_ratio": (0.0, 5.0),
    },
}
```

**Rationale for Bounds**:
- **Current Ratio (0.1, 15.0)**: Below 0.1 indicates severe liquidity crisis. Above 15 suggests inefficient capital allocation or data error.
- **Debt to Equity (-2.0, 25.0)**: Negative values possible during restructuring (negative equity). Above 25 indicates extreme leverage or error.
- **ROE (-1.0, 1.5)**: Negative during losses. Above 150% suggests unsustainable returns or accounting issues.
- **Loan to Deposit (0.3, 2.5)**: Banking-specific. Below 0.3 indicates excess deposits. Above 2.5 indicates aggressive lending.
- **NPL Ratio (0.0, 0.25)**: Non-performing loan ratio. Above 25% indicates systemic asset quality issues.

### Filter Pipeline Configuration

```python
FILTER_CONFIG = {
    # F2: Minimum periods filter
    "min_periods": 1,  # Require at least 1 period of data
    
    # F4: Winsorization percentiles
    "winsorize_lower": 5,   # P5
    "winsorize_upper": 95,  # P95
    
    # F5: Minimum peer count
    "min_peers_compute": 3,  # Require at least 3 peers to compute benchmark
    
    # F5: Reliability thresholds
    "reliability_thresholds": {
        "INSUFFICIENT": (0, 2),    # n < 3
        "LOW": (3, 4),             # 3 <= n <= 4
        "MEDIUM": (5, 9),          # 5 <= n <= 9
        "HIGH": (10, float('inf')),# n >= 10
    },
}
```

### Valid Sectors Configuration

```python
VALID_SECTORS = [
    "Bankacılık & Finans",
    "Teknoloji & İletişim",
    "Gıda & İçecek",
    "Perakende Ticaret",
    "Otomotiv",
    "İnşaat & İnşaat Malzemeleri",
    "Enerji",
    "Kimya & Petrol",
    "Metal Ana Sanayi",
    "Turizm",
    "Tekstil & Deri",
    "Ulaştırma & Lojistik",
    "Holdingler",
    "Diğer",
]

FINANCIAL_GROUP_MAPPING = {
    "Bankacılık & Finans": ["UFRS_K", "UFRS_F", "UFRS_S"],
    "_default": ["XI_29"],  # All other sectors
}
```

### Income Statement Items for TTM

```python
INCOME_STATEMENT_ITEMS = [
    "revenue",
    "gross_profit",
    "operating_income",
    "ebitda",
    "net_income",
    "cost_of_goods_sold",
    "operating_expenses",
    "interest_expense",
    "tax_expense",
    
    # Banking specific
    "net_interest_income",
    "fee_and_commission_income",
    "total_operating_income",
]

BALANCE_SHEET_ITEMS = [
    "total_assets",
    "current_assets",
    "non_current_assets",
    "total_liabilities",
    "current_liabilities",
    "non_current_liabilities",
    "shareholders_equity",
    "inventories",
    "accounts_receivable",
    "cash_and_equivalents",
    
    # Banking specific
    "gross_loans",
    "deposits",
    "non_performing_loans",
]
```

### Logging Configuration

```python
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "simple": {
            "format": "%(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "audit_execution.log",
            "formatter": "detailed",
            "level": "DEBUG"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"]
    }
}
```

---

## Implementation Notes

### Technology Stack

- **Language**: Python 3.10+
- **Testing Framework**: pytest 7.x
- **Property Testing**: Hypothesis 6.x
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Statistical Computing**: NumPy, SciPy
- **Reporting**: Markdown generation with tabulate for tables

### File Structure

```
tests/audit/
├── __init__.py
├── conftest.py                      # pytest configuration and fixtures
├── config.yaml                      # Test configuration
│
├── test_sector_classification.py   # Requirement 1
├── test_item_code_mapping.py       # Requirement 2
├── test_ratio_formulas.py          # Requirement 3
├── test_ratio_calculation.py       # Requirement 4
├── test_ttm_calculation.py         # Requirement 5
├── test_filter_pipeline.py         # Requirement 6
├── test_economic_bounds.py         # Requirement 7
├── test_benchmark_accuracy.py      # Requirement 8
├── test_reliability.py             # Requirement 9
├── test_data_quality.py            # Requirement 10
├── test_bootstrap_process.py       # Requirement 11
├── test_sector_ratios.py           # Requirement 12
│
├── utils/
│   ├── __init__.py
│   ├── pretty_printer.py           # Report formatting utilities
│   ├── test_parser.py              # Test result parsing
│   ├── report_generator.py         # Audit report generation
│   ├── synthetic_data.py           # Synthetic data generators
│   └── validation_algorithms.py    # Reusable validation logic
│
├── fixtures/
│   ├── reference_companies.json    # Ground truth data
│   ├── synthetic_peers.json        # Test peer data
│   └── expected_ratios.json        # Expected calculation results
│
└── reports/
    └── AUDIT_REPORT.md             # Generated audit report
```

### Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.10"
pytest = "^7.4.0"
hypothesis = "^6.90.0"
sqlalchemy = "^2.0.0"
psycopg2-binary = "^2.9.0"
numpy = "^1.24.0"
scipy = "^1.11.0"
pyyaml = "^6.0"
tabulate = "^0.9.0"
```

### Execution Time Estimates

- **Property-based tests**: ~5-10 minutes (2000 test cases)
- **Integration tests**: ~10-15 minutes (database queries, real data)
- **Report generation**: ~2-3 minutes
- **Total audit runtime**: ~20-30 minutes

### Scalability Considerations

- **Database Queries**: Use indexed queries and limit result sets
- **Parallel Execution**: Enable pytest-xdist for faster execution
- **Caching**: Cache database results for repeated queries
- **Sampling**: Use representative samples instead of full data scans where appropriate

---

## Summary

The Financial Engine Audit Phase 1 system provides comprehensive validation of the HissePro Financial Analysis Engine through a dual testing strategy combining property-based tests and integration tests. The system verifies correctness of sector classifications, ratio calculations, TTM aggregations, filter pipeline logic, and benchmark computations across 14 sectors and 620+ companies.

Key design principles include separation of concerns, comprehensive error handling, detailed reporting with ASCII tables and visualizations, and configurable thresholds for validation. The audit generates actionable recommendations for Phase 2 improvements based on automated test results and statistical analysis.

The design supports both sequential and parallel execution, uses synthetic data for property testing, validates against real production data, and produces a comprehensive Markdown audit report with health scores, priority matrices, and detailed findings for each requirement.

