"""
Mapping Integrity Test Module - Requirement 16

Validates round-trip consistency for item code to semantic name mappings.
Tests that forward mapping (item_code → semantic_name) and reverse mapping
(semantic_name → item_code) are consistent.
"""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict

from models.company import Company
from models.financial import FinancialStatementRaw
from services.item_code_mapper import ItemCodeMapper
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter


@dataclass
class RoundTripResult:
    """Round-trip mapping test result"""
    item_code: str
    financial_group: str
    semantic_name: str
    reverse_item_code: str
    is_consistent: bool
    error_type: str  # "SUCCESS" | "NO_REVERSE_MAPPING" | "MISMATCH"


@dataclass
class MappingIntegrityReport:
    """Mapping integrity report with round-trip statistics"""
    total_mappings: int
    consistent_mappings: int
    inconsistent_mappings: int
    consistency_rate: float
    inconsistencies_by_group: Dict[str, int]
    sample_inconsistencies: List[RoundTripResult]
    status: str  # PASS/FAIL based on 95% threshold


class MappingIntegrityTests:
    """Test suite for round-trip mapping consistency validation"""
    
    def __init__(self, db: Session):
        self.db = db
        self.printer = PrettyPrinter()
        self.mapper = ItemCodeMapper(db)
    
    def load_sample_companies(
        self, 
        n_banking: int = 3, 
        n_industrial: int = 3
    ) -> Dict[str, List[str]]:
        """
        Select sample companies for mapping integrity testing
        
        Args:
            n_banking: Number of banking companies to sample
            n_industrial: Number of industrial companies to sample
        
        Returns:
            Dictionary with 'banking' and 'industrial' ticker lists
        """
        # Banking companies
        BANKING_GROUPS = ["UFRS_K", "UFRS_F", "UFRS_S"]
        
        banking_stmt = select(Company.ticker).where(
            and_(
                Company.is_active == True,
                Company.financial_group.in_(BANKING_GROUPS)
            )
        ).join(
            FinancialStatementRaw,
            Company.ticker == FinancialStatementRaw.ticker
        ).distinct().limit(n_banking)
        
        banking_result = self.db.execute(banking_stmt)
        banking_companies = [row[0] for row in banking_result.all()]
        
        # Industrial companies
        industrial_stmt = select(Company.ticker).where(
            and_(
                Company.is_active == True,
                Company.financial_group == "XI_29"
            )
        ).join(
            FinancialStatementRaw,
            Company.ticker == FinancialStatementRaw.ticker
        ).distinct().limit(n_industrial)
        
        industrial_result = self.db.execute(industrial_stmt)
        industrial_companies = [row[0] for row in industrial_result.all()]
        
        return {
            "banking": banking_companies,
            "industrial": industrial_companies
        }
    
    def get_company_mappings(self, ticker: str) -> Tuple[Dict[str, str], str]:
        """
        Get all item code mappings for a company
        
        Args:
            ticker: Company ticker
        
        Returns:
            Tuple of (item_code -> semantic_name dict, financial_group)
        """
        # Get financial group
        company = self.db.execute(
            select(Company.financial_group).where(Company.ticker == ticker)
        ).first()
        
        if not company:
            return {}, "UNKNOWN"
        
        financial_group = company[0]
        
        # Get all distinct item codes for this company
        stmt = select(
            FinancialStatementRaw.item_code
        ).where(
            FinancialStatementRaw.ticker == ticker
        ).distinct()
        
        result = self.db.execute(stmt)
        item_codes = [row[0] for row in result.all()]
        
        # Map each item code to semantic name
        mappings = {}
        for item_code in item_codes:
            semantic_name = self.mapper.get_semantic_name(item_code, financial_group)
            if semantic_name:
                mappings[item_code] = semantic_name
        
        return mappings, financial_group
    
    def create_reverse_mapping(
        self, 
        forward_mappings: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """
        Create reverse mapping (semantic_name -> [item_codes])
        
        Args:
            forward_mappings: item_code -> semantic_name dict
        
        Returns:
            semantic_name -> list of item_codes dict
        
        Note: Multiple item codes can map to the same semantic name
        """
        reverse = defaultdict(list)
        for item_code, semantic_name in forward_mappings.items():
            reverse[semantic_name].append(item_code)
        return dict(reverse)
    
    def test_round_trip_consistency(
        self, 
        forward_mappings: Dict[str, str],
        financial_group: str
    ) -> List[RoundTripResult]:
        """
        Test round-trip consistency for all mappings
        
        Args:
            forward_mappings: item_code -> semantic_name dict
            financial_group: Financial group context
        
        Returns:
            List of RoundTripResult objects
        """
        results = []
        reverse_mappings = self.create_reverse_mapping(forward_mappings)
        
        for item_code, semantic_name in forward_mappings.items():
            # Check if semantic name has a reverse mapping
            if semantic_name not in reverse_mappings:
                results.append(RoundTripResult(
                    item_code=item_code,
                    financial_group=financial_group,
                    semantic_name=semantic_name,
                    reverse_item_code=None,
                    is_consistent=False,
                    error_type="NO_REVERSE_MAPPING"
                ))
                continue
            
            # Get reverse mapped item codes
            reverse_item_codes = reverse_mappings[semantic_name]
            
            # Check if original item_code is in reverse mapping
            if item_code in reverse_item_codes:
                results.append(RoundTripResult(
                    item_code=item_code,
                    financial_group=financial_group,
                    semantic_name=semantic_name,
                    reverse_item_code=item_code,
                    is_consistent=True,
                    error_type="SUCCESS"
                ))
            else:
                # Inconsistent - semantic name maps to different item code(s)
                results.append(RoundTripResult(
                    item_code=item_code,
                    financial_group=financial_group,
                    semantic_name=semantic_name,
                    reverse_item_code=reverse_item_codes[0] if reverse_item_codes else None,
                    is_consistent=False,
                    error_type="MISMATCH"
                ))
        
        return results
    
    def calculate_consistency_rate(
        self, 
        companies: Dict[str, List[str]]
    ) -> Dict[str, any]:
        """
        Calculate round-trip consistency rate across all sample companies
        
        Args:
            companies: Dictionary with banking and industrial company lists
        
        Returns:
            Statistics dictionary with consistency metrics
        """
        all_results = []
        company_stats = []
        inconsistencies_by_group = defaultdict(int)
        
        # Process all sample companies
        for category, ticker_list in companies.items():
            for ticker in ticker_list:
                forward_mappings, financial_group = self.get_company_mappings(ticker)
                
                if not forward_mappings:
                    continue
                
                # Test round-trip consistency
                results = self.test_round_trip_consistency(
                    forward_mappings,
                    financial_group
                )
                
                all_results.extend(results)
                
                # Calculate company-level stats
                consistent = sum(1 for r in results if r.is_consistent)
                total = len(results)
                rate = (consistent / total * 100) if total > 0 else 0
                
                company_stats.append({
                    "ticker": ticker,
                    "category": category,
                    "financial_group": financial_group,
                    "total_mappings": total,
                    "consistent": consistent,
                    "consistency_rate": rate
                })
                
                # Count inconsistencies by group
                for r in results:
                    if not r.is_consistent:
                        inconsistencies_by_group[financial_group] += 1
        
        # Calculate overall consistency rate
        total_mappings = len(all_results)
        consistent_mappings = sum(1 for r in all_results if r.is_consistent)
        consistency_rate = (
            (consistent_mappings / total_mappings * 100)
            if total_mappings > 0 else 0
        )
        
        # Get sample inconsistencies
        inconsistencies = [r for r in all_results if not r.is_consistent]
        sample_inconsistencies = inconsistencies[:10]  # Top 10
        
        return {
            "all_results": all_results,
            "company_stats": company_stats,
            "total_mappings": total_mappings,
            "consistent_mappings": consistent_mappings,
            "inconsistent_mappings": len(inconsistencies),
            "consistency_rate": consistency_rate,
            "inconsistencies_by_group": dict(inconsistencies_by_group),
            "sample_inconsistencies": sample_inconsistencies
        }
    
    def generate_report(
        self, 
        companies: Dict[str, List[str]]
    ) -> MappingIntegrityReport:
        """
        Generate mapping integrity report
        
        Args:
            companies: Sample companies dictionary
        
        Returns:
            MappingIntegrityReport with round-trip statistics
        """
        stats = self.calculate_consistency_rate(companies)
        
        # Determine status based on 95% threshold
        consistency_rate = stats["consistency_rate"]
        status = "PASS" if consistency_rate >= 95.0 else "FAIL"
        
        report = MappingIntegrityReport(
            total_mappings=stats["total_mappings"],
            consistent_mappings=stats["consistent_mappings"],
            inconsistent_mappings=stats["inconsistent_mappings"],
            consistency_rate=consistency_rate,
            inconsistencies_by_group=stats["inconsistencies_by_group"],
            sample_inconsistencies=stats["sample_inconsistencies"],
            status=status
        )
        
        return report
    
    def print_report(
        self, 
        report: MappingIntegrityReport,
        company_stats: List[Dict]
    ) -> str:
        """
        Format and print mapping integrity report
        
        Args:
            report: MappingIntegrityReport object
            company_stats: List of company-level statistics
        
        Returns:
            Formatted report string
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("MAPPING INTEGRITY TEST - REQUIREMENT 16")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"Sample Companies: {len(company_stats)}")
        lines.append(f"Total Mappings Tested: {report.total_mappings}")
        lines.append(f"Consistent Mappings: {report.consistent_mappings}")
        lines.append(f"Inconsistent Mappings: {report.inconsistent_mappings}")
        lines.append(f"Round-Trip Consistency Rate: {report.consistency_rate:.2f}%")
        lines.append("")
        
        # Status
        if report.status == "PASS":
            status_str = self.printer.colorize(
                "✅ PASS (≥95% consistency)", "green"
            )
        else:
            status_str = self.printer.colorize(
                f"❌ FAIL (<95% consistency)", "red"
            )
        
        lines.append(f"Status: {status_str}")
        lines.append("")
        
        # Consistency by Financial Group
        if report.inconsistencies_by_group:
            lines.append("## Inconsistencies by Financial Group")
            lines.append("")
            
            group_data = []
            for financial_group, count in sorted(report.inconsistencies_by_group.items()):
                group_data.append({
                    "financial_group": financial_group,
                    "inconsistent_count": count
                })
            
            lines.append(self.printer.format_table(
                group_data,
                ["financial_group", "inconsistent_count"],
                align={"inconsistent_count": "right"}
            ))
            lines.append("")
        
        # Company-level details
        lines.append("## Company-Level Consistency")
        lines.append("")
        
        company_table_data = []
        for stat in company_stats:
            company_table_data.append({
                "ticker": stat["ticker"],
                "category": stat["category"],
                "group": stat["financial_group"],
                "total": stat["total_mappings"],
                "consistent": stat["consistent"],
                "rate": f"{stat['consistency_rate']:.1f}%"
            })
        
        lines.append(self.printer.format_table(
            company_table_data,
            ["ticker", "category", "group", "total", "consistent", "rate"],
            align={"total": "right", "consistent": "right", "rate": "right"}
        ))
        lines.append("")
        
        # Sample inconsistencies
        if report.sample_inconsistencies:
            lines.append("## Sample Inconsistencies (Top 10)")
            lines.append("")
            
            inconsistency_data = []
            for inc in report.sample_inconsistencies:
                inconsistency_data.append({
                    "item_code": inc.item_code,
                    "semantic_name": inc.semantic_name[:30] + "..." if len(inc.semantic_name) > 30 else inc.semantic_name,
                    "reverse_code": inc.reverse_item_code or "N/A",
                    "error": inc.error_type,
                    "group": inc.financial_group
                })
            
            lines.append(self.printer.format_table(
                inconsistency_data,
                ["item_code", "semantic_name", "reverse_code", "error", "group"]
            ))
        else:
            lines.append("## ✅ No Inconsistencies Found")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)


@pytest.mark.integration
@pytest.mark.requirement_16
def test_round_trip_consistency_rate(db_session: Session):
    """
    Test round-trip mapping consistency rate >= 95%
    
    Validates:
        - Forward mapping (item_code → semantic_name) is reversible
        - Reverse mapping (semantic_name → item_code) matches original
        - Overall consistency rate is at least 95%
    """
    test_suite = MappingIntegrityTests(db_session)
    
    # Load sample companies
    companies = test_suite.load_sample_companies(n_banking=3, n_industrial=3)
    
    total_companies = len(companies["banking"]) + len(companies["industrial"])
    assert total_companies >= 6, (
        f"Expected at least 6 sample companies, got {total_companies}"
    )
    
    # Generate report
    report = test_suite.generate_report(companies)
    
    # Get company stats for printing
    stats = test_suite.calculate_consistency_rate(companies)
    
    # Print report
    report_str = test_suite.print_report(report, stats["company_stats"])
    print("\n" + report_str)
    
    # Assert 95% threshold
    assert report.consistency_rate >= 95.0, (
        f"Round-trip consistency is {report.consistency_rate:.2f}%, expected ≥95%. "
        f"Found {report.inconsistent_mappings} inconsistent mappings out of "
        f"{report.total_mappings} total mappings."
    )
    
    assert report.status == "PASS", f"Consistency test status is {report.status}"


@pytest.mark.integration
@pytest.mark.requirement_16
def test_banking_round_trip_consistency(db_session: Session):
    """
    Test round-trip consistency for banking financial groups (UFRS_K, UFRS_F, UFRS_S)
    
    Validates:
        - Banking companies have high mapping consistency
    """
    test_suite = MappingIntegrityTests(db_session)
    
    # Load banking companies only
    companies = test_suite.load_sample_companies(n_banking=3, n_industrial=0)
    
    assert len(companies["banking"]) > 0, "No banking companies found"
    
    # Calculate consistency
    stats = test_suite.calculate_consistency_rate(companies)
    
    # Check banking-specific consistency
    consistency_rate = stats["consistency_rate"]
    assert consistency_rate >= 95.0, (
        f"Banking round-trip consistency is {consistency_rate:.2f}%, expected ≥95%"
    )


@pytest.mark.integration
@pytest.mark.requirement_16
def test_industrial_round_trip_consistency(db_session: Session):
    """
    Test round-trip consistency for industrial financial group (XI_29)
    
    Validates:
        - Industrial companies have high mapping consistency
    """
    test_suite = MappingIntegrityTests(db_session)
    
    # Load industrial companies only
    companies = test_suite.load_sample_companies(n_banking=0, n_industrial=3)
    
    assert len(companies["industrial"]) > 0, "No industrial companies found"
    
    # Calculate consistency
    stats = test_suite.calculate_consistency_rate(companies)
    
    # Check industrial-specific consistency
    consistency_rate = stats["consistency_rate"]
    assert consistency_rate >= 95.0, (
        f"Industrial round-trip consistency is {consistency_rate:.2f}%, expected ≥95%"
    )


@pytest.mark.integration
@pytest.mark.requirement_16
def test_inconsistency_detection(db_session: Session):
    """
    Verify inconsistent mappings are properly detected and reported
    
    Validates:
        - Inconsistent mappings are tracked with error types
        - Error types are categorized correctly
    """
    test_suite = MappingIntegrityTests(db_session)
    
    companies = test_suite.load_sample_companies(n_banking=3, n_industrial=3)
    stats = test_suite.calculate_consistency_rate(companies)
    
    # Check that inconsistencies are detected
    inconsistencies = stats["sample_inconsistencies"]
    
    # Verify error type structure
    for inc in inconsistencies:
        assert inc.item_code, "Item code should not be empty"
        assert inc.semantic_name, "Semantic name should not be empty"
        assert inc.error_type in ["NO_REVERSE_MAPPING", "MISMATCH"], (
            f"Invalid error type: {inc.error_type}"
        )
        assert not inc.is_consistent, "Inconsistent mapping should have is_consistent=False"
