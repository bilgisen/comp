from datetime import datetime, timezone

def health_handler() -> dict:
    return {
        "status": "healthy",
        "service": "temel",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def root_handler() -> dict:
    return {
        "message": "HissePro Temel Finansal Analiz API",
        "version": "1.0.0",
        "endpoints": {
            "companies": "/api/v1/companies",
            "ai": "/api/v1/ai"
        }
    }
