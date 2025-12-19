import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# =====================================================
# CORE FUNCTIONS - Stock Risk Analysis
# =====================================================

def download_data(ticker, start, end):
    """Download historical stock data from Yahoo Finance"""
    data = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    
    # Handle multi-level columns from yfinance
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    
    return data

def calculate_daily_returns(df):
    """Calculate daily returns from close prices"""
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Ensure Close is a Series, not DataFrame
    if isinstance(df['Close'], pd.DataFrame):
        close_prices = df['Close'].iloc[:, 0]
    else:
        close_prices = df['Close']
    
    # Convert to numeric
    close_prices = pd.to_numeric(close_prices, errors='coerce')
    
    # Remove NaN values
    close_prices = close_prices.dropna()
    
    # Calculate daily returns
    daily_return = close_prices.pct_change()
    
    return daily_return

def calculate_statistics(daily_return):
    """Calculate mean return and volatility"""
    mean_daily_return = daily_return.mean()
    daily_volatility = daily_return.std()
    annual_volatility = daily_volatility * ((252)**0.5)
    return mean_daily_return, daily_volatility, annual_volatility

# ----- VaR Methods -----

def parametric_var(V, mean_daily_return, daily_volatility, confidence_level):
    """Calculate Parametric VaR"""
    if confidence_level == 95:
        z_score = 1.65
    else:
        z_score = 2.33
    
    Var_para = V * (-mean_daily_return + z_score * daily_volatility)
    return Var_para

def historical_var(V, daily_return, confidence_level):
    """Calculate Historical VaR"""
    if confidence_level == 95:
        percentile = daily_return.quantile(0.05)
    else:
        percentile = daily_return.quantile(0.01)
    
    Var_hist = -V * percentile
    return Var_hist

def monte_carlo_var(V, mean_daily_return, daily_volatility, confidence_level, Z=100_000):
    """Calculate Monte Carlo VaR"""
    simulated_returns = np.random.normal(mean_daily_return, daily_volatility, Z)
    
    if confidence_level == 95:
        mc_var = np.percentile(-simulated_returns*V, 95)
    else:
        mc_var = np.percentile(-simulated_returns*V, 99)
    
    return mc_var, simulated_returns

def expected_shortfall(V, daily_return, confidence_level):
    """Calculate Expected Shortfall (CVaR)"""
    if confidence_level == 95:
        var_threshold = daily_return.quantile(0.05)
    else:
        var_threshold = daily_return.quantile(0.01)
    
    tail_losses = daily_return[daily_return <= var_threshold]
    CVaR = -V * tail_losses.mean()
    return CVaR

# ----- Visualization Functions -----

def plot_time_series(daily_return, ticker):
    """Plot time series of daily returns"""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(daily_return.index, daily_return, color='blue')
    ax.set_title(f"{ticker} Daily Returns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Return")
    ax.grid(True)
    return fig

def plot_histogram(daily_return, ticker, confidence_level):
    """Plot histogram of daily returns with VaR threshold"""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(daily_return.dropna(), bins=50, color='skyblue', edgecolor='black')
    ax.set_title(f"Distribution of {ticker} Daily Returns")
    ax.set_xlabel("Daily Return")
    ax.set_ylabel("Frequency")
    
    if confidence_level == 95:
        ax.axvline(daily_return.quantile(0.05), color='red', linestyle='--', label='5% quantile (VaR 95%)')
    else:
        ax.axvline(daily_return.quantile(0.01), color='orange', linestyle='--', label='1% quantile (VaR 99%)')
    ax.legend()
    return fig

def plot_monte_carlo(simulated_returns, ticker, confidence_level):
    """Plot Monte Carlo simulated returns"""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(simulated_returns, bins=50, color='lightgreen', edgecolor='black')
    ax.set_title(f"Monte Carlo Simulated Daily Returns for {ticker}")
    ax.set_xlabel("Simulated Daily Return")
    ax.set_ylabel("Frequency")
    
    if confidence_level == 95:
        ax.axvline(np.percentile(simulated_returns, 5), color='red', linestyle='--', label='5% quantile (VaR 95%)')
    else:
        ax.axvline(np.percentile(simulated_returns, 1), color='orange', linestyle='--', label='1% quantile (VaR 99%)')
    ax.legend()
    return fig

