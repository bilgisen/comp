# Requirements Document: Production-Ready Fundamental Analysis API

## Introduction

HissePro COMP Engine, Türkiye sermaye piyasaları için endüstri standardında temel analiz API'si sağlayan bir sistemdir. Sistem, İş Yatırım API'sinden mali tablo verilerini otomatik olarak çeker, 50+ finansal rasyo hesaplar, sektörel benchmark'lar üretir ve AI-destekli analiz context'i sağlar. Bu requirements belgesi, mevcut sistemi production-ready, satılabilir ve endüstri best practices'e uygun hale getirmek için gerekli gereksinimleri tanımlar.

## Glossary

- **System**: HissePro COMP Engine - Temel analiz API platformu
- **Data_Fetcher**: İş Yatırım API'sinden mali tablo verilerini çeken bileşen
- **Ratio_Calculator**: Finansal rasyo hesaplama motoru
- **Benchmark_Engine**: Sektör medyan ve karşılaştırma hesaplama motoru
- **Scheduler**: Otomatik veri çekme zamanlayıcısı
- **Parser**: Mali tablo item_code verilerini ayrıştırıcı
- **Pretty_Printer**: Hesaplanan finansal verileri standart formatta yazdırıcı
- **Cache_Manager**: Redis/Valkey önbellekleme yöneticisi
- **API_Gateway**: REST API endpoint yönetim katmanı
- **Admin_Dashboard**: Sistem yönetim ve monitoring arayüzü
- **Quarter**: Çeyrek dönem (Q1=3, Q2=6, Q3=9, Q4=12)
- **TTM**: Trailing Twelve Months - Son 12 aylık toplam
- **Financial_Group**: Mali tablo format türü (UFRS_K, UFRS_F, UFRS_S, XI_29)
- **Item_Code**: İş Yatırım API'sindeki mali tablo kalemi kodu (örn: "1Z", "3ZA")
- **Diff_Check**: Checksum karşılaştırma ile yeni veri tespiti
- **F1_F5_Pipeline**: 5 aşamalı sektör medyan filtreleme sistemi
- **Winsorization**: Uç değerleri belirli persentillere çekerek düzeltme
- **KAP_Window**: KAP mali tablo raporlama penceresi (çeyrek sonu + 75 gün)
- **Bootstrap_Process**: İlk kurulumda tüm şirketlerin mali tablolarını çekme işlemi
- **Sector_Main**: 14 ana konsolide sektör grubu
- **Sector_Raw**: İş Yatırım'dan gelen orijinal ~53 sektör
- **NPL_Ratio**: Non-Performing Loan Ratio - Takipteki krediler oranı
- **NIM**: Net Interest Margin - Net faiz marjı
- **Economic_Bounds**: Sektöre özel ekonomik geçerlilik sınırları (F3 filtresi)
- **Peer_Company**: Aynı sektördeki karşılaştırılabilir şirket
- **Reliability_Score**: Sektör medyanı güvenilirlik seviyesi (HIGH/MEDIUM/LOW)
- **Circuit_Breaker**: Rate limiting aşımında devreye giren koruma mekanizması

## Requirements

### Requirement 1: Bootstrap Data Collection System

**User Story:** As a system administrator, I want to perform an initial complete data fetch for all active companies, so that the system has a complete historical dataset before regular incremental updates begin.

#### Acceptance Criteria

1. WHEN the system is initialized for the first time, THE Bootstrap_Process SHALL fetch financial statements for all active companies for the last 4 quarters
2. THE Bootstrap_Process SHALL respect İş Yatırım API rate limits during initial fetch (20 requests/minute)
3. WHEN fetching for multiple companies, THE Bootstrap_Process SHALL implement batch processing with 50 companies per batch
4. THE Bootstrap_Process SHALL log progress including company count, successful fetches, failures, and estimated completion time
5. IF a company fetch fails during bootstrap, THE Bootstrap_Process SHALL retry up to 3 times with exponential backoff (5s, 15s, 45s)
6. WHEN bootstrap completes, THE System SHALL generate a summary report showing total companies fetched, success rate, and any failed companies
7. THE Bootstrap_Process SHALL persist the completion status to prevent accidental re-runs
8. WHILE bootstrap is running, THE System SHALL reject other fetch operations to prevent resource conflicts

