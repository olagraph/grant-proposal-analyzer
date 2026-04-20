"""
Grant Database
Sample grants inspired by real Canadian funding programs
"""

GRANTS_DATA = [
    {
        "id": 1,
        "name": "Clean Energy Innovation Fund",
        "funder": "Natural Resources Canada",
        "amount": "$50,000 - $500,000",
        "deadline": "2024-06-15",
        "focus": ["renewable energy", "sustainability", "climate action"],
        "keywords": ["solar", "wind", "battery", "grid", "emissions", "sustainability", "climate", "clean energy", "renewable"],
        "requirements": ["feasibility study", "community partnerships", "evaluation plan", "sustainability plan"],
        "description": "Supports innovative clean energy projects that reduce greenhouse gas emissions and promote renewable energy adoption.",
        "website": "https://www.nrcan.gc.ca/energy/funding/clean-energy-innovation",
        "contact": "cleanenergy@nrcan.gc.ca | (613) 996-2000"
    },
    {
        "id": 2,
        "name": "Indigenous Community Health Initiative",
        "funder": "Indigenous Services Canada",
        "amount": "$100,000 - $1,000,000",
        "deadline": "2024-07-30",
        "focus": ["indigenous-led initiatives", "healthcare access", "community health"],
        "keywords": ["indigenous", "first nations", "community health", "healthcare", "rural health", "accessibility", "wellness"],
        "requirements": ["community partnerships", "indigenous engagement", "evaluation plan", "cultural integration"],
        "description": "Funds projects led by or in partnership with Indigenous communities to improve health outcomes and access to healthcare services.",
        "website": "https://www.sac-isc.gc.ca/eng/health/funding-programs",
        "contact": "healthgrants@isc.gc.ca | 1-800-567-9604"
    },
    {
        "id": 3,
        "name": "Circular Economy Accelerator",
        "funder": "Environment and Climate Change Canada",
        "amount": "$75,000 - $750,000",
        "deadline": "2024-08-20",
        "focus": ["waste reduction", "circular economy", "sustainability"],
        "keywords": ["recycling", "upcycling", "waste", "materials", "circular", "lifecycle", "sustainable materials"],
        "requirements": ["feasibility study", "impact measurement", "sustainability plan", "partnerships"],
        "description": "Accelerates projects that transform waste into resources, promoting circular economy principles and reducing environmental impact.",
        "website": "https://www.canada.ca/en/environment-climate-change/services/funding/circular-economy",
        "contact": "circular.economy@ec.gc.ca | (819) 938-3860"
    },
    {
        "id": 4,
        "name": "Rural Telemedicine Expansion",
        "funder": "Health Canada",
        "amount": "$50,000 - $300,000",
        "deadline": "2024-09-10",
        "focus": ["healthcare access", "telemedicine", "rural health"],
        "keywords": ["telemedicine", "telehealth", "rural health", "remote care", "digital health", "accessibility", "healthcare"],
        "requirements": ["feasibility study", "community partnerships", "evaluation plan", "technology infrastructure"],
        "description": "Expands telemedicine services to underserved rural and remote communities, improving healthcare accessibility.",
        "website": "https://www.canada.ca/en/health-canada/services/health-care-system/telehealth",
        "contact": "telemedicine@hc-sc.gc.ca | (613) 957-2991"
    },
    {
        "id": 5,
        "name": "AI for Social Good",
        "funder": "Innovation, Science and Economic Development Canada",
        "amount": "$100,000 - $2,000,000",
        "deadline": "2024-10-05",
        "focus": ["artificial intelligence", "social impact", "innovation"],
        "keywords": ["artificial intelligence", "machine learning", "AI", "data science", "algorithm", "automation", "innovation"],
        "requirements": ["feasibility study", "impact measurement", "ethical framework", "evaluation plan"],
        "description": "Supports AI projects that address social challenges and create positive societal impact through innovative technology solutions.",
        "website": "https://www.ic.gc.ca/eic/site/icgc.nsf/eng/home",
        "contact": "ai.socialgood@ised-isde.gc.ca | 1-800-328-6189"
    },
    {
        "id": 6,
        "name": "Sustainable Agriculture Innovation",
        "funder": "Agriculture and Agri-Food Canada",
        "amount": "$75,000 - $500,000",
        "deadline": "2024-11-15",
        "focus": ["sustainable agriculture", "food security", "environmental sustainability"],
        "keywords": ["sustainable agriculture", "organic farming", "food security", "crop", "farming", "agriculture", "sustainability"],
        "requirements": ["feasibility study", "community partnerships", "evaluation plan", "sustainability plan"],
        "description": "Funds innovative agricultural practices that enhance food security while protecting the environment and supporting rural communities.",
        "website": "https://www.agr.gc.ca/eng/programs-and-services/sustainable-agriculture",
        "contact": "agri.innovation@agr.gc.ca | 1-866-367-8506"
    }
]


def get_grants_dataframe():
    """Convert grants data to pandas DataFrame"""
    import pandas as pd
    return pd.DataFrame(GRANTS_DATA)


def get_grant_by_id(grant_id):
    """Get a grant by its ID"""
    for grant in GRANTS_DATA:
        if grant["id"] == grant_id:
            return grant
    return None


def get_all_grants():
    """Get all grants"""
    return GRANTS_DATA
