# Install required packages (run this once)
# !pip install pandas numpy matplotlib seaborn arch yfinance

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from arch import arch_model
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("All libraries imported successfully!")

# Step 1: Download NVDA stock data
print("\nDownloading NVDA stock data...")
nvda = yf.download('NVDA', start='2024-01-01', end='2025-12-31', progress=False)

# Fix multi-index columns issue
if isinstance(nvda.columns, pd.MultiIndex):
    nvda.columns = nvda.columns.droplevel(1)

nvda.index = pd.to_datetime(nvda.index)

# Calculate daily returns (percentage)
nvda['Returns'] = nvda['Close'].pct_change() * 100
nvda = nvda.dropna()

print(f"Downloaded {len(nvda)} days of NVDA data")
print(f"Date range: {nvda.index[0]} to {nvda.index[-1]}")

# Step 2: Define earnings announcement dates
earnings_dates_2025 = [
    '2025-02-26', '2025-05-28', '2025-08-27', '2025-11-19'
]

earnings_dates_2026 = [
    '2026-02-25', '2026-05-27', '2026-08-26', '2026-11-18'
]

# Step 3: Extract returns and volatility around earnings dates
def calculate_earnings_volatility(df, dates, window=5):
    """
    Calculate returns and realized volatility around earnings dates
    window: number of days to measure volatility
    """
    results = []
    
    for date_str in dates:
        date = pd.to_datetime(date_str)
        
        # Find the closest trading day
        if date in df.index:
            announcement_date = date
        else:
            future_dates = df.index[df.index >= date]
            if len(future_dates) > 0:
                announcement_date = future_dates[0]
            else:
                continue
        
        try:
            date_idx = df.index.get_loc(announcement_date)
            
            # Get window of returns around announcement
            start_idx = max(0, date_idx - window)
            end_idx = min(len(df), date_idx + window + 1)
            
            returns_window = df.iloc[start_idx:end_idx]['Returns']
            
            # Calculate realized volatility (standard deviation of returns)
            volatility = returns_window.std()
            mean_return = returns_window.mean()
            
            results.append({
                'Date': announcement_date,
                'Returns': df.loc[announcement_date, 'Returns'],
                'Volatility': volatility,
                'Mean_Return': mean_return
            })
        except:
            continue
    
    return pd.DataFrame(results).set_index('Date')

# Calculate 2025 volatility
print("\nCalculating 2025 earnings volatility...")
nvda_volatility_2025_df = calculate_earnings_volatility(nvda, earnings_dates_2025)

print("\n2025 NVDA Earnings Volatility:")
print(nvda_volatility_2025_df)

# Step 4: Prepare returns data for GARCH model
# Use returns around earnings dates
target_returns = nvda_volatility_2025_df['Returns']

print(f"\nTarget returns length: {len(target_returns)}")
print(f"Mean return: {target_returns.mean():.2f}%")
print(f"Volatility (std): {target_returns.std():.2f}%")

# Step 5: Fit GARCH(1,1) model
print("\nFitting GARCH(1,1) model...")
print("This may take a moment...")

try:
    # GARCH(1,1) is the most common specification
    # p=1 (ARCH term), q=1 (GARCH term)
    garch_model = arch_model(target_returns, vol='Garch', p=1, q=1, rescale=False)
    garch_fitted = garch_model.fit(disp='off')
    
    print("\nGARCH Model Summary:")
    print(garch_fitted.summary())
except Exception as e:
    print(f"Error: {e}")
    print("Using simpler ARCH(1) model...")
    garch_model = arch_model(target_returns, vol='Garch', p=1, q=0, rescale=False)
    garch_fitted = garch_model.fit(disp='off')

# Step 6: Forecast volatility for 2026
print("\n" + "="*60)
print("Forecasting 2026 Volatility")
print("="*60)

dates_2026_dt = pd.to_datetime(earnings_dates_2026)

if len(dates_2026_dt) > 0:
    horizon = len(dates_2026_dt)
    
    # GARCH forecast returns conditional variance
    garch_forecast = garch_fitted.forecast(horizon=horizon)
    
    # Extract forecasted variance and convert to volatility (std deviation)
    forecasted_variance = garch_forecast.variance.values[-1, :]
    forecasted_volatility = np.sqrt(forecasted_variance)
    
    # Create forecast dataframe
    nvda_volatility_2026_df = pd.DataFrame({
        'Predicted_Volatility': forecasted_volatility
    }, index=dates_2026_dt)
    
    # Calculate annualized volatility
    nvda_volatility_2026_df['Annualized_Volatility'] = \
        nvda_volatility_2026_df['Predicted_Volatility'] * np.sqrt(252)
    
    print("\nNVDA Stock Volatility Predictions for 2026 Earnings Dates:")
    print(nvda_volatility_2026_df)
    print("\nVolatility Statistics:")
    print(nvda_volatility_2026_df.describe())
    
    # Risk assessment
    avg_predicted_vol = nvda_volatility_2026_df['Predicted_Volatility'].mean()
    avg_actual_vol = nvda_volatility_2025_df['Volatility'].mean()
    volatility_change = ((avg_predicted_vol - avg_actual_vol) / avg_actual_vol) * 100
    
    print(f"\n--- Risk Assessment ---")
    print(f"2025 Average Volatility: {avg_actual_vol:.2f}%")
    print(f"2026 Average Volatility: {avg_predicted_vol:.2f}%")
    print(f"Volatility Change: {volatility_change:+.2f}%")
    
    if volatility_change > 10:
        print("\n⚠️  HIGH RISK: Increased volatility expected")
        print("   Strategy: Use protective options, reduce position size")
    elif volatility_change < -10:
        print("\n✓ LOW RISK: Decreased volatility expected")
        print("   Strategy: Favorable for directional trades")
    else:
        print("\n→ MODERATE RISK: Stable volatility expected")
        print("   Strategy: Maintain current risk management")
