# Requirements Document

## Introduction

Bu spec, HissePro Financial Analysis Engine'in Phase 1 detaylı analiz ve değerlendirme sürecini tanımlar. Sistem şu anda İş Yatırım API'den mali tablo verilerini çekerek, sektörlere göre gruplandırma yapıp finansal rasyolar ve benchmark hesaplamalarını gerçekleştiriyor. Phase 1'in amacı mevcut sistemin doğruluğunu, güvenilirliğini ve sektör bazlı hesaplamaların geçerliliğini detaylı olarak test edip değerlendirmektir.

Bu aşamada tespit edilen bulgular Phase 2'de (gelecek spec) çözüm ve iyileştirme çalışmalarına temel oluşturacaktır.

## Glossary

- **System**: Financial Analysis Engine - Mali tablo fetch, rasyo ve benchmark hesaplama sistemi
- **Bootstrap_Engine**: 3 fazlı bootstrap süreci (fetch → ratios → benchmarks)
- **Ratio_Calculator**: Senkron rasyo hesaplama modülü (DEFAULT_RATIOS, BANKING_RATIOS, SECTOR_RATIOS)
- **Benchmark_Calculator**: Senkron benchmark hesaplama modülü (F1-F5 filter pipeline)
- **Item_Code_Mapper**: İş Yatırım API item kodlarını semantic name'lere map eden servis
- **Sector_Main**: 14 ana sektör sınıflandırması (Bankacılık & Finans, vb.)
- **Financial_Group**: Mali tablo standart grubu (UFRS_K, UFRS_F, UFRS_S, XI_29)
- **F1_F5_Filter**: Benchmark hesaplamalarında peer validation için 5 aşamalı filtre (NULL check, minimum periods, economic validity, statistical outlier removal, peer count validation)
- **TTM**: Trailing Twelve Months - Son 12 aylık toplam değer
- **Economic_Bounds**: F3 filter'da kullanılan sektör bazlı geçerlilik aralıkları
- **Test_Suite**: Sistemin doğruluğunu ve güvenilirliğini test eden otomatik test koleksiyonu
- **Audit_Report**: Test sonuçlarını ve bulguları içeren detaylı analiz raporu

## Requirements

### Requirement 1: Sector Classification Testing

**User Story:** As a financial analyst, I want to verify sector classifications are accurate, so that companies are grouped correctly for benchmark calculations.

#### Acceptance Criteria

1. THE Test_Suite SHALL load all companies from the database with their sector_main and financial_group values
2. WHEN sector mappings are tested, THE Test_Suite SHALL verify each company's sector_main is one of the 14 valid main sectors
3. WHEN financial group mappings are tested, THE Test_Suite SHALL verify banking companies (Bankacılık & Finans sector) have UFRS_K, UFRS_F, or UFRS_S financial_group
4. WHEN financial group mappings are tested, THE Test_Suite SHALL verify industrial companies have XI_29 financial_group
5. IF a company's sector_main does not match its financial_group, THEN THE Test_Suite SHALL flag it as a classification error
6. THE Test_Suite SHALL generate a sector classification accuracy report showing total companies, correctly classified, and misclassified with details
7. THE Test_Suite SHALL identify any companies with NULL or invalid sector_main values
8. THE Audit_Report SHALL include sector classification accuracy percentage and list of misclassified companies

### Requirement 2: Item Code Mapping Coverage Testing

**User Story:** As a developer, I want to verify item code mappings are comprehensive, so that all financial statement line items are correctly interpreted.

#### Acceptance Criteria

1. THE Test_Suite SHALL select a sample of at least 10 companies (5 banking, 5 industrial)
2. FOR each sample company, THE Test_Suite SHALL retrieve all distinct item codes from financial_statements_raw table
3. FOR each item code, THE Test_Suite SHALL attempt to resolve it to a semantic name using Item_Code_Mapper
4. THE Test_Suite SHALL calculate mapping coverage percentage (mapped codes / total codes × 100)
5. IF mapping coverage is below 80 percent, THEN THE Test_Suite SHALL flag it as insufficient coverage
6. THE Test_Suite SHALL identify unmapped item codes and group them by financial_group
7. THE Audit_Report SHALL include mapping coverage statistics per financial_group
8. THE Audit_Report SHALL list top 20 unmapped item codes with their frequencies

### Requirement 3: Ratio Formula Validation Testing

**User Story:** As a financial analyst, I want to verify ratio formulas are mathematically correct, so that calculated ratios accurately represent company performance.

#### Acceptance Criteria