def plot_var_comparison(Var_para, Var_hist, mc_var, CVaR, confidence_level):
    """Plot comparison bar chart of all VaR methods"""
    methods = ['Parametric', 'Historical', 'Monte Carlo', 'CVaR']
    values = [Var_para, Var_hist, mc_var, CVaR]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(methods, values, color=['skyblue','orange','green','red'])
    ax.set_ylabel("VaR (Loss)")
    ax.set_title(f"VaR Comparison at {confidence_level}% Confidence")
    ax.grid(True, axis='y', alpha=0.3)
    return fig

# =====================================================
# STREAMLIT DASHBOARD
# =====================================================

import streamlit as st

# Page config
st.set_page_config(page_title="Stock Risk Analysis Dashboard", page_icon="📊", layout="wide")

st.title("📊 Stock Risk Analysis Dashboard")
st.markdown("**Value at Risk (VaR) & Expected Shortfall (CVaR) Analysis**")

# ---- Sidebar ----
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
V = st.sidebar.number_input("Investment Amount ($)", min_value=1000, max_value=10000000, value=100000, step=1000)
confidence_level = st.sidebar.selectbox("Confidence Level", options=[95, 99])

start_date = st.sidebar.date_input("Start Date", value=datetime.now() - timedelta(days=730))
end_date = st.sidebar.date_input("End Date", value=datetime.now())

run_button = st.sidebar.button("Run Analysis", type="primary")

