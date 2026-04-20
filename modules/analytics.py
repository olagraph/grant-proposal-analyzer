"""
Analytics Module
Provides data processing, statistics, and visualization helpers
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def get_grant_stats(grants_df):
    """
    Get grant statistics
    
    Args:
        grants_df (pd.DataFrame): DataFrame with grants
        
    Returns:
        dict: Statistics dictionary
    """
    stats = {
        "total_grants": len(grants_df),
        "avg_min_funding": extract_min_amount(grants_df['amount']).mean(),
        "avg_max_funding": extract_max_amount(grants_df['amount']).mean(),
        "focus_areas": grants_df['focus'].sum() if 'focus' in grants_df.columns else []
    }
    return stats


def extract_min_amount(amount_series):
    """Extract minimum funding amount from 'X - Y' format"""
    try:
        return amount_series.str.extract(r'\$?([\d,]+)').astype(str).str.replace(',', '').astype(float)
    except:
        return pd.Series([0] * len(amount_series))


def extract_max_amount(amount_series):
    """Extract maximum funding amount from 'X - Y' format"""
    try:
        return amount_series.str.extract(r'-\s*\$?([\d,]+)').astype(str).str.replace(',', '').astype(float)
    except:
        return pd.Series([0] * len(amount_series))


def visualize_match_distribution(matches_df):
    """
    Create a histogram of match scores
    
    Args:
        matches_df (pd.DataFrame): DataFrame with match_score column
    """
    if 'match_score' not in matches_df.columns or len(matches_df) == 0:
        st.info("No matches to visualize")
        return
    
    fig = px.histogram(
        matches_df,
        x='match_score',
        nbins=10,
        title='Match Score Distribution',
        labels={'match_score': 'Match Score (%)'},
        color_discrete_sequence=['#0066CC']
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def visualize_funding_amounts(grants_df):
    """
    Create a bar chart of funding ranges by grant
    
    Args:
        grants_df (pd.DataFrame): DataFrame with grants
    """
    if len(grants_df) == 0:
        return
    
    # Create a display dataframe with cleaned amounts
    display_df = grants_df[['name', 'amount']].copy()
    display_df['name'] = display_df['name'].str[:30]  # Truncate long names
    
    fig = px.bar(
        display_df,
        y='name',
        x='amount',
        title='Funding Amounts by Grant',
        labels={'name': 'Grant', 'amount': 'Funding Range'},
        orientation='h'
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def visualize_focus_areas(grants_df):
    """
    Create a chart of focus area frequency
    
    Args:
        grants_df (pd.DataFrame): DataFrame with focus column (list of strings)
    """
    if 'focus' not in grants_df.columns or len(grants_df) == 0:
        return
    
    # Flatten focus areas
    focus_areas = []
    for focus_list in grants_df['focus']:
        if isinstance(focus_list, list):
            focus_areas.extend(focus_list)
    
    focus_df = pd.Series(focus_areas).value_counts().reset_index()
    focus_df.columns = ['Focus Area', 'Count']
    
    fig = px.bar(
        focus_df,
        x='Focus Area',
        y='Count',
        title='Grant Focus Areas',
        color_discrete_sequence=['#0066CC']
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def create_matches_table(matches_df):
    """
    Create a formatted table of matches with key info
    
    Args:
        matches_df (pd.DataFrame): DataFrame with match results
        
    Returns:
        pd.DataFrame: Formatted results
    """
    if len(matches_df) == 0:
        return pd.DataFrame()
    
    display_cols = ['name', 'funder', 'amount', 'match_score', 'match_strength', 'deadline']
    available_cols = [col for col in display_cols if col in matches_df.columns]
    
    return matches_df[available_cols].copy()


def get_match_summary(matches_df):
    """
    Get a summary of match results
    
    Args:
        matches_df (pd.DataFrame): DataFrame with match results
        
    Returns:
        dict: Summary statistics
    """
    if 'match_score' not in matches_df.columns or len(matches_df) == 0:
        return {
            'high_matches': 0,
            'medium_matches': 0,
            'low_matches': 0,
            'avg_score': 0
        }
    
    return {
        'high_matches': len(matches_df[matches_df['match_score'] >= 70]),
        'medium_matches': len(matches_df[(matches_df['match_score'] >= 40) & (matches_df['match_score'] < 70)]),
        'low_matches': len(matches_df[matches_df['match_score'] < 40]),
        'avg_score': matches_df['match_score'].mean()
    }


def filter_grants_by_amount(grants_df, min_amount):
    """
    Filter grants by minimum funding amount
    
    Args:
        grants_df (pd.DataFrame): DataFrame with grants
        min_amount (int): Minimum funding amount in thousands
        
    Returns:
        pd.DataFrame: Filtered grants
    """
    min_funding = extract_min_amount(grants_df['amount'])
    return grants_df[min_funding >= min_amount * 1000].copy()