1. THE Test_Suite SHALL load ratio configurations from DEFAULT_RATIOS and BANKING_RATIOS
2. FOR each ratio configuration, THE Test_Suite SHALL verify the formula function is callable and returns a numeric value or None
3. THE Test_Suite SHALL create synthetic financial data with known values
4. WHEN synthetic data is provided, THE Test_Suite SHALL calculate each ratio and verify the result matches expected value within 0.01 tolerance
5. THE Test_Suite SHALL test division-by-zero handling by providing zero denominators
6. THE Test_Suite SHALL test NULL handling by providing None values for required fields
7. THE Test_Suite SHALL verify TTM ratios use correct aggregation (sum for income statement, average for balance sheet)
8. IF a ratio formula produces incorrect results, THEN THE Test_Suite SHALL flag it as a formula error
9. THE Audit_Report SHALL list all ratio formulas with validation status (PASS/FAIL) and error details

### Requirement 4: Ratio Calculation Correctness Testing

**User Story:** As a financial analyst, I want to verify ratio calculations match expected values, so that I can trust the computed financial metrics.

#### Acceptance Criteria

1. THE Test_Suite SHALL select 3 reference companies (1 bank, 2 industrial) with complete financial data
2. FOR each reference company, THE Test_Suite SHALL manually calculate expected ratio values using latest period data
3. THE Test_Suite SHALL execute Ratio_Calculator for the same companies and periods
4. THE Test_Suite SHALL compare calculated ratios against expected values with 2 percent tolerance
5. IF calculated ratio differs from expected by more than 2 percent, THEN THE Test_Suite SHALL flag it as a calculation discrepancy
6. THE Test_Suite SHALL verify current_ratio calculation (current_assets / current_liabilities)
7. THE Test_Suite SHALL verify debt_to_equity calculation (total_debt / shareholders_equity)
8. THE Test_Suite SHALL verify ROE calculation (net_income_ttm / shareholders_equity_avg)
9. THE Test_Suite SHALL verify banking-specific ratios (loan_to_deposit, npl_ratio) for banking sector
10. THE Audit_Report SHALL include comparison tables showing expected vs calculated values with percentage differences

### Requirement 5: TTM Calculation Testing

**User Story:** As a financial analyst, I want to verify TTM calculations are correct, so that trailing twelve month metrics accurately reflect company performance.

#### Acceptance Criteria

1. THE Test_Suite SHALL select companies with at least 4 quarters of historical data
2. FOR each selected company, THE Test_Suite SHALL manually calculate TTM revenue by summing last 4 quarters
3. THE Test_Suite SHALL execute Ratio_Calculator TTM logic and retrieve calculated revenue_ttm
4. THE Test_Suite SHALL compare manual TTM calculation against system TTM calculation with 1 percent tolerance
5. THE Test_Suite SHALL verify TTM calculation excludes banking sector (UFRS_K uses annual data directly)
6. THE Test_Suite SHALL verify TTM calculation includes industrial sector (XI_29 uses quarterly summation)
7. IF TTM calculation differs from expected by more than 1 percent, THEN THE Test_Suite SHALL flag it as a TTM calculation error
8. THE Test_Suite SHALL verify TTM requires minimum 3 of 4 quarters with data
9. THE Audit_Report SHALL include TTM calculation validation results with sample companies

### Requirement 6: Benchmark F1-F5 Filter Pipeline Testing

**User Story:** As a data quality engineer, I want to verify the F1-F5 filter pipeline correctly validates peers, so that benchmark calculations exclude invalid data.

#### Acceptance Criteria

1. THE Test_Suite SHALL create synthetic peer data with known characteristics (NULL values, infinite values, outliers, insufficient periods)
2. WHEN synthetic data is provided to Benchmark_Calculator, THE Test_Suite SHALL verify F1 filter excludes NULL and infinite values
3. WHEN synthetic data is provided, THE Test_Suite SHALL verify F2 filter excludes companies with fewer than minimum required periods
4. WHEN synthetic data is provided, THE Test_Suite SHALL verify F3 filter excludes values outside economic bounds
5. WHEN synthetic data is provided, THE Test_Suite SHALL verify F4 filter applies winsorization at P5 and P95 percentiles
6. WHEN synthetic data is provided, THE Test_Suite SHALL verify F5 filter rejects benchmark calculation if peer count is below 3
7. THE Test_Suite SHALL track exclusion counts per filter stage (F1, F2, F3, F4, F5)
8. THE Audit_Report SHALL include filter pipeline statistics showing exclusion rates per stage

### Requirement 7: Economic Bounds Validation Testing

**User Story:** As a financial analyst, I want to verify economic bounds are appropriate for each sector, so that benchmarks exclude economically impossible values.

#### Acceptance Criteria

