import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score
from scipy.stats import ks_2samp

# =====================================================
# DATA GENERATION - Creating Synthetic Credit Dataset
# =====================================================

print("Generating synthetic credit data...")

# Set random seed for reproducibility
np.random.seed(42)
num_samples = 1000

# Generate borrower features
borrower_age = np.random.randint(21, 65, size=num_samples)
annual_income = np.random.normal(50000, 15000, size=num_samples).astype(int)
total_debt = np.random.normal(15000, 5000, size=num_samples).astype(int)
payment_history_score = np.random.randint(0, 5, size=num_samples)
credit_utilization_ratio = np.round(np.random.uniform(0.1, 0.9, size=num_samples), 2)

# Create default indicator based on risk factors
# Higher debt, poor payment history, high utilization = higher default risk
default_indicator = (
    (total_debt > 18000).astype(int) +
    (payment_history_score < 2).astype(int) +
    (credit_utilization_ratio > 0.7).astype(int)
)

# Convert to binary: default if 2 or more risk factors present
loan_default = (default_indicator > 1).astype(int)

# Create DataFrame
credit_data = pd.DataFrame({
    'age': borrower_age,
    'income': annual_income,
    'debt': total_debt,
    'payment_history': payment_history_score,
    'credit_utilization': credit_utilization_ratio,
    'default': loan_default
})

# Calculate Debt-to-Income ratio (important credit metric)
credit_data['debt_to_income'] = (credit_data['debt'] / credit_data['income']).round(2)

print(f"Dataset created with {num_samples} borrowers")
print(f"Default rate: {credit_data['default'].mean():.1%}\n")

# =====================================================
# DATA PREPARATION - Train/Test Split
# =====================================================

# Select features for modeling
feature_columns = ['income', 'debt_to_income', 'credit_utilization', 'payment_history']
X_features = credit_data[feature_columns]
y_target = credit_data['default']

# Split data: 80% training, 20% testing
# stratify ensures same default rate in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X_features, 
    y_target, 
    test_size=0.2, 
    random_state=42,
    stratify=y_target
)

print(f"Training set: {len(X_train)} samples")
print(f"Testing set: {len(X_test)} samples\n")

# =====================================================
# MODEL TRAINING - Logistic Regression Pipeline
# =====================================================

print("Training credit risk model...")

# Create ML pipeline with scaling and logistic regression
credit_model = Pipeline([
    ('scaler', StandardScaler()),  # Standardize features
    ('classifier', LogisticRegression(
        class_weight='balanced',  # Handle imbalanced classes
        solver='lbfgs',
        max_iter=1000
    ))
])

# Train the model
credit_model.fit(X_train, y_train)

print("Model training complete!\n")

# =====================================================
# MODEL PREDICTIONS
# =====================================================

# Make predictions on test set
y_predictions = credit_model.predict(X_test)
y_probability = credit_model.predict_proba(X_test)[:, 1]  # Probability of default

# =====================================================
# MODEL EVALUATION METRICS
# =====================================================

print("=" * 50)
print("MODEL PERFORMANCE METRICS")
print("=" * 50)

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_predictions)
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nInterpretation:")
print(f"  True Negatives (Correctly predicted no default): {conf_matrix[0][0]}")
print(f"  False Positives (Predicted default but didn't): {conf_matrix[0][1]}")
print(f"  False Negatives (Missed actual defaults): {conf_matrix[1][0]}")
print(f"  True Positives (Correctly predicted default): {conf_matrix[1][1]}")

# Classification Report
print("\n" + "=" * 50)
print("CLASSIFICATION REPORT")
print("=" * 50)
print(classification_report(y_test, y_predictions))

# ROC-AUC Score
roc_auc_score_value = roc_auc_score(y_test, y_probability)
print(f"ROC-AUC Score: {roc_auc_score_value:.3f}")
print("(0.5 = random, 1.0 = perfect discrimination)")

# Kolmogorov-Smirnov Statistic
# Measures separation between default and non-default distributions
ks_statistic = ks_2samp(
    y_probability[y_test == 0],  # Non-defaulters
    y_probability[y_test == 1]   # Defaulters
)
print(f"\nKolmogorov-Smirnov Statistic: {ks_statistic.statistic:.3f}")
print("(Higher = better separation between groups)")

# =====================================================
# FEATURE IMPORTANCE - Model Coefficients
# =====================================================

print("\n" + "=" * 50)
print("FEATURE IMPORTANCE (Logistic Regression Coefficients)")
print("=" * 50)

