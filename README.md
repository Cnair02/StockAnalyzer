# 📊 AI-Powered Stock Analyzer

A multi-agent AI platform that automates stock analysis using Google's Agent Development Kit (ADK) and Gemini AI. The application delivers real-time technical, fundamental, and sentiment analysis with actionable investment recommendations.

---

## 1.Project Overview

### Problem Statement
Traditional stock analysis requires investors to manually gather data from multiple sources—financial statements, technical charts, news articles, and market sentiment—which is time-consuming and prone to bias. Retail investors often lack the tools and expertise to synthesize this information into actionable insights.

### Solution
This AI-powered stock analyzer automates the entire research process using a multi-agent architecture. Each specialized AI agent focuses on a specific analysis dimension (technical, fundamental, sentiment), and a synthesizer agent combines their findings into a unified BUY/HOLD/SELL recommendation with price targets and risk assessment.

### Impact & Value
- **80% Time Reduction**: Manual analysis (2-3 hours) → Automated analysis (30-40 seconds)
- **Comprehensive Coverage**: 3 analysis dimensions (technical, fundamental, sentiment) in one report
- **Bias Reduction**: AI-driven synthesis eliminates emotional decision-making

---
## 2.Features

### 📈 Top 10 Stocks Generator
- Identifies today's top-performing stocks (biggest gainers)
- Displays current price, today's change, and previous day's trend
- Visual trend indicators (↑↓→) for quick insights

### 🔎 Individual Stock Analysis
Comprehensive analysis across three dimensions:
- **Technical Analysis**: RSI, price trends, technical ratings
- **Fundamental Analysis**: P/E ratio, market cap, revenue growth, valuation metrics
- **News & Sentiment**: Latest market news and sentiment scoring
- **AI Recommendation**: BUY/HOLD/SELL rating with target price and risk assessment

### 🤖 Multi-Agent Architecture
- **Sequential Processing**: Agents execute in optimized order for accurate synthesis
- **Real-time Data**: Live market data via Google Search integration
- **Smart Error Handling**: Comprehensive validation and user-friendly error messages

---

## 3.Tech Stack

| Component | Technology |
|-----------|-----------|
| **AI Framework** | Google Agent Development Kit (ADK) |
| **LLM** | Google Gemini 2.0 Flash |
| **Frontend** | Streamlit |
| **Language** | Python 3.11+ |
| **Deployment** | Streamlit Cloud |
| **Version Control** | GitHub |

---

## 4.Architecture

<img width="378" height="477" alt="Screenshot 2026-05-14 at 2 24 19 PM" src="https://github.com/user-attachments/assets/e492cb43-1af1-41f8-9355-e0b5922c6c9d" />


---

## 5.Screenshots

<img width="1128" height="778" alt="Screenshot 2026-05-14 at 2 19 57 PM" src="https://github.com/user-attachments/assets/b7fc57cf-d256-40db-bd8b-8748a0e322eb" />

---

## 6.Roadmap

### Watchlist & Portfolio Tracking
- **Personal Watchlist**: Save and monitor favorite stocks with real-time price alerts and daily performance summaries
- **Portfolio Analytics**: Track investment holdings with P&L calculations, diversification analysis, and performance benchmarking vs. S&P 500

### Advanced Visualizations & Charts
- **Interactive Price Charts**: Historical candlestick charts with technical indicators (RSI, MACD, Bollinger Bands) and customizable timeframes
- **Sector Heatmap**: Visual market overview showing sector performance, top gainers/losers, and correlation analysis

### AI-Powered Enhancements
- **Smart Stock Screener**: Natural language queries (e.g., "Find undervalued tech stocks with P/E < 20") and pre-built investment strategies
- **Predictive Analytics**: ML-based price forecasting, earnings surprise predictions, and automated entry/exit signals for trading opportunities

---
