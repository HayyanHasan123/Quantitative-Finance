# Stock Risk Analysis and Value at Risk (VaR) Model

# Overview
This project performs a **comprehensive risk analysis of a stock portfolio** using historical price data. It calculates **daily returns, volatility**, and **Value at Risk (VaR)** using three widely used methods: **Parametric**, **Historical**, and **Monte Carlo Simulation**. The project also includes detailed **visualizations** and **risk interpretations**.

# Objectives
- Analyze stock return behavior
- Measure portfolio risk using volatility
- Estimate potential losses using Value at Risk (VaR)
- Compare different VaR methodologies
- Visualize risk metrics for better interpretation

# Data Source
- Historical stock price data from **Yahoo Finance**
- Data downloaded using the `yfinance` library
- Example stock used: **Apple Inc. (AAPL)**

# Technologies Used
- Python
- pandas
- numpy
- numpy-financial
- yfinance
- matplotlib

# Financial Metrics Calculated
- Daily Returns
- Mean Daily Return
- Daily Volatility
- Annualized Volatility

# Value at Risk (VaR) Methods
- Parametric (Variance–Covariance) Method
- Historical Simulation Method
- Monte Carlo Simulation Method

# Assumptions
- 252 trading days in a year
- Portfolio value fixed at PKR 100,000
- Returns are assumed to follow a normal distribution (Parametric & Monte Carlo methods)

# Methodology
- Calculate daily percentage returns from closing prices
- Estimate volatility using standard deviation
- Compute VaR at 95% and 99% confidence levels
- Simulate returns using Monte Carlo techniques
- Compare VaR results across different methods

# Visualizations
- Time series plot of daily returns
- Histogram of historical daily returns
- Historical VaR thresholds (95% and 99%)
- Monte Carlo simulated return distribution
- Bar chart comparing VaR across methods

# Results Interpretation
- Parametric VaR provides quick risk estimates under normality assumptions
- Historical VaR captures real market behavior and tail risks
- Monte Carlo VaR allows flexible modeling and scenario-based analysis
- Comparison highlights differences in risk estimates across methodologies

# Project Structure
- Data loading and cleaning
- Return and volatility calculation
- VaR computation (three methods)
- Graphical analysis
- Text-based risk interpretation

# Use Cases
- Risk management practice
- Portfolio risk assessment
- Academic projects in finance and quantitative finance
- Learning financial risk modeling using Python

# How to Run
- Ensure historical stock CSV file is available
- Install required libraries
- Run the Python script
- View numerical outputs and generated plots

# Author
- Syed Muhammad Hayyan Hasan

# Disclaimer
This project is for educational and academic purposes only. The results should not be used as professional financial or investment advice.
