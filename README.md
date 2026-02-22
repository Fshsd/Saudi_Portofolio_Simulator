# Saudi Market Investment Portfolio Simulator (TASI)

## Project Overview
I built this project as a practical assessment for my application at **Tarmeez Capital**. The goal is to help Saudi investors visualize how their stock choices would have performed in the past using real-time market data. As a Software Engineering graduate from Umm Al-Qura University, I wanted to create a tool that combines technical data engineering with a simple, user-friendly interface for stakeholders.

## Data Source
All the financial information in this dashboard is live and dynamic. I used the **Yahoo Finance API** (`yfinance`) to fetch the latest closing prices for major Saudi companies, such as **Aramco, Al Rajhi Bank, and stc**. I chose this source because it provides reliable, real-time data for the Saudi Stock Exchange (TASI).

## Methodology & Design
Following a professional ETL (Extract, Transform, Load) pipeline:
* **Data Cleaning & Transformation**: I applied a "Normalization" technique where all stock prices are scaled to start from a base value of 1.0. This is crucial for comparing stocks with vastly different price points.
* **Analysis Approach**: The simulator uses an "Equal Weight" portfolio strategy, distributing capital evenly across selected assets. It also calculates a live benchmark against the TASI index (`^TASI`) to measure alpha (market outperformance).
* **Tool Selection**: Python was chosen for its powerful data libraries (Pandas, Plotly), and Streamlit was used to deploy the project as a live, interactive web application.

## Key Insights & Stakeholder Recommendations
* **Diversification Impact**: The dashboard clearly shows how a diversified portfolio (e.g., mixing Banking and Energy) often yields more stable growth compared to single-stock investments.
* **Market Benchmarking**: By comparing the portfolio to TASI, stakeholders can identify if their specific stock picks are actually "beating the market."
* **Recommendation**: Investors should focus on high-growth sectors like Technology (Solutions) while maintaining a core position in stable giants like Aramco to balance volatility.

## Live Dashboard Link
👉 [**https://saudi-portfolio-simulator-fahad.streamlit.app/**]

## Assumptions & Limitations
* The model assumes an **Equal Weighting** strategy for simplicity.
* It does not account for transaction fees, taxes, or dividends.
* Historical performance is used as a simulator and does not guarantee future results.