### Requirement 2: Mali Tablo Parser and Pretty Printer

**User Story:** As a developer, I want robust parsing and formatting of financial statement data, so that data integrity is maintained throughout the system and can be verified.

#### Acceptance Criteria

1. THE Parser SHALL parse İş Yatırım API response JSON into normalized Item_Code structures according to UFRS_K and XI_29 format specifications
2. WHEN parsing UFRS_K (banking) data, THE Parser SHALL map item codes according to the hierarchical structure (1x=Assets, 2x=Liabilities, 3x=Income Statement)
3. WHEN parsing XI_29 (industrial) data, THE Parser SHALL map item codes according to industry-specific chart of accounts
4. IF an unknown Item_Code is encountered, THE Parser SHALL log a warning and store the raw value for manual review
5. THE Pretty_Printer SHALL format financial statements in standardized JSON format with proper nesting and item code descriptions
6. THE Pretty_Printer SHALL include metadata (company, period, financial_group, fetch_timestamp) in output
7. FOR ALL valid financial statement objects, parsing then printing then parsing SHALL produce an equivalent object (round-trip property)
8. WHEN printing for external consumption, THE Pretty_Printer SHALL format numeric values with thousand separators and 2 decimal precision
9. THE Parser SHALL validate that Toplam_Aktif (1Z) equals Toplam_Pasif (2Z) in balance sheet data and log discrepancies

### Requirement 3: Item Code Mapping Completion

**User Story:** As a financial analyst, I want complete and accurate mapping of all Item Codes to semantic financial terms, so that ratios can be calculated correctly for all sectors.

#### Acceptance Criteria

1. THE System SHALL maintain a complete mapping table for UFRS_K Item Codes covering all banking balance sheet and income statement items
2. THE System SHALL maintain a complete mapping table for XI_29 Item Codes covering all industrial financial statement items
3. THE System SHALL maintain separate mappings for UFRS_F (financial leasing) and UFRS_S (insurance) where applicable
4. WHEN a new Item_Code is encountered that has no mapping, THE System SHALL store it in an unmapped_codes table for review
5. THE Admin_Dashboard SHALL display unmapped codes with sample values and allow administrators to create mappings
6. WHEN an Item_Code mapping is added or modified, THE System SHALL invalidate affected cached ratios and trigger recalculation
7. THE System SHALL validate that critical Item Codes for each Financial_Group are present before allowing ratio calculation
8. THE System SHALL document the source and meaning of each Item_Code in the mapping configuration

### Requirement 4: TTM Calculation Engine

**User Story:** As a financial analyst, I want accurate Trailing Twelve Months calculations, so that income statement ratios reflect annualized performance correctly.

#### Acceptance Criteria

1. WHEN calculating TTM for UFRS_K (banking) companies, THE Ratio_Calculator SHALL use the period=12 value directly as it represents cumulative year-to-date data
2. WHEN calculating TTM for XI_29 (industrial) companies, THE Ratio_Calculator SHALL sum the last 4 quarters (value1 + value2 + value3 + value4)
3. IF fewer than 4 quarters of data are available for an XI_29 company, THE Ratio_Calculator SHALL return NULL for TTM ratios
4. THE Ratio_Calculator SHALL flag TTM values with is_ttm=TRUE in the company_ratios table
5. WHEN calculating balance sheet ratios (Current_Ratio, Debt_to_Equity), THE Ratio_Calculator SHALL use the most recent period value (instant snapshot)
6. WHEN calculating income statement ratios (Net_Margin, ROE, ROA), THE Ratio_Calculator SHALL use TTM values to ensure annualized comparability
7. FOR ROE and ROA calculations, THE Ratio_Calculator SHALL use average equity/assets computed as (period_start + period_end) / 2
8. THE Ratio_Calculator SHALL store both quarterly and TTM values separately for trending analysis

### Requirement 5: Sektörel Fine-Tuning Configuration

**User Story:** As a financial analyst, I want sector-specific ratio calculations and adjustments, so that comparisons are meaningful within each industry's unique characteristics.

#### Acceptance Criteria