1. THE Test_Suite SHALL load economic bounds from ECONOMIC_BOUNDS dictionary
2. FOR each ratio with economic bounds, THE Test_Suite SHALL verify min_val is less than max_val
3. THE Test_Suite SHALL verify banking sector ratios have sector-specific bounds
4. THE Test_Suite SHALL verify default bounds exist for all common ratios
5. THE Test_Suite SHALL create test cases with values at boundary edges (min_val - 0.01, min_val, max_val, max_val + 0.01)
6. WHEN boundary test cases are provided, THE Test_Suite SHALL verify F3 filter correctly includes/excludes based on bounds
7. THE Test_Suite SHALL identify ratios without economic bounds defined
8. THE Audit_Report SHALL list economic bounds per ratio and sector with validation status

### Requirement 8: Benchmark Calculation Accuracy Testing

**User Story:** As a financial analyst, I want to verify benchmark calculations are statistically correct, so that sector medians accurately represent peer performance.

#### Acceptance Criteria

1. THE Test_Suite SHALL select 2 sectors with sufficient peer data (n >= 10)
2. FOR each selected sector, THE Test_Suite SHALL retrieve raw ratio values for a specific period and ratio_code
3. THE Test_Suite SHALL manually calculate median_ew (equal-weight median) using numpy.median
4. THE Test_Suite SHALL manually calculate p25 and p75 percentiles
5. THE Test_Suite SHALL execute Benchmark_Calculator for the same sector, period, and ratio
6. THE Test_Suite SHALL compare manual calculations against system calculations with 0.1 tolerance
7. IF benchmark calculation differs from expected by more than 0.1, THEN THE Test_Suite SHALL flag it as a benchmark calculation error
8. THE Test_Suite SHALL verify market-cap weighted median (median_wt) uses correct weighting logic
9. THE Audit_Report SHALL include benchmark accuracy comparison tables

### Requirement 9: Benchmark Reliability Assessment Testing

**User Story:** As a financial analyst, I want to verify reliability assessments are correct, so that I can trust the quality indicators for benchmarks.

#### Acceptance Criteria

1. THE Test_Suite SHALL create test cases with varying peer counts (n=2, n=3, n=5, n=10, n=15)
2. WHEN peer count is less than 3, THE Test_Suite SHALL verify reliability is set to INSUFFICIENT and can_compute is False
3. WHEN peer count is 3 to 4, THE Test_Suite SHALL verify reliability is set to LOW
4. WHEN peer count is 5 to 9, THE Test_Suite SHALL verify reliability is set to MEDIUM
5. WHEN peer count is 10 or more, THE Test_Suite SHALL verify reliability is set to HIGH
6. THE Test_Suite SHALL verify benchmarks with INSUFFICIENT reliability are not saved to database
7. THE Audit_Report SHALL include reliability distribution statistics per sector

### Requirement 10: Data Quality and Completeness Testing

**User Story:** As a system administrator, I want to verify data quality and completeness, so that the system operates on reliable financial data.

#### Acceptance Criteria

1. THE Test_Suite SHALL query financial_statements_raw table and count total rows per ticker
2. THE Test_Suite SHALL identify companies with fewer than 4 periods of data
3. THE Test_Suite SHALL calculate NULL value percentage per semantic field (total_assets, revenue, net_income, etc.)
4. IF NULL percentage exceeds 20 percent for any critical field, THEN THE Test_Suite SHALL flag it as data quality issue
5. THE Test_Suite SHALL identify duplicate records (same ticker, period_key, item_code)
6. THE Test_Suite SHALL verify all active companies have at least one ratio calculated
7. THE Test_Suite SHALL verify all sectors with active companies have at least one benchmark
8. THE Audit_Report SHALL include data quality metrics (completeness, NULL rates, duplicate counts)

### Requirement 11: Bootstrap Process Testing

**User Story:** As a developer, I want to verify the bootstrap process executes correctly, so that the system can be reliably initialized.

#### Acceptance Criteria

1. THE Test_Suite SHALL execute Bootstrap_Engine for a single test sector with 5 companies
2. THE Test_Suite SHALL verify Phase 1 (fetch) completes and inserts financial statement rows
3. THE Test_Suite SHALL verify Phase 2 (ratios) completes and inserts company_ratios rows
4. THE Test_Suite SHALL verify Phase 3 (benchmarks) completes and inserts sector_benchmarks rows
5. THE Test_Suite SHALL verify fetch logs are created with correct metadata (checksum, is_new_data, http_status)
6. THE Test_Suite SHALL verify bootstrap handles API failures gracefully and continues processing
7. THE Test_Suite SHALL verify bootstrap respects rate limiting (20 requests per minute)
8. THE Audit_Report SHALL include bootstrap execution statistics (duration, success rate, error counts)

### Requirement 12: Sector-Specific Ratio Application Testing

**User Story:** As a financial analyst, I want to verify sector-specific ratios are applied correctly, so that banking and industrial companies use appropriate metrics.

