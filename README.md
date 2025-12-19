# Credit Risk Modeling Using Logistic Regression

# Overview
This project implements an **end-to-end credit risk modeling framework** using **Logistic Regression**. It simulates a real-world **credit scoring system** by generating borrower data, training a predictive model, evaluating performance using industry-standard metrics, and applying rule-based credit decisions.

# Objectives
- Build a binary classification model to predict loan default
- Simulate real-world borrower risk characteristics
- Evaluate model performance using statistical and ML metrics
- Translate model outputs into practical credit decisions
- Analyze model stability and distribution drift

# Dataset Description
- Synthetic credit dataset with 1,000 borrowers
- Features include income, debt, credit utilization, and payment history
- Target variable indicates loan default (binary)
- Debt-to-Income ratio engineered as a key credit metric

# Data Generation Logic
- Borrower characteristics generated using probabilistic distributions
- Default behavior derived from multiple risk factors
- Ensures realistic default rates and feature relationships
- Reproducible results using fixed random seed

# Feature Engineering
- Debt-to-Income Ratio calculation
- Selection of financially meaningful predictors
- Removal of noisy or irrelevant variables

# Model Selection
- Logistic Regression for interpretability and robustness
- StandardScaler applied for feature normalization
- Balanced class weighting to address class imbalance
- Pipeline-based implementation for clean workflow

# Model Training
- 80/20 train-test split with stratification
- Model trained on standardized financial features
- Probability-based default prediction (PD)

# Model Evaluation Metrics
- Confusion Matrix
- Precision, Recall, and F1-Score
- ROC Curve and ROC-AUC
- Kolmogorov–Smirnov (KS) Statistic

# Model Performance Interpretation
- ROC-AUC used to measure discriminatory power
- KS statistic used to assess separation between defaulters and non-defaulters
- Classification report provides class-level performance insights

# Feature Importance Analysis
- Logistic regression coefficients used for interpretability
- Positive coefficients indicate higher default risk
- Negative coefficients indicate risk-reducing factors

# Credit Decision Framework
- Probability of Default (PD)–based decision rules
- Approve: PD < 25%
- Review: 25% ≤ PD < 40%
- Reject: PD ≥ 40%
- Simulates real-world underwriting decisions

# Model Stability Analysis
- Population Stability Index (PSI) implemented
- Measures distribution shift between training and testing data
- Interprets model robustness over time

# Distribution Drift Analysis
- Feature-level distribution comparison
- KDE plots for training vs testing data
- Detects potential data drift risks

# Visualizations
- ROC Curve
- Feature distribution comparisons
- Probability distribution diagnostics
- Performance-driven plots for risk analysis

# Technologies Used
- Python
- pandas
- numpy
- scikit-learn
- seaborn
- matplotlib
- scipy

# Project Structure
- Data generation
- Feature engineering
- Model training
- Performance evaluation
- Decision logic
- Stability and drift analysis

# Use Cases
- Credit scoring systems
- Risk management analytics
- Fintech underwriting models
- Academic machine learning projects
- Quantitative finance applications

# Author
- Syed Muhammad Hayyan Hasan

# Disclaimer
This project is for educational and demonstration purposes only. The dataset is synthetic, and results should not be interpreted as real credit or lending advice.
