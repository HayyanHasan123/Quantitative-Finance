# Stock Risk Analysis Dashboard

An interactive web-based dashboard for comprehensive stock portfolio risk assessment using **Value at Risk (VaR)** and **Expected Shortfall (CVaR)** methodologies. Built with Python, Streamlit, and financial data from Yahoo Finance.

## Project Overview

This dashboard implements **four industry-standard risk measurement techniques** to quantify potential portfolio losses:

1. **Parametric VaR** - Statistical approach assuming normal distribution
2. **Historical VaR** - Non-parametric method using actual return distribution
3. **Monte Carlo VaR** - Simulation-based approach with 100,000 scenarios
4. **Expected Shortfall (CVaR)** - Tail risk measure for extreme loss scenarios

### Key Features

✅ **Dynamic Data Fetching** - Real-time stock data from Yahoo Finance  
✅ **Interactive Dashboard** - User-friendly Streamlit interface  
✅ **Multiple VaR Methods** - Compare different risk calculation approaches  
✅ **Tail Risk Analysis** - CVaR for understanding worst-case scenarios  
✅ **Visual Analytics** - Time series plots, histograms, and comparison charts  
✅ **Educational Content** - Built-in explanations of each methodology  
✅ **Flexible Configuration** - Customizable ticker, investment amount, confidence level, and date range

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/stock-risk-dashboard.git
cd stock-risk-dashboard
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit yfinance pandas numpy matplotlib
```

3. **Run the dashboard**
```bash
streamlit run app.py
```

4. **Open in browser**
The dashboard will automatically open at `http://localhost:8501`

---

## Project Structure

```
stock-risk-dashboard/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
└── assets/                # (Optional) Screenshots and images
    ├── dashboard_home.png
    ├── risk_metrics.png
    └── visualizations.png
```

---

## How to Use

### 1. Configure Analysis Parameters

Use the **sidebar** to customize your analysis:

- **Stock Ticker**: Enter any valid stock symbol (e.g., AAPL, GOOGL, TSLA, MSFT)
- **Investment Amount**: Specify portfolio value ($1,000 - $10,000,000)
- **Confidence Level**: Choose 95% or 99% confidence interval
- **Date Range**: Select start and end dates for historical data

### 2. Run Analysis

Click the **"Run Analysis"** button to:
- Download historical stock data
- Calculate daily returns and volatility
- Compute all VaR metrics and CVaR
- Generate visualizations

### 3. Interpret Results

The dashboard displays:

#### Portfolio Statistics
- Mean daily return
- Daily and annual volatility
- Investment value

#### Risk Metrics
- Parametric VaR
- Historical VaR
- Monte Carlo VaR
- Expected Shortfall (CVaR)

#### Visual Analysis
- Time series of daily returns
- Return distribution histograms
- Monte Carlo simulation results
- Comparative bar charts

#### Educational Content
- Detailed explanations of each method
- Assumptions and limitations
- Financial interpretation

---

## Methodology

### Parametric VaR

**Formula:**
```
VaR = Portfolio Value × (μ + z × σ)
```

Where:
- μ = mean daily return
- σ = daily volatility (standard deviation)
- z = z-score for confidence level (1.65 for 95%, 2.33 for 99%)

**Assumptions:**
- Returns follow normal distribution
- Constant volatility
- Independent returns

### Historical VaR

**Method:**
- Sorts historical returns from worst to best
- Identifies the percentile corresponding to confidence level
- 5th percentile for 95% confidence, 1st percentile for 99%

**Advantages:**
- No distribution assumptions
- Captures actual market behavior
- Includes real extreme events

### Monte Carlo VaR

**Process:**
1. Generate 100,000 random returns from normal distribution
2. Parameters: historical mean and volatility
3. Calculate portfolio losses for each simulation
4. Determine VaR at specified percentile

**Strengths:**
- Flexible modeling
- Can incorporate complex scenarios
- Industry standard for large portfolios

### Expected Shortfall (CVaR)

**Calculation:**
- Identifies returns worse than VaR threshold
- Computes average of these tail losses
- Provides conditional expected loss

**Why CVaR Matters:**
- Captures severity of worst-case scenarios
- Addresses VaR's limitation (doesn't show how bad losses can get)
- Preferred by Basel III banking regulations
- Better risk measure for portfolio optimization

---

## Example Output

### Sample Analysis for AAPL ($100,000 investment, 95% confidence)

| Risk Measure | Potential Loss | Loss % |
|--------------|----------------|--------|
| Parametric VaR | $3,245.67 | 3.25% |
| Historical VaR | $3,102.50 | 3.10% |
| Monte Carlo VaR | $3,198.34 | 3.20% |
| Expected Shortfall | $4,567.89 | 4.57% |

**Interpretation:**
- With 95% confidence, daily loss should not exceed ~$3,200
- If losses exceed VaR, average loss would be ~$4,568 (CVaR)
- Only 5% chance of losing more than VaR amount in a single day

---

## Technical Details

### Core Functions

#### Data Acquisition
```python
def download_data(ticker, start, end)
```
Fetches historical stock data from Yahoo Finance with multi-level column handling.

#### Return Calculation
```python
def calculate_daily_returns(df)
def calculate_statistics(daily_return)
```
Computes percentage changes, mean return, and volatility metrics.

#### VaR Calculations
```python
def parametric_var(V, mean_daily_return, daily_volatility, confidence_level)
def historical_var(V, daily_return, confidence_level)
def monte_carlo_var(V, mean_daily_return, daily_volatility, confidence_level, Z=100_000)
def expected_shortfall(V, daily_return, confidence_level)
```

#### Visualization
```python
def plot_time_series(daily_return, ticker)
def plot_histogram(daily_return, ticker, confidence_level)
def plot_monte_carlo(simulated_returns, ticker, confidence_level)
def plot_var_comparison(Var_para, Var_hist, mc_var, CVaR, confidence_level)
```

### Dependencies

```
streamlit>=1.28.0
yfinance>=0.2.28
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
```

---

## Educational Use Cases

This project is suitable for:

- **Quantitative Finance Courses**: Demonstrates risk management concepts
- **Portfolio Management**: Practical application of VaR methodologies
- **Financial Engineering**: Shows computational finance techniques
- **Data Science Projects**: Combines data analysis, visualization, and web development
- **Job Interviews**: Showcases practical Python skills in finance domain

---

## Limitations and Disclaimers

### Technical Limitations

1. **Parametric VaR**: Assumes normal distribution (markets have fat tails)
2. **Historical VaR**: Limited by historical period; past ≠ future
3. **Monte Carlo VaR**: Dependent on distribution assumptions
4. **All Methods**: 
   - One-day horizon only
   - Assumes independent returns
   - Doesn't account for liquidity risk or transaction costs

## Future Enhancements

Potential features for expansion:

- [ ] Multi-asset portfolio VaR with correlations
- [ ] Multi-day horizon VaR (5-day, 10-day, 21-day)
- [ ] Backtesting framework to validate VaR accuracy
- [ ] Stress testing and scenario analysis
- [ ] GARCH models for time-varying volatility
- [ ] Extreme Value Theory (EVT) for tail modeling
- [ ] PDF report export functionality
- [ ] Historical VaR breach analysis
- [ ] Sector and index comparison
- [ ] API integration for automated alerts