#### Acceptance Criteria

1. THE Test_Suite SHALL select 3 banking companies (sector_main = "Bankacılık & Finans")
2. THE Test_Suite SHALL execute Ratio_Calculator for banking companies
3. THE Test_Suite SHALL verify banking companies have banking-specific ratios calculated (net_interest_margin, loan_to_deposit, npl_ratio, capital_adequacy)
4. THE Test_Suite SHALL verify banking companies do NOT have inventory_turnover calculated
5. THE Test_Suite SHALL select 3 industrial companies (sector_main != "Bankacılık & Finans")
6. THE Test_Suite SHALL execute Ratio_Calculator for industrial companies
7. THE Test_Suite SHALL verify industrial companies have industrial ratios calculated (current_ratio, inventory_turnover, receivables_turnover)
8. THE Test_Suite SHALL verify industrial companies do NOT have loan_to_deposit calculated
9. THE Audit_Report SHALL include ratio application matrix showing which ratios are calculated per sector

### Requirement 13: Audit Report Generation

**User Story:** As a project manager, I want to receive a comprehensive audit report, so that I can understand system health and prioritize Phase 2 improvements.

#### Acceptance Criteria

1. THE System SHALL generate an audit report in Markdown format
2. THE Audit_Report SHALL include an executive summary with overall system health score (0-100)
3. THE Audit_Report SHALL include detailed findings for each requirement (1-12)
4. FOR each finding, THE Audit_Report SHALL include status (PASS/FAIL/WARNING), metrics, and recommendations
5. THE Audit_Report SHALL include a priority matrix ranking issues by severity (CRITICAL, HIGH, MEDIUM, LOW)
6. THE Audit_Report SHALL include statistics tables and visualizations (ASCII tables)
7. THE Audit_Report SHALL include a conclusions section summarizing key findings
8. THE Audit_Report SHALL include a recommendations section for Phase 2 improvements
9. THE Audit_Report SHALL be saved to the project root directory with timestamp
10. THE System SHALL log audit report generation completion

### Requirement 14: Test Parser and Test Report Generation

**User Story:** As a developer, I want to parse test results and generate a formatted report, so that test outcomes are easy to interpret.

#### Acceptance Criteria

1. THE System SHALL parse test output to extract test names, statuses (PASS/FAIL), and metrics
2. WHEN tests are executed, THE System SHALL capture all assertion failures with expected vs actual values
3. THE System SHALL calculate overall test pass rate (passed_tests / total_tests × 100)
4. THE System SHALL group test results by requirement category
5. THE System SHALL generate a test summary report in Markdown format
6. THE test summary report SHALL include pass/fail counts per requirement
7. THE test summary report SHALL include execution time and timestamp
8. THE test summary report SHALL highlight critical failures requiring immediate attention
9. THE System SHALL save the test report to .kiro/specs/financial-engine-audit-phase1/test_results.md

### Requirement 15: Pretty Printer for Audit Data

**User Story:** As a developer, I want to format audit data into readable tables and charts, so that reports are easy to understand.

#### Acceptance Criteria

1. THE System SHALL provide a Pretty_Printer module for formatting audit data
2. THE Pretty_Printer SHALL convert Python dictionaries to ASCII tables with aligned columns
3. THE Pretty_Printer SHALL support column width auto-sizing based on content
4. THE Pretty_Printer SHALL support numeric formatting (percentages, decimals, thousands separators)
5. THE Pretty_Printer SHALL generate comparison tables showing expected vs actual values with delta columns
6. THE Pretty_Printer SHALL generate distribution histograms using ASCII characters
7. THE Pretty_Printer SHALL generate summary statistics boxes (min, max, mean, median, std_dev)
8. THE Pretty_Printer SHALL support color coding for terminal output (green for PASS, red for FAIL, yellow for WARNING)

### Requirement 16: Round-Trip Testing for Data Integrity

**User Story:** As a data engineer, I want to verify data integrity through round-trip testing, so that data transformations preserve accuracy.

#### Acceptance Criteria

1. THE Test_Suite SHALL select a sample company with raw financial data
2. THE Test_Suite SHALL extract item_code values from financial_statements_raw
3. THE Test_Suite SHALL map item_codes to semantic names using Item_Code_Mapper
4. THE Test_Suite SHALL reverse-map semantic names back to item_codes
5. FOR all mapped fields, THE Test_Suite SHALL verify forward and reverse mappings are consistent (round-trip property)
6. THE Test_Suite SHALL calculate round-trip consistency rate (consistent_mappings / total_mappings × 100)
7. IF round-trip consistency is below 95 percent, THEN THE Test_Suite SHALL flag it as a mapping integrity issue
8. THE Audit_Report SHALL include round-trip consistency results

