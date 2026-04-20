"""
Utility Functions
Helper functions for data processing
"""

import pandas as pd
from datetime import datetime


def format_deadline(deadline_str):
    """Format deadline string to readable format"""
    try:
        date_obj = datetime.strptime(deadline_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return deadline_str


def format_amount(amount_str):
    """Format funding amount string"""
    return amount_str


def get_days_until_deadline(deadline_str):
    """Calculate days remaining until deadline"""
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        today = datetime.now()
        days = (deadline - today).days
        return days
    except:
        return None


def categorize_by_focus(grants_df, focus_area):
    """Get grants matching a specific focus area"""
    if 'focus' not in grants_df.columns:
        return pd.DataFrame()
    
    matching = []
    for idx, focus_list in enumerate(grants_df['focus']):
        if isinstance(focus_list, list) and focus_area.lower() in [f.lower() for f in focus_list]:
            matching.append(idx)
    
    return grants_df.iloc[matching] if matching else pd.DataFrame()


def get_unique_focus_areas(grants_df):
    """Get all unique focus areas across grants"""
    if 'focus' not in grants_df.columns:
        return []
    
    focus_set = set()
    for focus_list in grants_df['focus']:
        if isinstance(focus_list, list):
            focus_set.update(focus_list)
    
    return sorted(list(focus_set))


def get_keywords_for_grant(grant):
    """Extract keywords from a grant"""
    if 'keywords' in grant and isinstance(grant['keywords'], list):
        return grant['keywords']
    return []


def get_requirements_for_grant(grant):
    """Extract requirements from a grant"""
    if 'requirements' in grant and isinstance(grant['requirements'], list):
        return grant['requirements']
    return []


def format_grant_for_display(grant):
    """Format a grant object for display"""
    return {
        'name': grant.get('name', 'N/A'),
        'funder': grant.get('funder', 'N/A'),
        'amount': grant.get('amount', 'N/A'),
        'deadline': format_deadline(grant.get('deadline', 'N/A')),
        'days_left': get_days_until_deadline(grant.get('deadline', '')),
        'focus_areas': ', '.join(grant.get('focus', [])),
        'description': grant.get('description', 'N/A'),
        'requirements': ', '.join(grant.get('requirements', [])),
        'website': grant.get('website', 'N/A'),
        'contact': grant.get('contact', 'N/A')
    }
