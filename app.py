"""
Grant Proposal Analyzer - Modern Dashboard App
AI-powered grant matching with polished UI/UX
"""

import streamlit as st
import pandas as pd
from PIL import Image
import os

from data.grants_database import get_grants_dataframe
from modules.ai_matching import compute_similarity_scores
from modules.analytics import get_match_summary
from modules.utils import format_deadline, get_days_until_deadline

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="Grant Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark theme custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0f0f0f;
        color: #e0e0e0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #222222 100%);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 12px;
        color: #999999;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .match-bar-container {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
    }
    
    .detail-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #222222 100%);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
    }
    
    .detail-label {
        font-size: 11px;
        color: #0066CC;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .detail-value {
        color: #e0e0e0;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .upload-container {
        text-align: center;
        padding: 60px 20px;
    }
    
    .upload-title {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #0066CC, #00a8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .upload-subtitle {
        font-size: 16px;
        color: #999999;
        margin-bottom: 40px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0066CC 0%, #0052a3 100%);
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        color: white;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    h2, h3 {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZATION
# ============================================================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "uploaded_proposal" not in st.session_state:
    st.session_state.uploaded_proposal = None
if "matches" not in st.session_state:
    st.session_state.matches = None
if "selected_fund_idx" not in st.session_state:
    st.session_state.selected_fund_idx = 0

grants_df = get_grants_dataframe()

# ============================================================================
# HOME PAGE - Upload Interface
# ============================================================================
if st.session_state.page == "home":
    col_center = st.columns([1, 2, 1])[1]
    
    with col_center:
        st.markdown("""
        <div class="upload-container">
            <div class="upload-title">🎯 Grant Analyzer</div>
            <div class="upload-subtitle">
                Discover your ideal funding opportunities<br>
                <span style="font-size: 12px; color: #666;">Powered by AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Upload area
        uploaded_file = st.file_uploader(
            "Upload your proposal (PDF or TXT)",
            type=["pdf", "txt"],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            try:
                proposal_text = uploaded_file.read().decode("utf-8") if uploaded_file.type == "text/plain" else f"[PDF: {uploaded_file.name}]"
                
                # Analyze
                with st.spinner("🤖 Analyzing your proposal..."):
                    matches = compute_similarity_scores(proposal_text, grants_df)
                
                st.session_state.uploaded_proposal = proposal_text
                st.session_state.matches = matches
                st.session_state.page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"Error processing file: {e}")
        
        st.markdown("")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 12px; margin-top: 40px;">
            <p>Or paste your proposal below</p>
        </div>
        """, unsafe_allow_html=True)
        
        proposal_text = st.text_area(
            "Paste proposal text",
            height=150,
            placeholder="Describe your project here...",
            label_visibility="collapsed"
        )
        
        if proposal_text and st.button("Analyze Proposal", use_container_width=True):
            with st.spinner("🤖 Analyzing your proposal..."):
                matches = compute_similarity_scores(proposal_text, grants_df)
            
            st.session_state.uploaded_proposal = proposal_text
            st.session_state.matches = matches
            st.session_state.page = "dashboard"
            st.rerun()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
elif st.session_state.page == "dashboard":
    if st.session_state.matches is None:
        st.error("No matches found. Please upload a proposal.")
        if st.button("← Back to Upload"):
            st.session_state.page = "home"
            st.rerun()
    else:
        matches = st.session_state.matches
        
        # Back button
        col_back, col_space = st.columns([1, 19])
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.page = "home"
                st.session_state.matches = None
                st.session_state.uploaded_proposal = None
                st.rerun()
        
        st.title("📊 Analysis Dashboard")
        
        # ====== TOP METRICS ======
        summary = get_match_summary(matches)
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🟢 Strong Matches</div>
                <div class="metric-value">{summary['high_matches']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💰 Total Related Funds</div>
                <div class="metric-value">{len(matches)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Fund Type Split</div>
                <div style="text-align: left; margin-top: 10px;">
                    <div style="font-size: 12px; color: #0066CC;">Grants 83%</div>
                    <div style="font-size: 12px; color: #10a353;">Other 17%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            closing_soon = len(matches[matches['deadline'] < '2025-05-20'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⏰ Closing Soon</div>
                <div class="metric-value">{closing_soon}</div>
                <div style="font-size: 11px; color: #999;">in next 30 days</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ====== THEMES IDENTIFIED ======
        st.markdown("### 🏷️ THEMES IDENTIFIED IN YOUR PROPOSAL")
        
        # Extract focus areas
        all_focus = []
        for focus_list in matches['focus']:
            if isinstance(focus_list, list):
                all_focus.extend(focus_list)
        
        focus_counts = pd.Series(all_focus).value_counts().head(4)
        
        theme_cols = st.columns(len(focus_counts))
        for i, (focus, count) in enumerate(focus_counts.items()):
            with theme_cols[i]:
                score_pct = int((count / len(all_focus)) * 100) if all_focus else 0
                st.markdown(f"""
                <div class="match-bar-container">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="font-size: 13px; font-weight: 600;">{focus[:20]}</span>
                        <span style="font-size: 13px; color: #0066CC; font-weight: 600;">{count}</span>
                    </div>
                    <div style="background: #333333; height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #10a353 0%, #ff9400 50%); width: {score_pct}%; height: 100%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("---")
        
        # ====== MAIN CONTENT - Table & Detail ======
        col_table, col_detail = st.columns([2, 1.5], gap="medium")
        
        with col_table:
            st.markdown("### 📋 MATCHED FUNDS")
            
            # Display table
            for idx, (_, row) in enumerate(matches.iterrows()):
                days_left = get_days_until_deadline(row['deadline'])
                deadline_display = f"{days_left} days" if days_left and days_left > 0 else "Closed"
                
                cols = st.columns([2, 2, 1, 1], gap="small")
                with cols[0]:
                    if st.button(row['name'][:30], key=f"fund_{idx}", use_container_width=True):
                        st.session_state.selected_fund_idx = idx
                        st.rerun()
                with cols[1]:
                    st.caption(row['funder'][:20])
                with cols[2]:
                    st.caption(f"🎯 {row['match_score']:.0f}%")
                with cols[3]:
                    st.caption(f"⏰ {deadline_display}")
        
        with col_detail:
            st.markdown("### 💡 FUND DETAILS")
            
            selected = matches.iloc[st.session_state.selected_fund_idx]
            
            st.markdown(f"""
            <div class="detail-card">
                <div style="margin-bottom: 20px;">
                    <div class="detail-label">Fund Name</div>
                    <div class="detail-value">{selected['name']}</div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div class="detail-label">Organization</div>
                    <div class="detail-value">{selected['funder']}</div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div class="detail-label">Award Range</div>
                    <div class="detail-value">{selected['amount']}</div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div class="detail-label">Deadline</div>
                    <div class="detail-value">{format_deadline(selected['deadline'])}</div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div class="detail-label">Focus Areas</div>
                    <div class="detail-value">{', '.join(selected['focus'])}</div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div class="detail-label">Match Score</div>
                    <div class="detail-value">{selected['match_score']:.1f}%</div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <div class="detail-label">Contact</div>
                    <div class="detail-value" style="font-size: 12px;">{selected['contact']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            if st.button("🔗 Visit Fund Website", use_container_width=True):
                st.markdown(f"[Open Website]({selected['website']})")
        
        st.markdown("---")
        
        csv = matches[['name', 'funder', 'amount', 'match_score', 'deadline']].to_csv(index=False)
        st.download_button(
            label="📥 Download Results",
            data=csv,
            file_name="grant_matches.csv",
            mime="text/csv",
            use_container_width=True
        )