# Extract and display coefficients
model_coefficients = pd.DataFrame({
    'Feature': feature_columns,
    'Coefficient': credit_model.named_steps['classifier'].coef_[0]
}).sort_values(by='Coefficient', ascending=False)

print(model_coefficients)
print("\nPositive coefficient = increases default risk")
print("Negative coefficient = decreases default risk\n")

# =====================================================
# CREDIT DECISION FRAMEWORK
# =====================================================

print("=" * 50)
print("CREDIT DECISION RULES")
print("=" * 50)

# Create results DataFrame with predictions
credit_decisions = X_test.copy().reset_index(drop=True)
credit_decisions['default_probability'] = y_probability

# Apply decision rules based on default probability
# PD >= 40%: High risk - Reject
# PD >= 25%: Medium risk - Manual Review
# PD < 25%: Low risk - Approve
credit_decisions['decision'] = np.where(
    credit_decisions['default_probability'] >= 0.40, 'Reject',
    np.where(credit_decisions['default_probability'] >= 0.25, 'Review', 'Approve')
)

print("\nSample Credit Decisions:")
print(credit_decisions[['income', 'debt_to_income', 'default_probability', 'decision']].head(10))

# Decision distribution
print("\nDecision Distribution:")
print(credit_decisions['decision'].value_counts())

# =====================================================
# VISUALIZATION - ROC Curve
# =====================================================

print("\nGenerating ROC Curve...")

# Calculate ROC curve
false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_probability)

# Plot ROC Curve
plt.figure(figsize=(10, 6))
plt.plot(
    false_positive_rate, 
    true_positive_rate, 
    color="#34f405",
    linewidth=2,
    label=f'Model ROC Curve (AUC = {roc_auc_score_value:.2f})'
)
plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curve - Credit Risk Model', fontsize=14, fontweight='bold')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =====================================================
# MODEL STABILITY - Population Stability Index (PSI)
# =====================================================

def calculate_population_stability_index(expected_probs, actual_probs, num_buckets=10):
    """
    Calculate PSI to measure distribution drift between training and test sets
    PSI < 0.1: No significant change
    PSI 0.1-0.25: Moderate change
    PSI > 0.25: Significant change (model may need retraining)
    """
    
    def create_bins(data, num_buckets):
        return np.percentile(data, np.linspace(0, 100, num_buckets + 1))
    
    # Get bin edges from expected distribution
    bin_edges = create_bins(expected_probs, num_buckets)
    
    # Calculate percentage in each bin
    expected_percentages = np.histogram(expected_probs, bins=bin_edges)[0] / len(expected_probs)
    actual_percentages = np.histogram(actual_probs, bins=bin_edges)[0] / len(actual_probs)
    
    # Avoid division by zero
    expected_percentages = np.where(expected_percentages == 0, 0.0001, expected_percentages)
    actual_percentages = np.where(actual_percentages == 0, 0.0001, actual_percentages)
    
    # Calculate PSI
    psi_value = np.sum(
        (actual_percentages - expected_percentages) * 
        np.log(actual_percentages / expected_percentages)
    )
    
    return psi_value

# Calculate PSI between train and test predictions
train_probabilities = credit_model.predict_proba(X_train)[:, 1]
test_probabilities = credit_model.predict_proba(X_test)[:, 1]

psi_score = calculate_population_stability_index(train_probabilities, test_probabilities)

print("\n" + "=" * 50)
print("MODEL STABILITY ANALYSIS")
print("=" * 50)
print(f"Population Stability Index (PSI): {psi_score:.3f}")

if psi_score < 0.1:
    print("Status: ✓ Model is stable - no significant distribution shift")
elif psi_score < 0.25:
    print("Status: ⚠ Moderate shift detected - monitor model performance")
else:
    print("Status: ✗ Significant shift detected - consider retraining model")

# =====================================================
# DISTRIBUTION DRIFT ANALYSIS
# =====================================================

print("\nGenerating distribution drift visualizations...")

# Plot distribution comparison for each feature
for feature in feature_columns:
    plt.figure(figsize=(10, 5))
    
    # Plot training distribution
    sns.kdeplot(
        X_train[feature], 
        label='Training Set', 
        fill=True, 
        alpha=0.5,
        color="#f51b0f"
    )
    
    # Plot testing distribution
    sns.kdeplot(
        X_test[feature], 
        label='Testing Set', 
        fill=True, 
        alpha=0.5,
        color='#ec4899'
    )
    
    plt.title(f'Distribution Comparison: {feature}', fontsize=14, fontweight='bold')
    plt.xlabel(feature, fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

print("\n" + "=" * 50)
print("ANALYSIS COMPLETE")
print("=" * 50)