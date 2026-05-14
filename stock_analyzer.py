"""
Fast Stock Analyzer - Clean Version
Based on previously working code
"""
from google.genai import types
from google.adk.agents import llm_agent, ParallelAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.adk.models.google_llm import Gemini
import asyncio
import logging  # Make sure this is here

# Set up logging - ADD THESE LINES
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Agent 1: Technical Analysis
def create_stock_analyzer():
    technical_agent = llm_agent.LlmAgent(
        model="-lite",
        name="TechnicalAnalyst",
        instruction="""
        Use Google Search to find for the given stock ticker:
        - Current stock price
        - RSI indicator
        - Price trend
        - Technical rating
        
        Keep response concise.
        """,
        tools=[google_search],
    )


    # Agent 2: Fundamental Analysis
    fundamental_agent = llm_agent.LlmAgent(
        model="-lite",
        name="FundamentalAnalyst",
        instruction="""
        Use Google Search to find for the given stock ticker:
        - Market cap
        - P/E ratio
        - Revenue growth
        - Valuation rating
        
        Keep response concise.
        """,
        tools=[google_search],
    )


    # Agent 3: News & Sentiment
    news_sentiment_agent = llm_agent.LlmAgent(
        model="-lite",
        name="NewsSentimentAnalyst",
        instruction="""
        Use Google Search to find latest news for the given stock ticker.
        
        Return: 1 sentence + sentiment + impact level.
        """,
        tools=[google_search],
    )


    sequential_analysts = SequentialAgent(
        name="SequentialAnalysts",
        sub_agents=[
            technical_agent,
            fundamental_agent,
            news_sentiment_agent
        ]
    )

    # Synthesizer
    synthesizer_agent = llm_agent.LlmAgent(
        model="-lite",
        name="RecommendationSynthesizer",
        instruction="""
        Create ONLY the final summary table from the 3 analyses.
        
        **STOCK ANALYSIS SUMMARY**
        
        | Category | Key Metric | Value | Rating |
        |----------|-----------|-------|--------|
        | Technical | Price / Trend | $XXX / Direction | RATING |
        | Fundamental | P/E / Growth | XX.X / XX% | RATING |
        | Sentiment | Latest News | Brief | RATING |
        
        **OVERALL:** BUY / HOLD / SELL
        
        **TARGET PRICE:** $XXX | **RISK:** LOW/MED/HIGH
        
        **THESIS:** [2 sentences]
        
        Output ONLY this final table.
        """
    )


    # Sequential Coordinator
    stock_analyzer = SequentialAgent(
        name="StockAnalyzer",
        sub_agents=[sequential_analysts, synthesizer_agent]
    )
    return stock_analyzer

def create_top_stocks_agent():
    top_stocks_agent = llm_agent.LlmAgent(
        model="-lite",
        name="TopStocksGenerator",
        instruction="""
        You are a top stocks identifier. Use Google Search to find:
        
        1. Today's top 10 performing stocks (by % gain) - check major market indexes
        2. For each stock, find:
           - Ticker symbol
           - Company name
           - Current price
           - Today's % change
           - Previous day's % change (yesterday)
           - Trend indicator (↑ if up, ↓ if down, → if flat)
        
        Format your response EXACTLY as a markdown table:
        
        **TOP 10 STOCKS TODAY** (May 13, 2026)
        
        | Rank | Ticker | Company | Current Price | Today Change | Yesterday Change | Trend |
        |------|--------|---------|---------------|--------------|------------------|-------|
        | 1 | XXX | Company Name | $XXX.XX | +X.XX% | +X.XX% | ↑ |
        | 2 | XXX | Company Name | $XXX.XX | +X.XX% | -X.XX% | ↑ |
        | 3 | XXX | Company Name | $XXX.XX | +X.XX% | +X.XX% | ↑ |
        | 4 | XXX | Company Name | $XXX.XX | +X.XX% | +X.XX% | ↑ |
        | 5 | XXX | Company Name | $XXX.XX | +X.XX% | -X.XX% | ↑ |
        | 6 | XXX | Company Name | $XXX.XX | +X.XX% | +X.XX% | ↑ |
        | 7 | XXX | Company Name | $XXX.XX | +X.XX% | +X.XX% | ↑ |
        | 8 | XXX | Company Name | $XXX.XX | +X.XX% | -X.XX% | ↑ |
        | 9 | XXX | Company Name | $XXX.XX | +X.XX% | +X.XX% | ↑ |
        | 10 | XXX | Company Name | $XXX.XX | +X.XX% | +X.XX% | ↑ |
        
        Use ↑ for positive yesterday change, ↓ for negative, → for minimal change.
        
        Search for "top performing stocks today" or "biggest stock gainers today" to find current data.
        """,
        tools=[google_search],
    )
    return top_stocks_agent