1. THE System SHALL maintain a SECTOR_RATIO_CONFIG defining which ratios are calculated for each Sector_Main
2. WHERE sector is "Bankacılık & Finans", THE Ratio_Calculator SHALL calculate banking-specific ratios (NIM, Credit_to_Deposit, Capital_Adequacy, NPL_Ratio)
3. WHERE sector is "GYO", THE Ratio_Calculator SHALL NOT calculate Current_Ratio as it is economically meaningless for REITs
4. WHERE sector is "Sigortacılık", THE Ratio_Calculator SHALL calculate insurance-specific ratios (Loss_Ratio, Expense_Ratio, Combined_Ratio)
5. THE System SHALL maintain sector-specific Economic_Bounds for F3 filtering with realistic min/max ranges per ratio per sector
6. WHERE sector is "Teknoloji & İletişim", THE Economic_Bounds SHALL allow negative Net_Margin up to -500% and P/E ratio up to 200
7. WHERE sector is "Sağlık & İlaç", THE Economic_Bounds SHALL allow P/E ratios up to 100 due to growth premium
8. THE System SHALL allow administrators to modify sector-specific configurations without code changes
9. WHEN sector configuration is updated, THE System SHALL invalidate affected sector medians and trigger recalculation

### Requirement 6: Bankalar İçin NPL Data Source

**User Story:** As a financial analyst, I want accurate Non-Performing Loan ratios for banks, so that credit quality assessment is reliable.

#### Acceptance Criteria

1. THE System SHALL identify an alternative data source for NPL (Takipteki Krediler) when Item_Code 1AFD returns zero or null
2. IF NPL data is available from İş Yatırım API in a separate endpoint, THE Data_Fetcher SHALL fetch it during bank data collection
3. IF NPL data must be sourced from KAP disclosures, THE System SHALL provide an admin interface to manually input NPL values
4. WHEN NPL data is unavailable, THE System SHALL return NULL for NPL_Ratio instead of calculating with zero
5. THE System SHALL flag companies with missing NPL data in the Admin_Dashboard for manual review
6. WHERE alternative NPL data source is configured, THE System SHALL document the source and update frequency
7. THE System SHALL validate that NPL values are non-negative and not greater than Total_Loans

### Requirement 7: Momentum and Quarterly Comparison

**User Story:** As a financial analyst, I want to analyze quarter-over-quarter and year-over-year trends, so that momentum and growth patterns are visible.

#### Acceptance Criteria

1. THE System SHALL store financial statement data for at least 8 quarters per company to enable trend analysis
2. THE System SHALL calculate quarter-over-quarter (QoQ) percentage change for all income statement items
3. THE System SHALL calculate year-over-year (YoY) percentage change for all financial statement items
4. WHEN displaying ratio trends, THE API_Gateway SHALL return historical values for the last 8 quarters
5. THE System SHALL calculate momentum scores based on consistent QoQ improvement over 3+ quarters
6. THE Benchmark_Engine SHALL calculate sector median trends alongside company-specific trends
7. WHEN a company shows unusual momentum (>3 standard deviations from sector), THE System SHALL flag it for review
8. THE System SHALL provide endpoints returning time-series data in formats suitable for charting (arrays with timestamps and values)

### Requirement 8: Advanced Sector Median Calculation

**User Story:** As a financial analyst, I want statistically robust sector medians, so that peer comparisons are reliable and outlier-resistant.

#### Acceptance Criteria

1. THE Benchmark_Engine SHALL implement the complete F1-F5 filter pipeline for all sector median calculations
2. WHEN applying F1 filter, THE Benchmark_Engine SHALL exclude companies with NULL, infinite, or NaN ratio values
3. WHEN applying F2 filter, THE Benchmark_Engine SHALL exclude companies with fewer than 3 out of 4 most recent quarters of data
4. WHEN applying F3 filter, THE Benchmark_Engine SHALL exclude companies with ratio values outside sector-specific Economic_Bounds
5. WHEN applying F4 filter, THE Benchmark_Engine SHALL apply Winsorization at P5 and P95 percentiles to cap extreme values without removing them
6. WHEN applying F5 filter, THE Benchmark_Engine SHALL mark reliability as INSUFFICIENT if fewer than 3 peer companies remain
7. THE Benchmark_Engine SHALL calculate both equal-weighted median and market-cap-weighted median
8. THE Benchmark_Engine SHALL store n_peers, n_excluded, and reliability score for each sector median
9. THE Benchmark_Engine SHALL maintain audit trail in sector_median_peers table showing which companies were included/excluded and why
10. WHEN a sector median is calculated, THE System SHALL cache the result in Redis with 24-hour TTL

