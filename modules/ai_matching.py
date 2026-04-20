"""
AI Matching Module
Uses Hugging Face sentence-transformers for semantic similarity matching
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import streamlit as st

MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'


@st.cache_resource
def load_model():
    """Load and cache the sentence transformer model"""
    return SentenceTransformer(MODEL_NAME)


def compute_similarity_scores(proposal_text, grants_df):
    """
    Compare proposal to all grants using semantic similarity.
    
    Args:
        proposal_text (str): The user's proposal text
        grants_df (pd.DataFrame): DataFrame containing grants with 'description' column
        
    Returns:
        pd.DataFrame: Grants sorted by match score (0-100)
    """
    if not proposal_text or not proposal_text.strip():
        return grants_df.copy()
    
    try:
        model = load_model()
        
        # Encode proposal
        proposal_embedding = model.encode(proposal_text, convert_to_tensor=True)
        
        # Encode grant descriptions
        grant_descriptions = grants_df['description'].tolist()
        grant_embeddings = model.encode(grant_descriptions, convert_to_tensor=True)
        
        # Calculate cosine similarity (0-1)
        similarities = util.cos_sim(proposal_embedding, grant_embeddings)[0]
        
        # Normalize to 0-100 and add to dataframe
        result_df = grants_df.copy()
        result_df['match_score'] = (similarities.cpu().numpy() * 100).round(2)
        result_df['match_strength'] = result_df['match_score'].apply(categorize_match)
        
        # Sort by match score descending
        return result_df.sort_values('match_score', ascending=False).reset_index(drop=True)
        
    except Exception as e:
        st.error(f"Error computing matches: {str(e)}")
        result_df = grants_df.copy()
        result_df['match_score'] = 0
        result_df['match_strength'] = 'No Match'
        return result_df


def categorize_match(score):
    """Categorize match strength based on score"""
    if score >= 70:
        return "🟢 High"
    elif score >= 40:
        return "🟡 Medium"
    else:
        return "🔴 Low"


def get_top_matches(proposal_text, grants_df, top_n=3):
    """Get top N matching grants"""
    results = compute_similarity_scores(proposal_text, grants_df)
    return results.head(top_n)


def explain_match(grant_name, proposal_text, grant_description, match_score):
    """
    Generate a simple explanation of why a grant matches the proposal
    
    Args:
        grant_name (str): Name of the grant
        proposal_text (str): User's proposal
        grant_description (str): Grant description
        match_score (float): Match score 0-100
        
    Returns:
        str: Explanation text
    """
    strength = categorize_match(match_score)
    
    # Find overlapping words for simple explanation
    proposal_words = set(proposal_text.lower().split())
    description_words = set(grant_description.lower().split())
    common_words = proposal_words & description_words
    
    explanation = f"{strength} Match ({match_score}%)\n\n"
    explanation += f"This grant aligns with your proposal's focus areas and keywords.\n"
    
    if common_words and len(common_words) > 2:
        common_keywords = ', '.join(sorted(list(common_words))[:5])
        explanation += f"Common terms: {common_keywords}"
    
    return explanation