async def generate_top_10_async(top_stocks_agent):
    """Generate today's top 10 stocks with trend indicators"""
    try:
        logger.info("Starting top 10 stocks generation")
        
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            state={}, app_name="top_stocks", user_id="user"
        )
        
        runner = Runner(
            agent=top_stocks_agent,
            app_name="top_stocks",
            session_service=session_service
        )
        
        query = """Find today's top 10 performing stocks with trend indicators."""
        content = types.Content(role="user", parts=[types.Part(text=query)])
        
        events = runner.run_async(
            session_id=session.id, user_id="user", new_message=content
        )
        
        all_outputs = []
        async for event in events:
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        all_outputs.append(part.text)
        
        if not all_outputs:
            logger.warning("No top stocks data generated")
            return "⚠️ **Unable to retrieve top stocks data.** Please try again in a few moments."
        
        logger.info("Top 10 stocks generated successfully")
        return all_outputs[-1]
        
    except Exception as e:
        logger.error(f"Error generating top 10 stocks: {e}")
        return f"❌ **Error generating top stocks:** {str(e)}\n\nPlease try again or check your internet connection."
    






async def analyze_stock_async(ticker: str,stock_analyzer_agent):
    """Run stock analysis"""
    try:
        # Validate ticker input
        if not ticker or not isinstance(ticker, str):
            return "❌ **Error:** Invalid ticker symbol provided."
        
        ticker = ticker.strip().upper()
        
        if len(ticker) < 1 or len(ticker) > 5:
            return f"❌ **Error:** Ticker '{ticker}' is invalid. Please enter a valid 1-5 character ticker symbol."
        
        logger.info(f"Starting analysis for ticker: {ticker}")
        
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            state={}, app_name="stock_analyzer", user_id="user"
        )
        
        runner = Runner(
            agent=stock_analyzer_agent,
            app_name="stock_analyzer",
            session_service=session_service
        )
        
        query = f"Analyze stock ticker {ticker}. Provide final summary only."
        content = types.Content(role="user", parts=[types.Part(text=query)])
        
        events = runner.run_async(
            session_id=session.id, user_id="user", new_message=content
        )
        
        all_outputs = []
        async for event in events:
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        all_outputs.append(part.text)
        
        if not all_outputs:
            logger.warning(f"No analysis generated for {ticker}")
            return f"⚠️ **No data found for ticker '{ticker}'**. Please verify the ticker symbol is correct and try again."
        
        logger.info(f"Analysis completed successfully for {ticker}")
        return all_outputs[-1]
        
    except Exception as e:
        logger.error(f"Error analyzing stock {ticker}: {e}")
        return f"❌ **Error analyzing {ticker}:** {str(e)}\n\nPlease try again or contact support if the issue persists."



# ==================== SYNC WRAPPERS (for non-async environments) ====================

def analyze_stock(ticker: str, stock_analyzer_agent):
    """Sync wrapper - works in Streamlit and regular Python"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
    except RuntimeError:
        pass
    except Exception as e:
        logger.error(f"Error in event loop setup: {e}")
        return f"❌ **System Error:** Unable to initialize analysis engine. Please refresh the page."
    
    try:
        return asyncio.run(analyze_stock_async(ticker, stock_analyzer_agent))
    except Exception as e:
        logger.error(f"Error in analyze_stock wrapper: {e}")
        return f"❌ **Error:** Analysis failed. Please try again.\n\nDetails: {str(e)}"

# def analyze_stock(ticker: str, agent):
#     """Sync wrapper for analyze_stock_async"""
#     return asyncio.run(analyze_stock(ticker))



def generate_top_10(top_stocks_agent):
    """Sync wrapper - works in Streamlit and regular Python"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
    except RuntimeError:
        pass
    except Exception as e:
        logger.error(f"Error in event loop setup: {e}")
        return f"❌ **System Error:** Unable to initialize top stocks generator. Please refresh the page."
    
    try:
        return asyncio.run(generate_top_10_async(top_stocks_agent))
    except Exception as e:
        logger.error(f"Error in generate_top_10 wrapper: {e}")
        return f"❌ **Error:** Failed to generate top stocks. Please try again.\n\nDetails: {str(e)}"

# def generate_top_10(agent):
#     """Sync wrapper for generate_top_10_async"""
#     return asyncio.run(generate_top_10_stocks())
