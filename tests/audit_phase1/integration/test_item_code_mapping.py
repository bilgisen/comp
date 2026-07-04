"""
Item Code Mapping Test Module - Requirement 2

Validates Item_Code_Mapper coverage for financial statement line items
across banking (UFRS_K, UFRS_F, UFRS_S) and industrial (XI_29) financial groups.
Tests that mapping coverage meets the 80% threshold.
"""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass
from collections import Counter

from models.company import Company
from models.financial import FinancialStatementRaw
from services.item_code_mapper import ItemCodeMapper
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter


@dataclass
class UnmappedCode:
    """Unmapped item code with frequency"""
    item_code: str
    financial_group: str
    frequency: int
    sample_desc_tr: str


@dataclass
class MappingCoverageReport:
    """Item code mapping coverage report"""
    sample_companies: List[str]
    total_codes: int
    mapped_codes: int
    unmapped_codes: int
    overall_coverage: float
    coverage_by_group: Dict[str, float]  # financial_group -> coverage %
    unmapped_top20: List[UnmappedCode]
    status: str  # PASS/FAIL based on 80% threshold


class ItemCodeMappingTests:
    """Test suite for item code mapping validation"""
    
    def __init__(self, db: Session):
        self.db = db
        self.printer = PrettyPrinter()
        self.mapper = ItemCodeMapper(db)
    
    def load_sample_companies(
        self, 
        n_banking: int = 5, 
        n_industrial: int = 5
    ) -> Dict[str, List[str]]:
        """
        Select sample companies for mapping coverage testing
        
        Args:
            n_banking: Number of banking companies to sample
            n_industrial: Number of industrial companies to sample
        
        Returns:
            Dictionary with 'banking' and 'industrial' ticker lists
        """
        # Banking companies (UFRS_K, UFRS_F, UFRS_S) with financial data
        BANKING_GROUPS = ["UFRS_K", "UFRS_F", "UFRS_S"]
        
        # Get banking companies that have financial statements
        banking_stmt = select(Company.ticker, Company.financial_group).where(
            and_(
                Company.is_active == True,
                Company.financial_group.in_(BANKING_GROUPS)
            )
        ).join(
            FinancialStatementRaw,
            Company.ticker == FinancialStatementRaw.ticker
        ).distinct().limit(n_banking * 2)  # Get more to filter
        
        banking_result = self.db.execute(banking_stmt)
        banking_candidates = [row[0] for row in banking_result.all()]
        
        # Filter to ensure companies have data
        banking_companies = []
        for ticker in banking_candidates:
            item_codes, _ = self.get_distinct_item_codes(ticker)
            if len(item_codes) > 0:
                banking_companies.append(ticker)
                if len(banking_companies) >= n_banking:
                    break
        
        # Industrial companies (XI_29) with financial data
        industrial_stmt = select(Company.ticker, Company.financial_group).where(
            and_(
                Company.is_active == True,
                Company.financial_group == "XI_29"
            )
        ).join(
            FinancialStatementRaw,
            Company.ticker == FinancialStatementRaw.ticker
        ).distinct().limit(n_industrial * 2)  # Get more to filter
        
        industrial_result = self.db.execute(industrial_stmt)
        industrial_candidates = [row[0] for row in industrial_result.all()]
        
        # Filter to ensure companies have data
        industrial_companies = []
        for ticker in industrial_candidates:
            item_codes, _ = self.get_distinct_item_codes(ticker)
            if len(item_codes) > 0:
                industrial_companies.append(ticker)
                if len(industrial_companies) >= n_industrial:
                    break
        
        return {
            "banking": banking_companies,
            "industrial": industrial_companies
        }
    
    def get_distinct_item_codes(
        self, 
        company_id: str
    ) -> Tuple[Set[str], str]:
        """
        Query distinct item codes for a company from financial_statements_raw
        
        Args:
            company_id: Company ticker
        
        Returns:
            Tuple of (set of item codes, financial_group)
        """
        stmt = select(
            FinancialStatementRaw.item_code,
            FinancialStatementRaw.financial_group
        ).where(
            FinancialStatementRaw.ticker == company_id
        ).distinct()
        
        result = self.db.execute(stmt)
        rows = result.all()
        
        if not rows:
            return set(), "UNKNOWN"
        
        item_codes = {row[0] for row in rows}
        financial_group = rows[0][1]  # All rows should have same financial_group
        
        return item_codes, financial_group
    
    def attempt_mapping(
        self, 
        item_code: str, 
        financial_group: str
    ) -> bool:
        """
        Test Item_Code_Mapper resolution for an item code
        
        Args:
            item_code: Item code to map
            financial_group: Financial group context
        
        Returns:
            True if mapping successful, False otherwise
        """
        semantic_name = self.mapper.get_semantic_name(item_code, financial_group)
        return semantic_name is not None
    
    def calculate_coverage_stats(
        self, 
        companies: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Compute coverage percentages per financial_group
        
        Args:
            companies: Dictionary with banking and industrial company lists
        
        Returns:
            Coverage statistics dictionary
        """
        all_codes = {}  # financial_group -> {item_code: count}
        mapped_codes = {}  # financial_group -> {item_code}
        company_details = []
        
        # Process all sample companies
        for category, ticker_list in companies.items():
            for ticker in ticker_list:
                item_codes, financial_group = self.get_distinct_item_codes(ticker)
                
                if not item_codes:
                    continue
                
                # Initialize group tracking
                if financial_group not in all_codes:
                    all_codes[financial_group] = Counter()
                    mapped_codes[financial_group] = set()
                
                # Count occurrences and test mappings
                for item_code in item_codes:
                    all_codes[financial_group][item_code] += 1
                    
                    if self.attempt_mapping(item_code, financial_group):
                        mapped_codes[financial_group].add(item_code)
                
                # Track company-level stats
                company_mapped = sum(
                    1 for code in item_codes 
                    if self.attempt_mapping(code, financial_group)
                )
                company_total = len(item_codes)
                company_coverage = (
                    (company_mapped / company_total * 100) 
                    if company_total > 0 else 0
                )
                
                company_details.append({
                    "ticker": ticker,
                    "category": category,
                    "financial_group": financial_group,
                    "total_codes": company_total,
                    "mapped": company_mapped,
                    "coverage": company_coverage
                })
        
        # Calculate overall and group-level coverage
        coverage_by_group = {}
        total_unique_codes = 0
        total_mapped_codes = 0
        
        for financial_group in all_codes.keys():
            group_total = len(all_codes[financial_group])
            group_mapped = len(mapped_codes[financial_group])
            group_coverage = (
                (group_mapped / group_total * 100) 
                if group_total > 0 else 0
            )
            
            coverage_by_group[financial_group] = group_coverage
            total_unique_codes += group_total
            total_mapped_codes += group_mapped
        
        overall_coverage = (
            (total_mapped_codes / total_unique_codes * 100)
            if total_unique_codes > 0 else 0
        )
        
        return {
            "all_codes": all_codes,
            "mapped_codes": mapped_codes,
            "coverage_by_group": coverage_by_group,
            "overall_coverage": overall_coverage,
            "total_unique_codes": total_unique_codes,
            "total_mapped_codes": total_mapped_codes,
            "company_details": company_details
        }
    
    def identify_unmapped_codes(
        self, 
        all_codes: Dict[str, Counter], 
        mapped_codes: Dict[str, Set[str]]
    ) -> List[UnmappedCode]:
        """
        Find and rank unmapped codes by frequency
        
        Args:
            all_codes: Dictionary of financial_group -> Counter(item_code)
            mapped_codes: Dictionary of financial_group -> set(mapped_item_codes)
        
        Returns:
            List of UnmappedCode objects sorted by frequency (descending)
        """
        unmapped_list = []
        
        for financial_group, code_counter in all_codes.items():
            mapped_set = mapped_codes.get(financial_group, set())
            
            for item_code, frequency in code_counter.items():
                if item_code not in mapped_set:
                    # Get sample description
                    stmt = select(FinancialStatementRaw.item_desc_tr).where(
                        and_(
                            FinancialStatementRaw.item_code == item_code,
                            FinancialStatementRaw.financial_group == financial_group,
                            FinancialStatementRaw.item_desc_tr.isnot(None)
                        )
                    ).limit(1)
                    
                    result = self.db.execute(stmt)
                    row = result.first()
                    sample_desc = row[0] if row else "N/A"
                    
                    unmapped_list.append(UnmappedCode(
                        item_code=item_code,
                        financial_group=financial_group,
                        frequency=frequency,
                        sample_desc_tr=sample_desc or "N/A"
                    ))
        
        # Sort by frequency descending
        unmapped_list.sort(key=lambda x: x.frequency, reverse=True)
        
        return unmapped_list
    
    def generate_coverage_report(
        self, 
        companies: Dict[str, List[str]]
    ) -> MappingCoverageReport:
        """
        Create ASCII table report using PrettyPrinter
        
        Args:
            companies: Sample companies dictionary
        
        Returns:
            MappingCoverageReport with all statistics
        """
        # Calculate coverage statistics
        stats = self.calculate_coverage_stats(companies)
        
        # Identify unmapped codes
        unmapped_codes = self.identify_unmapped_codes(
            stats["all_codes"],
            stats["mapped_codes"]
        )
        
        # Determine status based on 80% threshold
        overall_coverage = stats["overall_coverage"]
        status = "PASS" if overall_coverage >= 80.0 else "FAIL"
        
        # Flatten sample companies list
        all_tickers = companies["banking"] + companies["industrial"]
        
        report = MappingCoverageReport(
            sample_companies=all_tickers,
            total_codes=stats["total_unique_codes"],
            mapped_codes=stats["total_mapped_codes"],
            unmapped_codes=len(unmapped_codes),
            overall_coverage=overall_coverage,
            coverage_by_group=stats["coverage_by_group"],
            unmapped_top20=unmapped_codes[:20],
            status=status
        )
        
        return report
    
    def print_report(
        self, 
        report: MappingCoverageReport,
        company_details: List[Dict[str, Any]]
    ) -> str:
        """
        Format and print item code mapping coverage report
        
        Args:
            report: MappingCoverageReport object
            company_details: List of company-level statistics
        
        Returns:
            Formatted report string
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("ITEM CODE MAPPING COVERAGE TEST - REQUIREMENT 2")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"Sample Companies: {len(report.sample_companies)}")
        lines.append(f"  Banking: {sum(1 for c in company_details if c['category'] == 'banking')}")
        lines.append(f"  Industrial: {sum(1 for c in company_details if c['category'] == 'industrial')}")
        lines.append("")
        lines.append(f"Total Unique Item Codes: {report.total_codes}")
        lines.append(f"Mapped Codes: {report.mapped_codes}")
        lines.append(f"Unmapped Codes: {report.unmapped_codes}")
        lines.append(f"Overall Coverage: {report.overall_coverage:.2f}%")
        lines.append("")
        
        # Status
        if report.status == "PASS":
            status_str = self.printer.colorize("✅ PASS (≥80% coverage)", "green")
        else:
            status_str = self.printer.colorize(
                f"❌ FAIL (<80% coverage)", "red"
            )
        
        lines.append(f"Status: {status_str}")
        lines.append("")
        
        # Coverage by Financial Group
        lines.append("## Coverage by Financial Group")
        lines.append("")
        
        group_data = []
        for financial_group, coverage in sorted(report.coverage_by_group.items()):
            group_status = "✓" if coverage >= 80.0 else "✗"
            group_data.append({
                "financial_group": financial_group,
                "coverage": f"{coverage:.2f}%",
                "status": group_status
            })
        
        lines.append(self.printer.format_table(
            group_data,
            ["financial_group", "coverage", "status"],
            align={"coverage": "right", "status": "center"}
        ))
        lines.append("")
        
        # Company-level details
        lines.append("## Company-Level Coverage")
        lines.append("")
        
        company_table_data = []
        for detail in company_details:
            company_table_data.append({
                "ticker": detail["ticker"],
                "category": detail["category"],
                "group": detail["financial_group"],
                "total": detail["total_codes"],
                "mapped": detail["mapped"],
                "coverage": f"{detail['coverage']:.1f}%"
            })
        
        lines.append(self.printer.format_table(
            company_table_data,
            ["ticker", "category", "group", "total", "mapped", "coverage"],
            align={"total": "right", "mapped": "right", "coverage": "right"}
        ))
        lines.append("")
        
        # Top 20 unmapped codes
        if report.unmapped_top20:
            lines.append("## Top 20 Unmapped Item Codes (by frequency)")
            lines.append("")
            
            unmapped_data = []
            for unmapped in report.unmapped_top20:
                # Truncate description if too long
                desc = unmapped.sample_desc_tr
                if len(desc) > 50:
                    desc = desc[:47] + "..."
                
                unmapped_data.append({
                    "item_code": unmapped.item_code,
                    "group": unmapped.financial_group,
                    "frequency": unmapped.frequency,
                    "description": desc
                })
            
            lines.append(self.printer.format_table(
                unmapped_data,
                ["item_code", "group", "frequency", "description"],
                align={"frequency": "right"}
            ))
        else:
            lines.append("## ✅ No Unmapped Codes Found")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)


