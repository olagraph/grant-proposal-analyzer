"""
Grant Proposal Analyzer - Main Streamlit App
AI-powered grant matching using semantic similarity
"""

import streamlit as st
import pandas as pd
from PIL import Image
import os

from data.grants_database import get_grants_dataframe
from data.sample_proposals import SAMPLE_PROPOSALS, get_sample_proposal
from modules.ai_matching import compute_similarity_scores, categorize_match
from modules.analytics import (
    visualize_match_distribution,
    visualize_focus_areas,
    create_matches_table,
    get_match_summary,
    filter_grants_by_amount
)
from modules.utils import format_deadline, get_days_until_deadline

# Page config
st.set_page_config(
    page_title="Grant Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .high-match {
        color: #10a353;
        font-weight: bold;
    }
    .medium-match {
        color: #ff9400;
        font-weight: bold;
    }
    .low-match {
        color: #d33212;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.title("🎯 Grant Analyzer")

# Load and display logo if it exists
logo_path = "src/assets/analyzer-logo.png"
if os.path.exists(logo_path):
    try:
        logo = Image.open(logo_path)
        st.sidebar.image(logo, width=200)
    except:
        pass

st.sidebar.markdown("---")

# Input method selection
input_method = st.sidebar.radio(
    "📝 Input Method:",
    options=["Paste Text", "Use Sample", "Upload File"],
    help="Choose how to input your proposal"
)

proposal_text = ""

if input_method == "Use Sample":
    sample_name = st.sidebar.selectbox(
        "Select a Sample Proposal:",
        options=list(SAMPLE_PROPOSALS.keys()),
        help="Choose from pre-written example proposals"
    )
    proposal_text = get_sample_proposal(sample_name)
    st.sidebar.info(f"✅ Loaded: {sample_name}")

elif input_method == "Paste Text":
    proposal_text = st.sidebar.text_area(
        "Paste your proposal:",
        height=150,
        placeholder="Enter your project description here...",
        help="Describe your project, including problem, solution, impact, etc."
    )

elif input_method == "Upload File":
    uploaded_file = st.sidebar.file_uploader(
        "Upload a text file:",
        type=["txt", "pdf"],
        help="Upload a .txt or .pdf file containing your proposal"
    )
    if uploaded_file:
        try:
            proposal_text = uploaded_file.read().decode("utf-8")
            st.sidebar.success("✅ File loaded successfully")
        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")

# Filters
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")

min_funding = st.sidebar.slider(
    "Minimum Funding ($K):",
    min_value=0,
    max_value=2000,
    value=50,
    step=50,
    help="Filter grants by minimum funding amount"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**About:** AI-powered grant matching using semantic similarity analysis. "
    "Powered by [Hugging Face Transformers](https://huggingface.co)"
)

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.title("🎯 Grant Proposal Analyzer")
st.markdown("Find your ideal grant matches using AI-powered semantic analysis")

# Load grants database
grants_df = get_grants_dataframe()

# Initialize session state for results
if 'last_proposal' not in st.session_state:
    st.session_state.last_proposal = None
    st.session_state.matches = None

# Show character count and instructions
if proposal_text:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Proposal Length:** {len(proposal_text)} characters | {len(proposal_text.split())} words")
    with col2:
        if st.button("🔍 Analyze", use_container_width=True):
            st.session_state.last_proposal = proposal_text
else:
    st.info("👈 **Get Started:** Select or paste a proposal in the sidebar to analyze")

# ============================================================================
# RESULTS
# ============================================================================
if st.session_state.last_proposal:
    proposal_to_analyze = st.session_state.last_proposal
    
    # Filter by minimum funding
    filtered_grants = filter_grants_by_amount(grants_df, min_funding)
    
    if len(filtered_grants) == 0:
        st.warning(f"No grants found with minimum funding of ${min_funding}K")
    else:
        # Compute matches
        with st.spinner("🤖 Analyzing proposal with AI model..."):
            matches = compute_similarity_scores(proposal_to_analyze, filtered_grants)
        
        st.session_state.matches = matches
        
        # Summary metrics
        summary = get_match_summary(matches)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "🟢 High Matches",
                summary['high_matches'],
                help="Matches with 70%+ similarity"
            )
        with col2:
            st.metric(
                "🟡 Medium Matches",
                summary['medium_matches'],
                help="Matches with 40-69% similarity"
            )
        with col3:
            st.metric(
                "🔴 Low Matches",
                summary['low_matches'],
                help="Matches with <40% similarity"
            )
        with col4:
            st.metric(
                "📊 Avg Score",
                f"{summary['avg_score']:.1f}%",
                help="Average match score"
            )
        
        st.markdown("---")
        
        # Tabs for results
        tab1, tab2, tab3 = st.tabs(["📋 Rankings", "📊 Analytics", "ℹ️ Details"])
        
        # TAB 1: Rankings
        with tab1:
            st.subheader("Matched Grants (Ranked by Similarity)")
            
            # Display matches in expandable format
            for idx, (_, match) in enumerate(matches.iterrows(), 1):
                with st.expander(
                    f"{idx}. {match['name']} - {match['match_strength']} ({match['match_score']}%)",
                    expanded=(idx == 1)
                ):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Funder:** {match['funder']}")
                        st.markdown(f"**Funding:** {match['amount']}")
                        st.markdown(f"**Deadline:** {format_deadline(match['deadline'])}")
                        days_left = get_days_until_deadline(match['deadline'])
                        if days_left is not None:
                            if days_left > 0:
                                st.markdown(f"**Days Left:** ⏰ {days_left} days")
                            else:
                                st.markdown(f"**Status:** ❌ Deadline passed")
                        
                        st.markdown("**Focus Areas:** " + ", ".join(match['focus']))
                        st.markdown("**Description:** " + match['description'])
                        
                        if match.get('requirements'):
                            st.markdown("**Requirements:** " + ", ".join(match['requirements']))
                        
                        col_web, col_contact = st.columns(2)
                        with col_web:
                            st.markdown(f"[🔗 Visit Website]({match['website']})")
                        with col_contact:
                            st.markdown(f"**Contact:** {match['contact']}")
                    
                    with col2:
                        # Match score circle
                        score_color = "green" if match['match_score'] >= 70 else ("orange" if match['match_score'] >= 40 else "red")
                        st.markdown(f"""
                        <div style="
                            background-color: {score_color}20;
                            border: 3px solid {score_color};
                            border-radius: 50%;
                            width: 120px;
                            height: 120px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 32px;
                            font-weight: bold;
                        ">
                            {match['match_score']}%
                        </div>
                        """, unsafe_allow_html=True)
        
        # TAB 2: Analytics
        with tab2:
            st.subheader("Match Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Match Distribution**")
                visualize_match_distribution(matches)
            
            with col2:
                st.markdown("**Focus Areas**")
                visualize_focus_areas(matches)
        
        # TAB 3: Details Table
        with tab3:
            st.subheader("Detailed Results Table")
            
            display_table = create_matches_table(matches)
            
            if len(display_table) > 0:
                # Format for display
                display_table_copy = display_table.copy()
                display_table_copy['match_score'] = display_table_copy['match_score'].apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(
                    display_table_copy,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "name": st.column_config.TextColumn("Grant Name", width="medium"),
                        "funder": st.column_config.TextColumn("Funder", width="medium"),
                        "amount": st.column_config.TextColumn("Funding", width="small"),
                        "match_score": st.column_config.TextColumn("Match Score", width="small"),
                        "match_strength": st.column_config.TextColumn("Strength", width="small"),
                        "deadline": st.column_config.TextColumn("Deadline", width="small"),
                    }
                )
                
                # Download button
                csv = display_table.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv,
                    file_name="grant_matches.csv",
                    mime="text/csv"
                )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px;">
    <p>Grant Proposal Analyzer | Powered by Sentence-Transformers & Streamlit</p>
    <p><a href="https://github.com/15121connect/grant-proposal-analyzer">GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)
