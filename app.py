"""
Stock Analyzer Streamlit App
WITH COMPREHENSIVE ERROR HANDLING
"""
import streamlit as st
import os
import logging

# Set up logging - ADD THESE LINES
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import everything from our core module
from stock_analyzer import (
    create_stock_analyzer,
    create_top_stocks_agent,
    analyze_stock,
    generate_top_10
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Stock Analyzer",
    page_icon="📊",
    layout="wide"
)


# ==================== API KEY SETUP ====================
try:
    # Use Streamlit secrets for deployment
    if 'GOOGLE_API_KEY' in st.secrets:
        os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
        logger.info("API key loaded from Streamlit secrets")
    elif 'GOOGLE_API_KEY' in os.environ:
        logger.info("API key loaded from environment variables")
    else:
        st.error("⚠️ **Configuration Error:** GOOGLE_API_KEY not found.")
        st.info("Please add your Google API key to Streamlit secrets or environment variables.")
        st.stop()
except Exception as e:
    logger.error(f"Error loading API key: {e}")
    st.error(f"❌ **Error:** Unable to load API configuration.\n\nDetails: {str(e)}")
    st.stop()


# ==================== INITIALIZE AGENTS ====================
@st.cache_resource
def get_agents():
    """Initialize and return both agents (cached)"""
    try:
        logger.info("Initializing agents...")
        stock_analyzer = create_stock_analyzer()
        top_stocks_gen = create_top_stocks_agent()
        logger.info("Agents initialized successfully")
        return stock_analyzer, top_stocks_gen
    except Exception as e:
        logger.error(f"Error initializing agents: {e}")
        st.error(f"❌ **Initialization Error:** Unable to create AI agents.\n\nDetails: {str(e)}")
        st.stop()


# ==================== STREAMLIT UI ====================

def main():
    try:
        # Get both agents
        stock_analyzer, top_stocks_agent = get_agents()
        
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
                try:
                    with st.spinner("🔍 Searching for top performers..."):
                        logger.info("User clicked Generate Top 10 Stocks")
                        result = generate_top_10(top_stocks_agent)
                        
                        # Check if result contains an error message
                        if result.startswith("❌") or result.startswith("⚠️"):
                            st.error(result)
                        else:
                            st.markdown(result)
                            st.success("✅ Top 10 stocks generated successfully!")
                            
                except Exception as e:
                    logger.error(f"Error in Top 10 generation UI: {e}")
                    st.error(f"❌ **Error:** Unable to generate top stocks.\n\nDetails: {str(e)}")
                    st.info("💡 **Troubleshooting Tips:**\n- Check your internet connection\n- Refresh the page\n- Try again in a few moments")
        
        # ===== RIGHT: Individual Stock Analysis =====
        with col2:
            st.header("🔎 Analyze Specific Stock")
            st.markdown("Deep dive into technical, fundamental, and sentiment analysis")
            
            ticker_input = st.text_input(
                "Enter Stock Ticker",
                placeholder="e.g., AAPL, NVDA, GOOGL",
                help="Enter a valid stock ticker symbol (1-5 characters)",
                max_chars=5
            )
            
            if st.button("📊 Analyze Stock", use_container_width=True, type="primary"):
                if ticker_input:
                    try:
                        ticker = ticker_input.strip().upper()
                        
                        # Client-side validation
                        if not ticker.isalpha():
                            st.warning("⚠️ **Invalid Input:** Ticker should only contain letters (A-Z).")
                        elif len(ticker) < 1:
                            st.warning("⚠️ **Invalid Input:** Please enter a ticker symbol.")
                        else:
                            with st.spinner(f"🔍 Analyzing {ticker}..."):
                                logger.info(f"User analyzing ticker: {ticker}")
                                result = analyze_stock(ticker, stock_analyzer)
                                
                                # Check if result contains an error message
                                if result.startswith("❌") or result.startswith("⚠️"):
                                    st.error(result)
                                else:
                                    st.markdown(result)
                                    st.success(f"✅ Analysis for {ticker} completed!")
                                    
                    except Exception as e:
                        logger.error(f"Error in stock analysis UI for {ticker}: {e}")
                        st.error(f"❌ **Error:** Unable to analyze {ticker}.\n\nDetails: {str(e)}")
                        st.info("💡 **Troubleshooting Tips:**\n- Verify the ticker symbol is correct\n- Check if the market is open\n- Try a different stock")
                else:
                    st.warning("⚠️ **Missing Input:** Please enter a stock ticker symbol.")
        
        st.markdown("---")
        
        # ===== FOOTER =====
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Powered by <strong>Google ADK</strong> & <strong>Gemini AI</strong></p>
            <p>Multi-Agent System: Technical • Fundamental • News & Sentiment</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add helpful info in sidebar
        with st.sidebar:
            st.header("ℹ️ About")
            st.markdown("""
            This AI-powered stock analyzer uses multi-agent AI architecture to provide:
            
            - **Technical Analysis**: Price trends, RSI, MACD
            - **Fundamental Analysis**: P/E ratio, revenue, growth
            - **News & Sentiment**: Latest market sentiment
            
            **How to use:**
            1. Click "Generate Top 10 Stocks" for daily top performers
            2. Enter a ticker (e.g., AAPL) for detailed analysis
            
            **Note:** Analysis takes 20-40 seconds due to real-time data gathering.
            """)
            
            st.markdown("---")
            st.caption("Built with Google ADK & Streamlit")
        
    except Exception as e:
        logger.error(f"Critical error in main app: {e}")
        st.error(f"❌ **Critical Error:** The application encountered an unexpected error.\n\nDetails: {str(e)}")
        st.info("Please refresh the page. If the issue persists, contact support.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        st.error("❌ **Fatal Error:** Unable to start the application.")
        st.code(str(e))
