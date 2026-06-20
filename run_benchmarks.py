import asyncio
from core.database import AsyncSessionLocal
from services.sector_benchmarks import SectorBenchmarkService

async def main():
    print("Connecting to the database...")
    async with AsyncSessionLocal() as session:
        service = SectorBenchmarkService(session)
        print("Computing benchmarks for 'Ulaştırma & Lojistik' - '2026Q1'...")
        results = await service.compute_sector_benchmarks("Ulaştırma & Lojistik", "2026Q1")
        print(f"✅ Completed! Computed {len(results)} benchmarks:")
        for r in results:
            print(f"  - {r.ratio_code}: Median EW = {float(r.median_ew) if r.median_ew is not None else 'None'}, Sufficient = {r.is_sufficient}")
            
if __name__ == "__main__":
    asyncio.run(main())