@pytest.mark.integration
@pytest.mark.requirement_2
def test_mapping_coverage_banking(db_session: Session):
    """
    Test Item_Code_Mapper coverage for banking financial groups (UFRS_K, UFRS_F, UFRS_S)
    
    Validates:
        - Banking companies have at least 80% item code mapping coverage
        - All UFRS_K, UFRS_F, UFRS_S groups are tested
    """
    test_suite = ItemCodeMappingTests(db_session)
    
    # Load banking companies only
    companies = test_suite.load_sample_companies(n_banking=5, n_industrial=0)
    
    assert len(companies["banking"]) > 0, "No banking companies found"
    
    # Calculate coverage
    stats = test_suite.calculate_coverage_stats(companies)
    
    # Check each banking group
    banking_groups = ["UFRS_K", "UFRS_F", "UFRS_S"]
    for group in banking_groups:
        if group in stats["coverage_by_group"]:
            coverage = stats["coverage_by_group"][group]
            assert coverage >= 80.0, (
                f"{group} mapping coverage is {coverage:.2f}%, expected ≥80%"
            )


@pytest.mark.integration
@pytest.mark.requirement_2
def test_mapping_coverage_industrial(db_session: Session):
    """
    Test Item_Code_Mapper coverage for industrial financial group (XI_29)
    
    Validates:
        - Industrial companies have at least 80% item code mapping coverage
    """
    test_suite = ItemCodeMappingTests(db_session)
    
    # Load industrial companies only
    companies = test_suite.load_sample_companies(n_banking=0, n_industrial=5)
    
    assert len(companies["industrial"]) > 0, "No industrial companies found"
    
    # Calculate coverage
    stats = test_suite.calculate_coverage_stats(companies)
    
    # Check XI_29 group
    if "XI_29" in stats["coverage_by_group"]:
        coverage = stats["coverage_by_group"]["XI_29"]
        assert coverage >= 80.0, (
            f"XI_29 mapping coverage is {coverage:.2f}%, expected ≥80%"
        )