else:
    print("No earnings dates available for 2026 predictions.")

# Step 7: Visualization - Compare volatilities
print("\nGenerating volatility comparison chart...")

plt.figure(figsize=(14, 7))

# Plot actual 2025 volatility
plt.plot(nvda_volatility_2025_df.index,
         nvda_volatility_2025_df['Volatility'],
         label='2025 Actual Volatility',
         marker='o',
         linewidth=2.5,
         markersize=10,
         color='#D32F2F')  # Red

# Plot predicted 2026 volatility
plt.plot(nvda_volatility_2026_df.index,
         nvda_volatility_2026_df['Predicted_Volatility'],
         label='2026 Predicted Volatility',
         marker='s',
         linestyle='--',
         linewidth=2.5,
         markersize=10,
         color='#1976D2')  # Blue

plt.title('NVDA Stock Volatility: 2025 Actual vs 2026 GARCH Forecast', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Earnings Announcement Date', fontsize=12, fontweight='bold')
plt.ylabel('Volatility (%)', fontsize=12, fontweight='bold')
plt.legend(fontsize=11, loc='best', framealpha=0.9)
plt.grid(True, alpha=0.3, linestyle=':')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 8: Advanced visualization - Returns and Volatility
print("\nGenerating returns and volatility clustering chart...")

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Top plot: Returns
axes[0].plot(nvda_volatility_2025_df.index, 
             nvda_volatility_2025_df['Returns'], 
             color='#76B900', 
             linewidth=2, 
             marker='o',
             markersize=8,
             alpha=0.7,
             label='2025 Returns')
axes[0].axhline(y=0, color='black', linestyle='-', linewidth=1)
axes[0].set_title('NVDA Returns Around 2025 Earnings Dates', 
                  fontsize=14, fontweight='bold')
axes[0].set_ylabel('Returns (%)', fontsize=11, fontweight='bold')
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3, linestyle=':')

# Bottom plot: Conditional volatility
axes[1].plot(nvda_volatility_2025_df.index, 
             nvda_volatility_2025_df['Volatility'], 
             color='#D32F2F', 
             linewidth=2.5,
             marker='o',
             markersize=8,
             label='2025 Actual')
axes[1].plot(nvda_volatility_2026_df.index, 
             nvda_volatility_2026_df['Predicted_Volatility'], 
             color='#1976D2', 
             linewidth=2.5,
             marker='s',
             markersize=8,
             linestyle='--', 
             label='2026 Forecast')
axes[1].set_title('NVDA Conditional Volatility (GARCH Model)', 
                  fontsize=14, fontweight='bold')
axes[1].set_xlabel('Date', fontsize=11, fontweight='bold')
axes[1].set_ylabel('Volatility (%)', fontsize=11, fontweight='bold')
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3, linestyle=':')

plt.tight_layout()
plt.show()

# Step 9: Volatility regime analysis
print("\n" + "="*60)
print("Volatility Regime Analysis")
print("="*60)

max_vol_2026 = nvda_volatility_2026_df['Predicted_Volatility'].max()
min_vol_2026 = nvda_volatility_2026_df['Predicted_Volatility'].min()

print(f"\nMaximum Predicted Volatility: {max_vol_2026:.2f}%")
print(f"Minimum Predicted Volatility: {min_vol_2026:.2f}%")
print(f"Volatility Range: {max_vol_2026 - min_vol_2026:.2f}%")

# Classify volatility levels
for idx, row in nvda_volatility_2026_df.iterrows():
    vol = row['Predicted_Volatility']
    if vol > avg_predicted_vol * 1.2:
        regime = "HIGH"
        strategy = "Defensive positioning recommended"
    elif vol < avg_predicted_vol * 0.8:
        regime = "LOW"
        strategy = "Aggressive positioning possible"
    else:
        regime = "NORMAL"
        strategy = "Standard risk management"
    
    print(f"\n{idx.date()}: {vol:.2f}% - {regime} volatility")
    print(f"  → {strategy}")

print("\n" + "="*60)
print("GARCH Analysis Complete!")
print("="*60)