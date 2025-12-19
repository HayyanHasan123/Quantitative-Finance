# Quantitative-Finance

## ARIMA Model:
This is a predictive model designed to forecast price movements and volatility in NVDA (Nvidia) stock specifically around earnings announcement dates. The model analyzes historical percentage changes that occurred during 2025 earnings calls and uses ARIMA time series methodology to project similar patterns for 2026.
The twist here is that instead of analyzing continuous daily data, we're focused solely on high-impact events, quarterly earnings announcements when Jensen Huang and the NVDA executive team reveal financial results. These specific dates create significant market reactions due to investor sentiment, guidance updates, and financial performance reveals.
Based on our 2025 observations, NVDA showed extraordinary volatility during early 2025 earnings calls, driven by continued AI chip demand and data center growth, pushing the stock to new highs. However, later in 2025, we observed increased competition concerns and market saturation fears that led to more muted reactions and occasional selloffs post-earnings.
The 2026 predictions suggest a stabilization pattern, the model forecasts that NVDA will likely trade sideways around earnings dates with reduced volatility compared to early 2025's explosive movements. This indicates investors should consider a hold strategy with selective buying opportunities during dips, rather than expecting the dramatic gains seen in the AI boom period.

<img width="1280" height="612" alt="Arima 1" src="https://github.com/user-attachments/assets/c3605884-c44b-4128-b71e-0ce63eebc3e8" />

<img width="1280" height="612" alt="Arima 2" src="https://github.com/user-attachments/assets/afd44b24-33ae-4b78-816b-6073b9b877a1" />



## GARCH Model:
This volatility-focused model specifically measures and predicts the conditional volatility (risk level) of NVDA stock around earnings announcements. GARCH (Generalized Autoregressive Conditional Heteroskedasticity) excels at capturing volatility clustering, the phenomenon where high volatility periods tend to be followed by high volatility, and calm periods by calm periods.
For NVDA in 2025, we observed extreme volatility clustering around earnings dates, particularly when guidance exceeded or missed expectations. The early 2025 earnings showed massive volatility spikes as the market reacted to AI revenue projections and GPU supply constraints. Mid-to-late 2025 showed decreasing but still elevated volatility as the market began pricing in NVDA's dominant position.
The GARCH forecast for 2026 suggests mean reversion in volatility; we're expecting more normalized, lower volatility reactions compared to 2025's extremes. This implies that the "surprise factor" is diminishing as analysts and investors better understand NVDA's business model and growth trajectory.

<img width="1280" height="612" alt="Garch 1" src="https://github.com/user-attachments/assets/caa18d09-cf22-4baf-b20c-2669a338aebf" />

<img width="1280" height="612" alt="Garch 2" src="https://github.com/user-attachments/assets/96e5231b-417b-4f8c-99b7-b76b76f54c1a" />