### Requirement 9: Event-Driven Architecture

**User Story:** As a system architect, I want event-driven updates, so that changes propagate efficiently without full recalculation cycles.

#### Acceptance Criteria

1. WHEN new financial statement data is fetched and Diff_Check confirms it is new, THE System SHALL emit a "financial_data_updated" event
2. WHEN a "financial_data_updated" event is received, THE Ratio_Calculator SHALL recalculate ratios for the affected company
3. WHEN company ratios are updated, THE System SHALL emit a "company_ratios_updated" event with company ticker and Sector_Main
4. WHEN a "company_ratios_updated" event is received, THE Benchmark_Engine SHALL invalidate the cached sector median for the affected sector
5. THE Benchmark_Engine SHALL recalculate sector medians asynchronously using a job queue (not blocking API requests)
6. THE System SHALL use Redis Pub/Sub or a message queue (e.g., PostgreSQL LISTEN/NOTIFY) for event distribution
7. IF event processing fails, THE System SHALL retry with exponential backoff up to 3 times before logging as failed event
8. THE Admin_Dashboard SHALL display a log of recent events and their processing status

### Requirement 10: Rate Limiting and Circuit Breaker

**User Story:** As a system operator, I want intelligent rate limiting and circuit breaker protection, so that external API failures don't cascade and quotas are respected.

#### Acceptance Criteria

1. THE Data_Fetcher SHALL enforce a rate limit of 20 requests per minute to İş Yatırım API
2. THE Data_Fetcher SHALL implement jittered delays between requests (2.5-4.0 seconds) to avoid burst patterns
3. WHEN processing batches, THE Data_Fetcher SHALL pause for 120 seconds after every 50 companies
4. IF İş Yatırım API returns HTTP 429 (rate limit exceeded), THE Circuit_Breaker SHALL open and pause all requests for 5 minutes
5. IF İş Yatırım API returns HTTP 503 (service unavailable), THE Circuit_Breaker SHALL open and pause all requests for 15 minutes
6. WHILE Circuit_Breaker is open, THE System SHALL return cached data and log that live data is unavailable
7. THE Circuit_Breaker SHALL store state in Redis (not in-memory) to work correctly in multi-instance deployments
8. THE Admin_Dashboard SHALL display Circuit_Breaker status and allow manual reset
9. THE System SHALL monitor and log rate limiting metrics (requests per minute, circuit breaker events, 429 responses)

### Requirement 11: Comprehensive API Endpoints

**User Story:** As an API consumer, I want well-documented, consistent, and comprehensive API endpoints, so that I can build applications on top of the platform.

#### Acceptance Criteria

1. THE API_Gateway SHALL provide OpenAPI/Swagger documentation at /docs endpoint
2. THE API_Gateway SHALL provide endpoint GET /api/v1/companies/{ticker}/ratios returning all calculated ratios with sector comparison
3. THE API_Gateway SHALL provide endpoint GET /api/v1/companies/{ticker}/financials returning raw financial statements for last 4 quarters
4. THE API_Gateway SHALL provide endpoint GET /api/v1/companies/{ticker}/trends returning historical ratio values for trending
5. THE API_Gateway SHALL provide endpoint GET /api/v1/sectors/{sector_name}/benchmarks returning sector medians with reliability scores
6. THE API_Gateway SHALL provide endpoint GET /api/v1/sectors/{sector_name}/companies returning all companies in sector with basic metrics
7. THE API_Gateway SHALL provide endpoint GET /api/v1/companies/{ticker}/compare?compare_to=sector returning percentile rankings
8. THE API_Gateway SHALL provide endpoint GET /api/v1/ai/context/{ticker} returning AI-optimized context for chatbot integration
9. THE API_Gateway SHALL implement pagination for list endpoints with query parameters page and page_size
10. THE API_Gateway SHALL return consistent error responses with HTTP status codes, error messages, and timestamps
11. THE API_Gateway SHALL implement request validation and return HTTP 400 with details for invalid inputs
12. THE API_Gateway SHALL add cache-control headers to responses based on data volatility

### Requirement 12: Admin Dashboard and Monitoring

**User Story:** As a system administrator, I want a comprehensive admin dashboard, so that I can monitor system health, trigger operations, and troubleshoot issues.

#### Acceptance Criteria

