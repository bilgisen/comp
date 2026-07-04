"""
pytest configuration and shared fixtures for audit_phase1 test suite
"""
import pytest
from sqlalchemy.orm import Session
from core.database import SessionLocal


@pytest.fixture(scope="session")
def db_session() -> Session:
    """Provide database session for tests (read-only access)"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_companies():
    """Reference companies for testing"""
    return {
        "banking": ["GARAN"],  # Garanti BBVA
        "industrial": ["THYAO", "EREGL"],  # Turkish Airlines, Ereğli Demir Çelik
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "unit: Unit tests for business logic")
    config.addinivalue_line("markers", "integration: Integration tests with real data")
    config.addinivalue_line("markers", "property: Property-based tests with Hypothesis")
    config.addinivalue_line("markers", "slow: Slow-running tests")
    config.addinivalue_line("markers", "requirement_1: Tests for Requirement 1 - Sector Classification")
    config.addinivalue_line("markers", "requirement_2: Tests for Requirement 2 - Item Code Mapping")