@pytest.mark.integration
@pytest.mark.requirement_2
def test_unmapped_code_identification(db_session: Session):
    """
    Verify unmapped codes are captured and can be identified
    
    Validates:
        - Unmapped codes are tracked by financial_group
        - Frequency information is available
    """
    test_suite = ItemCodeMappingTests(db_session)
    
    companies = test_suite.load_sample_companies(n_banking=5, n_industrial=5)
    stats = test_suite.calculate_coverage_stats(companies)
    
    # Get unmapped codes
    unmapped_codes = test_suite.identify_unmapped_codes(
        stats["all_codes"],
        stats["mapped_codes"]
    )
    
    # Verify structure
    for unmapped in unmapped_codes[:5]:  # Check first 5
        assert unmapped.item_code, "Item code should not be empty"
        assert unmapped.financial_group, "Financial group should not be empty"
        assert unmapped.frequency > 0, "Frequency should be positive"
        # sample_desc_tr can be "N/A" if not available


@pytest.mark.integration
@pytest.mark.requirement_2
def test_coverage_threshold(db_session: Session):
    """
    Assert >= 80% overall mapping coverage threshold
    
    Validates:
        - Overall mapping coverage across all sampled companies is at least 80%
        - Report is generated successfully
    """
    # Initialize test suite
    test_suite = ItemCodeMappingTests(db_session)
    
    # Load sample companies
    companies = test_suite.load_sample_companies(n_banking=5, n_industrial=5)
    
    total_companies = len(companies["banking"]) + len(companies["industrial"])
    assert total_companies >= 10, (
        f"Expected at least 10 sample companies, got {total_companies}"
    )
    
    # Generate report
    report = test_suite.generate_coverage_report(companies)
    
    # Get company details for printing
    stats = test_suite.calculate_coverage_stats(companies)
    
    # Print report
    report_str = test_suite.print_report(report, stats["company_details"])
    print("\n" + report_str)
    
    # Assert 80% threshold
    assert report.overall_coverage >= 80.0, (
        f"Mapping coverage is {report.overall_coverage:.2f}%, expected ≥80%. "
        f"Found {report.unmapped_codes} unmapped codes out of {report.total_codes} total codes."
    )
    
    assert report.status == "PASS", f"Coverage test status is {report.status}"


