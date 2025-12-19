import yfinance as yf
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

'''def download_data(ticker, start="2020-01-01", end="2025-01-01"):
    """
    Download historical stock data from Yahoo Finance.
    """
    data = yf.download(ticker, start=start, end=end, auto_adjust=False)
    data.to_csv(f"{ticker}_data.csv")
    print(f"Data saved as {ticker}_data.csv")
    return data

ticker = "AAPL"  # Example
data = download_data(ticker, start="2023-01-01", end="2025-01-01")'''


# We will be calculating a few financial mertics first(volatility)

df = pd.read_csv("D:\\QF\\AAPL_data.csv")

# Finding daily return(mean)
df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
df = df.dropna(subset=['Close'])

aapl_daily_return = df['Close'].pct_change()
aapl_mean_daily_return = aapl_daily_return.mean()
print("mean daily return: ", aapl_mean_daily_return)

# Finding Volatility
daily_volatility = aapl_daily_return.std()
annual_volatility = daily_volatility *((252)**0.5)
print("Daily volatility ", daily_volatility)

# ----- VaR-----

# 1) Parametric Var
V = 100_000
# 95% confidence
z_95 = 1.65

Var_para_1 = V * (-aapl_mean_daily_return + z_95 * daily_volatility)
print("Var from parametric method at 95% confidence is: ", Var_para_1)

# 99% confidence
z_99 = 2.33
Var_para_2 = V * (-aapl_mean_daily_return + z_99 * daily_volatility)
print("Var from parametric method at 99% confidence is: ", Var_para_2)


# 2) Historical Method
percent_5th = aapl_daily_return.quantile(0.05)
percent_1th = aapl_daily_return.quantile(0.01)

Var_hist_95 = -V * percent_5th
Var_hist_99 = -V * percent_1th

print("Var from Historical Method in 95th percentile is: ", Var_hist_95)
print("Var from Historical Method in 99th percentile is: ", Var_hist_99)


# 3) Monte Carlo Simulation Method
Z = 100_000

simulated_returns = np.random.normal(aapl_mean_daily_return, daily_volatility, Z)
simulated_losses = -V * simulated_returns

# 95% and 99% Monte Carlo VaR
mc_var_95 = np.percentile(-simulated_returns*V, 95)
mc_var_99 = np.percentile(-simulated_returns*V, 99)


print("Monte Carlo VaR at 95% confidence:", mc_var_95)
print("Monte Carlo VaR at 99% confidence:", mc_var_99)


# ---- Graphical Rep ----

# Time series of daily returns
plt.figure(figsize=(12,6))
plt.plot(aapl_daily_return.index, aapl_daily_return, color='blue')
plt.title("AAPL Daily Returns")
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.grid(True)
plt.show()

# Histogram of daily returns
plt.figure(figsize=(10,6))
plt.hist(aapl_daily_return.dropna(), bins=50, color='skyblue', edgecolor='black')
plt.title("Distribution of AAPL Daily Returns")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.axvline(aapl_daily_return.quantile(0.05), color='red', linestyle='--', label='5% quantile (VaR 95%)')
plt.axvline(aapl_daily_return.quantile(0.01), color='orange', linestyle='--', label='1% quantile (VaR 99%)')
plt.legend()
plt.show()

# Historical VaR graph
plt.figure(figsize=(10,6))
plt.hist(aapl_daily_return.dropna(), bins=50, color='skyblue', edgecolor='black')
plt.title("Historical Daily Returns and VaR Levels")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.axvline(aapl_daily_return.quantile(0.05), color='red', linestyle='--', label='5% quantile (VaR 95%)')
plt.axvline(aapl_daily_return.quantile(0.01), color='orange', linestyle='--', label='1% quantile (VaR 99%)')

plt.legend()
plt.show()

# Monte carlo simulated VaR Graph
plt.figure(figsize=(10,6))
plt.hist(simulated_returns, bins=50, color='lightgreen', edgecolor='black')
plt.title("Monte Carlo Simulated Daily Returns for AAPL")
plt.xlabel("Simulated Daily Return")
plt.ylabel("Frequency")
plt.axvline(np.percentile(simulated_returns, 5), color='red', linestyle='--', label='5% quantile (VaR 95%)')
plt.axvline(np.percentile(simulated_returns, 1), color='orange', linestyle='--', label='1% quantile (VaR 99%)')
plt.legend()
plt.show()

# Comparing VaR
methods = ['Parametric 95%', 'Parametric 99%', 'Historical 95%', 'Historical 99%', 'Monte Carlo 95%', 'Monte Carlo 99%']
values = [Var_para_1, Var_para_2, Var_hist_95, Var_hist_99, mc_var_95, mc_var_99]  # use your calculated variables

plt.figure(figsize=(10,6))
plt.bar(methods, values, color=['skyblue','skyblue','orange','orange','green','green'])
plt.ylabel("VaR (Loss)")
plt.title("VaR Comparison Across Methods")
plt.xticks(rotation=45)
plt.show()



# ---- Interpretation ----
print(" INTERPRETATIONS \n")

print("---PARAMETRIC VaR---\n")
print(f"The 1-day 95% Parametric VaR of PKR {Var_para_1:.5f} means that there is only a 5% chance that the portfolio will lose more than PKR {Var_para_1:.5f} in a single day. \nThis method assumes returns are normally distributed, so it provides a quick estimate of potential losses.\n")
print(f"The 1-day 99% Parametric VaR of PKR {Var_para_2:.5f} means that there is only a 1% chance that the portfolio will lose more than PKR {Var_para_2:.5f} in a single day. \nThis method assumes returns are normally distributed, so it provides a quick estimate of potential losses.")
print(" ")
print("---HISTORICAL METHOD OF VaR---\n")
print(f"The 1-day 95% Historical VaR of PKR {Var_hist_95:.5f} indicates that based on actual past returns, the portfolio could lose more than PKR {Var_hist_95:.5f} on 5% of trading days.  \nThis method captures real market behavior, including extreme events that may not be normally distributed. It is useful for understanding risk based on historical data rather than assumptions.\n")
print(f"The 1-day 99% Historical VaR of PKR {Var_hist_99:.5f} indicates that based on actual past returns, the portfolio could lose more than PKR {Var_hist_99:.5f} on 1% of trading days.  \nThis method captures real market behavior, including extreme events that may not be normally distributed. It is useful for understanding risk based on historical data rather than assumptions.")
print(" ")
print("---Monte Carlo Simulation VaR---\n")
print(f"The 1-day 95% Monte Carlo VaR of PKR {mc_var_95:.5f} shows that after simulating 100,000 possible outcomes, the portfolio could lose more than PKR {mc_var_95:.5f} in 5% of scenarios.  \nMonte Carlo allows modeling complex portfolios and capturing non-linear risk patterns. This method is valuable when assessing portfolios with multiple assets or derivatives.\n")
print(f"The 1-day 99% Monte Carlo VaR of PKR {mc_var_99:.5f} shows that after simulating 100,000 possible outcomes, the portfolio could lose more than PKR {mc_var_99:.5f} in 1% of scenarios.  \nMonte Carlo allows modeling complex portfolios and capturing non-linear risk patterns. This method is valuable when assessing portfolios with multiple assets or derivatives.")