"""
Sector Classification Test Module - Requirement 1

Validates that companies are correctly classified by sector_main and
financial_group, and identifies any mismatches.
"""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict, Any
from dataclasses import dataclass

from models.company import Company
from tests.audit_phase1.utilities.pretty_printer import PrettyPrinter
from tests.audit_phase1.utilities.validation_algorithms import validate_sector_financial_group


# Valid sectors (14 main sectors)
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


@dataclass
class ClassificationError:
    """Sector classification error"""
    ticker: str
    company_name: str
    sector_main: str
    financial_group: str
    expected_financial_group: str
    error_type: str  # "INVALID_SECTOR" | "MISMATCHED_GROUP"


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


class SectorClassificationTests:
    """Test suite for sector classification validation"""
    
    def __init__(self, db: Session):
        self.db = db
        self.printer = PrettyPrinter()
    
    def test_load_companies(self) -> List[Company]:
        """
        Load all active companies from database
        
        Returns:
            List of Company objects
        """
        stmt = select(Company).where(Company.is_active == True)
        result = self.db.execute(stmt)
        companies = result.scalars().all()
        
        return list(companies)
    
    def test_valid_sector_main(self, companies: List[Company]) -> Dict[str, Any]:
        """
        Verify each company's sector_main is in VALID_SECTORS list
        
        Args:
            companies: List of companies to validate
        
        Returns:
            Validation result with errors
        """
        errors = []
        
        for company in companies:
            if company.sector_main not in VALID_SECTORS:
                errors.append(ClassificationError(
                    ticker=company.ticker,
                    company_name=company.name,
                    sector_main=company.sector_main,
                    financial_group=company.financial_group,
                    expected_financial_group="N/A",
                    error_type="INVALID_SECTOR"
                ))
        
        return {
            "total_checked": len(companies),
            "errors": errors,
            "valid_count": len(companies) - len(errors)
        }
    
    def test_banking_financial_group(self, companies: List[Company]) -> Dict[str, Any]:
        """
        Verify banking companies have UFRS_K, UFRS_F, or UFRS_S financial_group
        
        Args:
            companies: List of companies to validate
        
        Returns:
            Validation result with errors
        """
        BANKING_SECTOR = "Bankacılık & Finans"
        BANKING_GROUPS = {"UFRS_K", "UFRS_F", "UFRS_S"}
        
        errors = []
        banking_companies = [c for c in companies if c.sector_main == BANKING_SECTOR]
        
        for company in banking_companies:
            if company.financial_group not in BANKING_GROUPS:
                errors.append(ClassificationError(
                    ticker=company.ticker,
                    company_name=company.name,
                    sector_main=company.sector_main,
                    financial_group=company.financial_group,
                    expected_financial_group="UFRS_K/F/S",
                    error_type="MISMATCHED_GROUP"
                ))
        
        return {
            "total_banking": len(banking_companies),
            "errors": errors,
            "valid_count": len(banking_companies) - len(errors)
        }
    
    def test_industrial_financial_group(self, companies: List[Company]) -> Dict[str, Any]:
        """
        Verify industrial companies have XI_29 financial_group
        
        Args:
            companies: List of companies to validate
        
        Returns:
            Validation result with errors
        """
        BANKING_SECTOR = "Bankacılık & Finans"
        INDUSTRIAL_GROUP = "XI_29"
        
        errors = []
        industrial_companies = [c for c in companies if c.sector_main != BANKING_SECTOR]
        
        for company in industrial_companies:
            if company.financial_group != INDUSTRIAL_GROUP:
                errors.append(ClassificationError(
                    ticker=company.ticker,
                    company_name=company.name,
                    sector_main=company.sector_main,
                    financial_group=company.financial_group,
                    expected_financial_group="XI_29",
                    error_type="MISMATCHED_GROUP"
                ))
        
        return {
            "total_industrial": len(industrial_companies),
            "errors": errors,
            "valid_count": len(industrial_companies) - len(errors)
        }
    
    def test_classification_errors(self, companies: List[Company]) -> List[ClassificationError]:
        """
        Flag all classification errors (invalid sectors + mismatched groups)
        
        Args:
            companies: List of companies to validate
        
        Returns:
            List of all classification errors
        """
        all_errors = []
        
        # Check for invalid sectors
        sector_result = self.test_valid_sector_main(companies)
        all_errors.extend(sector_result["errors"])
        
        # Check banking group mappings
        banking_result = self.test_banking_financial_group(companies)
        all_errors.extend(banking_result["errors"])
        
        # Check industrial group mappings
        industrial_result = self.test_industrial_financial_group(companies)
        all_errors.extend(industrial_result["errors"])
        
        return all_errors
    
    def calculate_sector_distribution(self, companies: List[Company]) -> Dict[str, int]:
        """
        Calculate company count per sector
        
        Args:
            companies: List of companies
        
        Returns:
            Dictionary mapping sector_main to company count
        """
        distribution = {}
        
        for company in companies:
            sector = company.sector_main
            if sector not in distribution:
                distribution[sector] = 0
            distribution[sector] += 1
        
        return distribution
    
    def generate_report(self, companies: List[Company]) -> SectorClassificationReport:
        """
        Generate comprehensive sector classification report
        
        Args:
            companies: List of companies to analyze
        
        Returns:
            SectorClassificationReport with all metrics
        """
        errors = self.test_classification_errors(companies)
        distribution = self.calculate_sector_distribution(companies)
        
        total = len(companies)
        misclassified = len(errors)
        correctly_classified = total - misclassified
        accuracy = (correctly_classified / total * 100) if total > 0 else 0.0
        
        report = SectorClassificationReport(
            total_companies=total,
            correctly_classified=correctly_classified,
            misclassified=misclassified,
            accuracy_percentage=accuracy,
            errors=errors,
            valid_sectors=VALID_SECTORS,
            sector_distribution=distribution
        )
        
        return report
    
    def print_report(self, report: SectorClassificationReport) -> str:
        """
        Format and print sector classification report
        
        Args:
            report: SectorClassificationReport object
        
        Returns:
            Formatted report string
        """
        lines = []
        
        lines.append("=" * 70)
        lines.append("SECTOR CLASSIFICATION TEST - REQUIREMENT 1")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"Total Companies: {report.total_companies}")
        lines.append(f"Correctly Classified: {report.correctly_classified}")
        lines.append(f"Misclassified: {report.misclassified}")
        lines.append(f"Accuracy: {report.accuracy_percentage:.2f}%")
        lines.append("")
        
        # Status
        if report.accuracy_percentage == 100.0:
            status = self.printer.colorize("✅ PASS", "green")
        elif report.accuracy_percentage >= 95.0:
            status = self.printer.colorize("⚠️ WARNING", "yellow")
        else:
            status = self.printer.colorize("❌ FAIL", "red")
        
        lines.append(f"Status: {status}")
        lines.append("")
        
        # Sector Distribution
        lines.append("## Sector Distribution")
        lines.append("")
        
        dist_data = []
        for sector in sorted(report.sector_distribution.keys()):
            count = report.sector_distribution[sector]
            pct = (count / report.total_companies * 100) if report.total_companies > 0 else 0
            dist_data.append({
                "sector": sector,
                "count": count,
                "percentage": f"{pct:.1f}%"
            })
        
        lines.append(self.printer.format_table(
            dist_data,
            ["sector", "count", "percentage"],
            align={"count": "right", "percentage": "right"}
        ))
        lines.append("")
        
        # Errors
        if report.errors:
            lines.append("## Classification Errors")
            lines.append("")
            
            error_data = []
            for error in report.errors[:20]:  # Show first 20
                error_data.append({
                    "ticker": error.ticker,
                    "sector": error.sector_main,
                    "group": error.financial_group,
                    "expected": error.expected_financial_group,
                    "error": error.error_type
                })
            
            lines.append(self.printer.format_table(
                error_data,
                ["ticker", "sector", "group", "expected", "error"]
            ))
            
            if len(report.errors) > 20:
                lines.append("")
                lines.append(f"... and {len(report.errors) - 20} more errors")
        else:
            lines.append("## No Classification Errors Found ✅")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)