1. THE Admin_Dashboard SHALL provide a view of scheduler status showing next run times and last execution results
2. THE Admin_Dashboard SHALL allow manual triggering of data fetch for individual companies or entire sectors
3. THE Admin_Dashboard SHALL display recent fetch logs with status, row counts, checksums, and error messages
4. THE Admin_Dashboard SHALL display unmapped Item Codes with frequency counts and allow creation of mappings
5. THE Admin_Dashboard SHALL display sector median calculation status with reliability scores and peer counts
6. THE Admin_Dashboard SHALL provide system health metrics (database connections, Redis status, API response times)
7. THE Admin_Dashboard SHALL display Circuit_Breaker status and allow manual reset
8. THE Admin_Dashboard SHALL provide alerts configuration for critical events (fetch failures, median calculation failures, API errors)
9. THE Admin_Dashboard SHALL allow viewing and editing of sector-specific configurations (Economic_Bounds, ratio lists)
10. THE Admin_Dashboard SHALL display data quality metrics (missing data percentages, stale data warnings, outlier counts)

### Requirement 13: Data Quality and Validation

**User Story:** As a financial analyst, I want high data quality assurance, so that I can trust the analysis results for investment decisions.

#### Acceptance Criteria

1. THE System SHALL validate that balance sheet identity (Assets = Liabilities + Equity) holds for all parsed financial statements
2. THE System SHALL flag companies where Toplam_Aktif (1Z) does not equal Toplam_Pasif (2Z) within 0.1% tolerance
3. THE System SHALL validate that all ratio denominators are non-zero before calculation and return NULL if zero
4. THE System SHALL validate that percentages and ratios are within economically reasonable ranges during calculation (not just filtering)
5. THE System SHALL compute and store a data_quality_score for each company based on completeness, consistency, and recency
6. THE System SHALL flag companies with data_quality_score below 0.7 in API responses and admin dashboard
7. THE System SHALL detect and log sudden large changes in financial statement values (>500% QoQ change) as potential data errors
8. THE System SHALL provide data lineage tracking showing source API response, parse time, and calculation time for each ratio
9. WHEN data quality issues are detected, THE System SHALL create alerts viewable in Admin_Dashboard

### Requirement 14: Performance and Scalability

**User Story:** As a system architect, I want the system to handle 300+ companies with sub-second API response times, so that user experience is excellent even under load.

#### Acceptance Criteria

1. THE API_Gateway SHALL return cached ratio data in less than 100ms for P95 of requests
2. THE Ratio_Calculator SHALL calculate all ratios for a single company in less than 5 seconds
3. THE Benchmark_Engine SHALL recalculate a sector median (with 50 companies) in less than 10 seconds
4. THE System SHALL use Redis caching with appropriate TTL values (24h for ratios, 12h for benchmarks, 6h for AI context)
5. THE System SHALL implement database connection pooling with minimum 10 and maximum 30 connections
6. THE System SHALL use database indexes on high-query columns (ticker, sector_main, ratio_code, period_key)
7. THE System SHALL implement async/await patterns for all I/O operations to maximize concurrency
8. THE System SHALL support horizontal scaling by storing all state in PostgreSQL or Redis (no in-memory state)
9. WHEN under high load (>100 concurrent requests), THE System SHALL maintain P95 response time under 500ms

### Requirement 15: Security and Access Control

**User Story:** As a security officer, I want proper authentication and access control, so that sensitive financial data is protected.

#### Acceptance Criteria

1. THE API_Gateway SHALL require API key authentication for all endpoints except /health and /docs
2. THE System SHALL support multiple API key tiers (free, professional, enterprise) with different rate limits
3. THE System SHALL log all API requests with API key, endpoint, timestamp, and response status
4. THE Admin_Dashboard SHALL require admin authentication separate from API keys
5. THE System SHALL not expose database credentials or internal configuration in API responses or logs
6. THE System SHALL not log sensitive information (full API keys, passwords) in application logs
7. THE System SHALL implement HTTPS-only in production environments
8. THE System SHALL implement CORS headers allowing only configured frontend origins

### Requirement 16: Deployment and DevOps

**User Story:** As a DevOps engineer, I want automated deployment and environment management, so that the system can be reliably deployed and updated.

#### Acceptance Criteria

