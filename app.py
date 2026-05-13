"""
Stock Analyzer Streamlit App
Imports core logic from stock_analyzer.py
"""
import streamlit as st
import os

# Import everything from our core module
from stock-analyzer import (
    create_stock_analyzer,
    create_top_stocks_agent,
    analyze_stock,
    generate_top_10
)


# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Stock Analyzer",
    page_icon="📊",
    layout="wide"
)


# ==================== API KEY SETUP ====================
# Use Streamlit secrets for deployment, environment variable for local
if 'GOOGLE_API_KEY' in st.secrets:
    os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
elif 'GOOGLE_API_KEY' not in os.environ:
    st.error("⚠️ GOOGLE_API_KEY not found. Please add it to secrets.toml")
    st.stop()


# ==================== INITIALIZE AGENTS ====================
@st.cache_resource
def initialize_agents():
    """Initialize agents (cached to avoid recreation)"""
    stock_analyzer = create_stock_analyzer()
    top_stocks_agent = create_top_stocks_agent()
    return stock_analyzer, top_stocks_agent


# ==================== STREAMLIT UI ====================

def main():
    # Initialize agents
    stock_analyzer, top_stocks_agent = initialize_agents()
    
    # Title and header
    st.title("📊 AI-Powered Stock Analyzer")
    st.markdown("**Multi-Agent Analysis** powered by Google ADK & Gemini")
    
    st.markdown("---")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # ===== LEFT: Top 10 Stocks =====
    with col1:
        st.header("📈 Top 10 Stocks Today")
        st.markdown("Get today's top performing stocks with trend indicators")
        
        if st.button("🔄 Generate Top 10 Stocks", use_container_width=True, type="primary"):
            with st.spinner("🔍 Searching for top performers..."):
                result = generate_top_10(top_stocks_agent)
                st.markdown(result)
    
    # ===== RIGHT: Individual Stock Analysis =====
    with col2:
        st.header("🔎 Analyze Specific Stock")
        st.markdown("Deep dive into technical, fundamental, and sentiment analysis")
        
        ticker_input = st.text_input(
            "Enter Stock Ticker",
            placeholder="e.g., AAPL, NVDA, GOOGL",
            help="Enter a valid stock ticker symbol"
        )
        
        if st.button("📊 Analyze Stock", use_container_width=True, type="primary"):
            if ticker_input:
                ticker = ticker_input.strip().upper()
                with st.spinner(f"🔍 Analyzing {ticker}..."):
                    result = analyze_stock(ticker, stock_analyzer)
                    st.markdown(result)
            else:
                st.warning("⚠️ Please enter a stock ticker")
    
    st.markdown("---")
    
    # ===== FOOTER =====
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Powered by <strong>Google ADK</strong> & <strong>Gemini AI</strong></p>
        <p>Multi-Agent System: Technical • Fundamental • News & Sentiment</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
