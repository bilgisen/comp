"""
Valid Sectors Configuration - Fixture Data

Defines valid sector classifications and financial group mappings
for the HissePro Financial Analysis Engine.
"""

# 14 Main Sectors
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

# Sector to Financial Group Mapping
SECTOR_FINANCIAL_GROUP_MAPPING = {
    "Bankacılık & Finans": ["UFRS_K", "UFRS_F", "UFRS_S"],
    "_default": ["XI_29"],  # All other sectors use XI_29
}

# Financial Groups
BANKING_FINANCIAL_GROUPS = {"UFRS_K", "UFRS_F", "UFRS_S"}
INDUSTRIAL_FINANCIAL_GROUP = "XI_29"

# Sector to Ratio Configuration Mapping
SECTOR_RATIOS = {
    "Bankacılık & Finans": "BANKING_RATIOS",
    "_default": "DEFAULT_RATIOS"
}