1. THE System SHALL provide a Dockerfile for containerized deployment
2. THE System SHALL provide environment variable configuration via .env file for all deployment-specific settings
3. THE System SHALL implement health check endpoint GET /health returning service status and dependency health
4. THE System SHALL implement readiness check confirming database and Redis connectivity before accepting traffic
5. THE System SHALL provide database migration scripts for schema version management
6. THE System SHALL log to stdout in JSON format for centralized log aggregation
7. THE System SHALL expose Prometheus-compatible metrics endpoint for monitoring
8. THE System SHALL provide example docker-compose.yml for local development setup
9. THE System SHALL document environment variables required for production deployment

### Requirement 17: Documentation and Developer Experience

**User Story:** As a developer integrating with the API, I want comprehensive documentation, so that I can quickly understand and use the system.

#### Acceptance Criteria

1. THE System SHALL provide auto-generated OpenAPI documentation at /docs with request/response examples
2. THE System SHALL provide a README with quickstart guide, architecture overview, and deployment instructions
3. THE System SHALL provide example API requests and responses in documentation
4. THE System SHALL document all sector-specific configurations and their meanings
5. THE System SHALL document the F1-F5 filter pipeline with examples
6. THE System SHALL document the difference between UFRS_K and XI_29 TTM calculation
7. THE System SHALL provide a glossary of financial terms and Item Codes
8. THE System SHALL provide changelog documenting API changes between versions
9. THE System SHALL provide code examples in Python and JavaScript for common integration patterns

### Requirement 18: Graceful Degradation and Error Handling

**User Story:** As a system user, I want the system to continue functioning partially when external dependencies fail, so that service is not completely disrupted.

#### Acceptance Criteria

1. WHEN İş Yatırım API is unavailable, THE System SHALL return cached data with staleness indicator
2. WHEN Redis is unavailable, THE System SHALL fall back to database queries and log degraded performance
3. WHEN database query times out, THE System SHALL return HTTP 503 with retry-after header
4. WHEN ratio calculation fails for a company, THE System SHALL log the error and continue processing other companies
5. WHEN sector median calculation fails, THE System SHALL retain the previous cached median and mark it as stale
6. IF bootstrap process is interrupted, THE System SHALL resume from last successful company on restart
7. THE System SHALL never return HTTP 500 errors to clients; all errors SHALL be caught and returned as appropriate HTTP status codes
8. THE System SHALL implement request timeouts and circuit breakers for all external dependencies

### Requirement 19: Sektör Medyan Invalidation Strategy

**User Story:** As a system architect, I want intelligent cache invalidation, so that stale data is refreshed efficiently without excessive recalculation.

#### Acceptance Criteria

1. WHEN a company's ratios are updated, THE Cache_Manager SHALL invalidate the sector median cache for that company's Sector_Main
2. THE Cache_Manager SHALL NOT immediately recalculate sector medians upon invalidation
3. WHEN an invalidated sector median is requested via API, THE System SHALL trigger async recalculation and return stale data with is_stale=true flag
4. THE System SHALL implement lazy recalculation where medians are only recalculated when requested after invalidation
5. THE Cache_Manager SHALL group multiple invalidations within a 5-minute window into a single recalculation batch
6. THE System SHALL never serve sector median data older than 7 days, triggering forced recalculation if necessary
7. THE System SHALL prioritize sector median recalculation for sectors with higher API request frequency

### Requirement 20: Testing and Quality Assurance

**User Story:** As a quality assurance engineer, I want comprehensive automated testing, so that regressions are caught before deployment.

#### Acceptance Criteria

1. THE System SHALL include unit tests for Ratio_Calculator covering all ratio formulas
2. THE System SHALL include unit tests for F1-F5 filter pipeline with edge cases (empty data, single peer, all outliers)
3. THE System SHALL include integration tests for İş Yatırım API client with mocked responses
4. THE System SHALL include integration tests for database operations (CRUD, transactions, concurrent access)
5. THE System SHALL include API endpoint tests for all public endpoints with valid and invalid inputs
6. THE System SHALL include property-based tests for Parser ensuring round-trip property (parse -> print -> parse)
7. THE System SHALL include load tests simulating 100 concurrent users for performance validation
8. THE System SHALL achieve minimum 80% code coverage for business logic (services/, core/)
9. THE System SHALL run all tests automatically on git push via CI/CD pipeline