# ---- Main Analysis ----
if run_button:
    
    # Download data
    try:
        data = download_data(ticker, start=start_date, end=end_date)
        if data.empty:
            st.error(f"No data found for ticker '{ticker}'")
            st.stop()
    except:
        st.error(f"Error fetching data for ticker '{ticker}'")
        st.stop()
    
    st.success(f"Data loaded for {ticker}: {len(data)} days")
    
    # Calculate daily returns
    daily_return = calculate_daily_returns(data)
    
    # Calculate statistics
    mean_daily_return, daily_volatility, annual_volatility = calculate_statistics(daily_return)
    
    # Display stats
    st.subheader("Portfolio Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investment", f"${V:,.0f}")
    col2.metric("Mean Daily Return", f"{mean_daily_return*100:.4f}%")
    col3.metric("Daily Volatility", f"{daily_volatility*100:.2f}%")
    col4.metric("Annual Volatility", f"{annual_volatility*100:.2f}%")
    
    st.markdown("---")
    
    # Calculate all VaR methods
    Var_para = parametric_var(V, mean_daily_return, daily_volatility, confidence_level)
    Var_hist = historical_var(V, daily_return, confidence_level)
    mc_var, simulated_returns = monte_carlo_var(V, mean_daily_return, daily_volatility, confidence_level)
    CVaR = expected_shortfall(V, daily_return, confidence_level)
    
    # Display VaR Results
    st.subheader(f"Risk Metrics at {confidence_level}% Confidence")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Parametric VaR", f"${Var_para:,.2f}")
    col2.metric("Historical VaR", f"${Var_hist:,.2f}")
    col3.metric("Monte Carlo VaR", f"${mc_var:,.2f}")
    col4.metric("Expected Shortfall (CVaR)", f"${CVaR:,.2f}")
    
    st.markdown("---")
    
    # Comparison table
    st.subheader("Risk Measure Comparison")
    comparison_data = {
        'Method': ['Parametric VaR', 'Historical VaR', 'Monte Carlo VaR', 'Expected Shortfall (CVaR)'],
        'Potential Loss ($)': [Var_para, Var_hist, mc_var, CVaR],
        'Loss %': [f"{(Var_para/V)*100:.2f}%", f"{(Var_hist/V)*100:.2f}%", 
                   f"{(mc_var/V)*100:.2f}%", f"{(CVaR/V)*100:.2f}%"]
    }
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ---- Visualizations ----
    st.subheader("Visual Analysis")
    
    # Time series of daily returns
    st.markdown("**Time Series of Daily Returns**")
    fig1 = plot_time_series(daily_return, ticker)
    st.pyplot(fig1)
    
    # Histogram and Monte Carlo side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Distribution of Daily Returns**")
        fig2 = plot_histogram(daily_return, ticker, confidence_level)
        st.pyplot(fig2)
    
    with col2:
        st.markdown("**Monte Carlo Simulated Returns**")
        fig3 = plot_monte_carlo(simulated_returns, ticker, confidence_level)
        st.pyplot(fig3)
    
    # VaR Comparison chart
    st.markdown("**VaR Comparison Across Methods**")
    fig4 = plot_var_comparison(Var_para, Var_hist, mc_var, CVaR, confidence_level)
    st.pyplot(fig4)
    
    st.markdown("---")
    
    # ---- Interpretation ----
    st.subheader("Interpretation")
    
    with st.expander("What is Value at Risk (VaR)?"):
        st.write(f"""
        **VaR** tells you the maximum expected loss over a time period at a given confidence level.
        
        At **{confidence_level}% confidence**, there is only a **{100-confidence_level}%** chance that your loss will exceed the VaR amount.
        
        **Parametric VaR**: Assumes returns are normally distributed. Uses mean and standard deviation.
        
        **Historical VaR**: Uses actual historical data without distribution assumptions. Looks at the worst {100-confidence_level}% of historical days.
        
        **Monte Carlo VaR**: Simulates 100,000 possible future scenarios based on historical statistics.
        
        **Your Results:**
        - Parametric VaR: ${Var_para:,.2f}
        - Historical VaR: ${Var_hist:,.2f}
        - Monte Carlo VaR: ${mc_var:,.2f}
        """)
    
    with st.expander("What is Expected Shortfall (CVaR)?"):
        st.write(f"""
        **CVaR** (Conditional VaR or Expected Shortfall) measures the **average loss** in the worst **{100-confidence_level}%** of cases.
        
        While VaR tells you the threshold, **CVaR tells you how bad it gets when you cross that threshold**.
        
        **Your CVaR**: ${CVaR:,.2f}
        
        This means if losses exceed the VaR threshold, the average loss would be ${CVaR:,.2f}.
        
        **Why it matters**: CVaR captures "tail risk" - extreme market events that VaR doesn't fully account for. 
        It's especially important for risk management because it considers the severity of worst-case scenarios, not just their probability.
        """)
    
    with st.expander("Key Assumptions and Limitations"):
        st.write("""
        **Parametric VaR Assumptions:**
        - Returns follow a normal distribution (often violated in real markets)
        - Volatility remains constant
        - No extreme events (fat tails)
        
        **Historical VaR Assumptions:**
        - Past patterns will repeat in the future
        - Limited by the historical period chosen
        - May miss rare events not in the data
        
        **Monte Carlo VaR Assumptions:**
        - Future returns follow the same statistical properties as the past
        - Normal distribution assumption (in our implementation)
        
        **General Limitations:**
        - All methods assume independent returns (no autocorrelation)
        - One-day horizon only
        - Doesn't account for liquidity risk
        - Market conditions can change rapidly
        - VaR says nothing about losses beyond the threshold
        
        **Best Practice**: Use multiple methods together and stress test your portfolio under extreme scenarios.
        """)

else:
    st.info("👈 Configure your analysis in the sidebar and click 'Run Analysis' to start")
    
    st.markdown("---")
    st.subheader("About This Dashboard")
    st.write("""
    This dashboard implements three industry-standard Value at Risk (VaR) methodologies:
    
    1. **Parametric VaR** - Based on normal distribution assumptions
    2. **Historical VaR** - Based on actual historical return distribution
    3. **Monte Carlo VaR** - Based on simulated scenarios (100,000 simulations)
    4. **Expected Shortfall (CVaR)** - Average loss beyond VaR threshold
    
    **Use Cases:**
    - Portfolio risk assessment
    - Capital allocation decisions
    - Regulatory compliance (Basel III)
    - Investment strategy evaluation
    """)