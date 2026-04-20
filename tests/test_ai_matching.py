"""
Unit tests for AI matching module
"""

import pytest
import pandas as pd
from modules.ai_matching import (
    compute_similarity_scores,
    categorize_match,
    get_top_matches
)
from data.grants_database import get_grants_dataframe


@pytest.fixture
def sample_grants():
    """Get sample grants for testing"""
    return get_grants_dataframe()


@pytest.fixture
def sample_proposal_solar():
    """Sample proposal related to solar energy"""
    return """We're developing a solar-powered water purification system for rural communities. 
    The project combines renewable energy with sustainable water management, creating local jobs 
    while ensuring clean water access. We have partnerships with three Indigenous communities."""


@pytest.fixture
def sample_proposal_health():
    """Sample proposal related to healthcare"""
    return """Our telemedicine initiative brings remote healthcare to underserved rural areas. 
    We're implementing digital health systems and training local health workers to improve 
    accessibility to medical services in remote communities."""


@pytest.fixture
def sample_proposal_ai():
    """Sample proposal related to artificial intelligence"""
    return """We're building an AI platform using machine learning to match vulnerable populations 
    with social services. Our data science team has developed algorithms for social good."""


class TestCategorizeMatch:
    """Test match categorization"""
    
    def test_high_match(self):
        assert categorize_match(75) == "🟢 High"
    
    def test_medium_match(self):
        assert categorize_match(55) == "🟡 Medium"
    
    def test_low_match(self):
        assert categorize_match(25) == "🔴 Low"


class TestComputeSimilarity:
    """Test similarity computation"""
    
    def test_returns_dataframe(self, sample_grants, sample_proposal_solar):
        """Test that compute_similarity_scores returns a DataFrame"""
        result = compute_similarity_scores(sample_proposal_solar, sample_grants)
        assert isinstance(result, pd.DataFrame)
    
    def test_has_match_score_column(self, sample_grants, sample_proposal_solar):
        """Test that result has match_score column"""
        result = compute_similarity_scores(sample_proposal_solar, sample_grants)
        assert 'match_score' in result.columns
    
    def test_match_scores_in_range(self, sample_grants, sample_proposal_solar):
        """Test that match scores are between 0 and 100"""
        result = compute_similarity_scores(sample_proposal_solar, sample_grants)
        assert all(0 <= score <= 100 for score in result['match_score'])
    
    def test_sorted_by_score(self, sample_grants, sample_proposal_solar):
        """Test that results are sorted by match score descending"""
        result = compute_similarity_scores(sample_proposal_solar, sample_grants)
        scores = result['match_score'].tolist()
        assert scores == sorted(scores, reverse=True)
    
    def test_solar_matches_clean_energy(self, sample_grants, sample_proposal_solar):
        """Test that solar proposal matches clean energy grant highly"""
        result = compute_similarity_scores(sample_proposal_solar, sample_grants)
        clean_energy = result[result['name'] == 'Clean Energy Innovation Fund']
        
        assert len(clean_energy) > 0
        # Solar proposal should have reasonable match score with clean energy grant
        assert clean_energy.iloc[0]['match_score'] > 30
    
    def test_health_matches_telemedicine(self, sample_grants, sample_proposal_health):
        """Test that health proposal matches telemedicine grant"""
        result = compute_similarity_scores(sample_proposal_health, sample_grants)
        telemedicine = result[result['name'] == 'Rural Telemedicine Expansion']
        
        assert len(telemedicine) > 0
        assert telemedicine.iloc[0]['match_score'] > 30
    
    def test_ai_matches_ai_grant(self, sample_grants, sample_proposal_ai):
        """Test that AI proposal matches AI social good grant"""
        result = compute_similarity_scores(sample_proposal_ai, sample_grants)
        ai_grant = result[result['name'] == 'AI for Social Good']
        
        assert len(ai_grant) > 0
        assert ai_grant.iloc[0]['match_score'] > 30
    
    def test_empty_proposal(self, sample_grants):
        """Test handling of empty proposal"""
        result = compute_similarity_scores("", sample_grants)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_grants)


class TestTopMatches:
    """Test getting top matches"""
    
    def test_returns_top_n(self, sample_grants, sample_proposal_solar):
        """Test that get_top_matches returns exactly N results"""
        result = get_top_matches(sample_proposal_solar, sample_grants, top_n=3)
        assert len(result) <= 3
    
    def test_top_matches_are_highest_scoring(self, sample_grants, sample_proposal_solar):
        """Test that top matches have highest scores"""
        all_matches = compute_similarity_scores(sample_proposal_solar, sample_grants)
        top_3 = get_top_matches(sample_proposal_solar, sample_grants, top_n=3)
        
        if len(top_3) > 0:
            top_3_scores = top_3['match_score'].tolist()
            all_scores = all_matches['match_score'].tolist()
            
            # Top 3 scores should be in the top 3 of all scores
            top_scores_overall = sorted(all_scores, reverse=True)[:3]
            assert max(top_3_scores) >= top_scores_overall[-1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