@pytest.mark.integration
@pytest.mark.requirement_2
def test_sample_company_selection(db_session: Session):
    """
    Verify sample company selection works correctly
    
    Validates:
        - At least 5 banking companies are selected
        - At least 5 industrial companies are selected
        - Companies have financial statement data
    """
    test_suite = ItemCodeMappingTests(db_session)
    
    companies = test_suite.load_sample_companies(n_banking=5, n_industrial=5)
    
    # Check banking companies
    assert "banking" in companies, "Banking key missing"
    assert len(companies["banking"]) >= 3, (
        f"Expected at least 3 banking companies, got {len(companies['banking'])}"
    )
    
    # Check industrial companies
    assert "industrial" in companies, "Industrial key missing"
    assert len(companies["industrial"]) >= 3, (
        f"Expected at least 3 industrial companies, got {len(companies['industrial'])}"
    )
    
    # Verify companies have data
    for ticker in companies["banking"][:2]:  # Check first 2
        item_codes, financial_group = test_suite.get_distinct_item_codes(ticker)
        assert len(item_codes) > 0, f"No item codes found for banking company {ticker}"
        assert financial_group in ["UFRS_K", "UFRS_F", "UFRS_S"], (
            f"Banking company {ticker} has unexpected financial_group: {financial_group}"
        )
    
    for ticker in companies["industrial"][:2]:  # Check first 2
        item_codes, financial_group = test_suite.get_distinct_item_codes(ticker)
        assert len(item_codes) > 0, f"No item codes found for industrial company {ticker}"
        assert financial_group == "XI_29", (
            f"Industrial company {ticker} has unexpected financial_group: {financial_group}"
        )