@pytest.mark.integration
@pytest.mark.requirement_1
def test_sector_classification(db_session: Session):
    """
    Main test function for sector classification
    
    Validates:
        - All companies have valid sector_main values
        - Banking companies have correct financial_group
        - Industrial companies have correct financial_group
    """
    # Initialize test suite
    test_suite = SectorClassificationTests(db_session)
    
    # Load companies
    companies = test_suite.test_load_companies()
    assert len(companies) > 0, "No companies found in database"
    
    # Generate report
    report = test_suite.generate_report(companies)
    
    # Print report
    report_str = test_suite.print_report(report)
    print("\n" + report_str)
    
    # Assertions
    assert report.accuracy_percentage == 100.0, (
        f"Classification accuracy is {report.accuracy_percentage:.2f}%, "
        f"expected 100%. Found {report.misclassified} errors."
    )
    
    assert len(report.errors) == 0, f"Found {len(report.errors)} classification errors"
    
    # Verify all sectors are valid
    for sector in report.sector_distribution.keys():
        assert sector in VALID_SECTORS, f"Invalid sector found: {sector}"


@pytest.mark.integration
@pytest.mark.requirement_1
def test_no_null_sectors(db_session: Session):
    """Verify no companies have NULL sector_main values"""
    stmt = select(Company).where(
        (Company.is_active == True) & 
        (Company.sector_main.is_(None))
    )
    result = db_session.execute(stmt)
    null_companies = result.scalars().all()
    
    assert len(null_companies) == 0, (
        f"Found {len(null_companies)} companies with NULL sector_main"
    )


@pytest.mark.integration
@pytest.mark.requirement_1
def test_banking_sector_financial_group(db_session: Session):
    """Verify banking sector companies have UFRS_K/F/S"""
    BANKING_SECTOR = "Bankacılık & Finans"
    BANKING_GROUPS = {"UFRS_K", "UFRS_F", "UFRS_S"}
    
    stmt = select(Company).where(
        (Company.is_active == True) & 
        (Company.sector_main == BANKING_SECTOR)
    )
    result = db_session.execute(stmt)
    banking_companies = result.scalars().all()
    
    errors = []
    for company in banking_companies:
        if company.financial_group not in BANKING_GROUPS:
            errors.append(f"{company.ticker}: {company.financial_group}")
    
    assert len(errors) == 0, (
        f"Found {len(errors)} banking companies with wrong financial_group: {errors}"
    )


@pytest.mark.integration
@pytest.mark.requirement_1
def test_industrial_sector_financial_group(db_session: Session):
    """Verify industrial sector companies have XI_29"""
    BANKING_SECTOR = "Bankacılık & Finans"
    INDUSTRIAL_GROUP = "XI_29"
    
    stmt = select(Company).where(
        (Company.is_active == True) & 
        (Company.sector_main != BANKING_SECTOR)
    )
    result = db_session.execute(stmt)
    industrial_companies = result.scalars().all()
    
    errors = []
    for company in industrial_companies:
        if company.financial_group != INDUSTRIAL_GROUP:
            errors.append(f"{company.ticker}: {company.financial_group} (sector: {company.sector_main})")
    
    assert len(errors) == 0, (
        f"Found {len(errors)} industrial companies with wrong financial_group: {errors}"
    )
