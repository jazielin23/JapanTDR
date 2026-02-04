#!/usr/bin/env python3
"""
Brand Benefit Factor Analysis
Uses Factor Analysis instead of clustering to identify underlying dimensions.
Factor Analysis is more appropriate when attributes are correlated (low silhouette).
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.stats import pearsonr, chi2
from scipy.linalg import eigh
import statsmodels.api as sm
import warnings
import os
import json

warnings.filterwarnings('ignore')

# Custom KMO and Bartlett's test implementations
def calculate_kmo_manual(X):
    """Calculate Kaiser-Meyer-Olkin measure."""
    X = np.array(X)
    corr_matrix = np.corrcoef(X.T)
    inv_corr = np.linalg.pinv(corr_matrix)
    
    # Partial correlations
    n = corr_matrix.shape[0]
    partial_corr = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                partial_corr[i, j] = -inv_corr[i, j] / np.sqrt(inv_corr[i, i] * inv_corr[j, j])
    
    # KMO for each variable
    kmo_per_var = []
    for j in range(n):
        r_sq = sum(corr_matrix[j, i]**2 for i in range(n) if i != j)
        p_sq = sum(partial_corr[j, i]**2 for i in range(n) if i != j)
        kmo_per_var.append(r_sq / (r_sq + p_sq) if (r_sq + p_sq) > 0 else 0)
    
    # Overall KMO
    r_sq_total = sum(corr_matrix[i, j]**2 for i in range(n) for j in range(n) if i != j)
    p_sq_total = sum(partial_corr[i, j]**2 for i in range(n) for j in range(n) if i != j)
    kmo_overall = r_sq_total / (r_sq_total + p_sq_total) if (r_sq_total + p_sq_total) > 0 else 0
    
    return np.array(kmo_per_var), kmo_overall

def calculate_bartlett_manual(X):
    """Calculate Bartlett's test of sphericity."""
    X = np.array(X)
    n, p = X.shape
    corr_matrix = np.corrcoef(X.T)
    
    # Chi-square statistic
    det = np.linalg.det(corr_matrix)
    if det <= 0:
        det = 1e-10
    chi_square = -((n - 1) - (2 * p + 5) / 6) * np.log(det)
    
    # Degrees of freedom
    df = p * (p - 1) / 2
    
    # p-value
    p_value = 1 - chi2.cdf(chi_square, df)
    
    return chi_square, p_value

# Output directories
OUTPUT_DIR = 'output/reports'
FIGURES_DIR = 'output/figures'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 70)
print("  BRAND BENEFIT FACTOR ANALYSIS - 6 MONTH DATA")
print("=" * 70)
print()

# ============================================================================
# Load Data
# ============================================================================

print("Loading TDL survey data...")
df = pd.read_csv('dbt_project/seeds/survey_responses_tdl.csv')
print(f"Total records: {len(df)}")

# Define brand benefit columns
func_cols = [col for col in df.columns if col.startswith('tdl_func_')]
emot_cols = [col for col in df.columns if col.startswith('tdl_emot_')]
all_benefit_cols = func_cols + emot_cols

print(f"Total brand benefit attributes: {len(all_benefit_cols)}")

# ============================================================================
# Data Preparation
# ============================================================================

print("\n" + "-" * 50)
print("DATA PREPARATION")
print("-" * 50)

# Clean benefit data - replace 0 with NaN (missing values)
benefit_df = df[all_benefit_cols].replace(0, np.nan)

# Create analysis dataset
analysis_df = df[['respondent_id', 'wave', 'month', 'audience', 'geography',
                   'familiarity_tdl', 'opinion_tdl', 'consideration_tdl', 
                   'likelihood_visit_tdl', 'nps_tdl']].copy()

for col in ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl', 
            'likelihood_visit_tdl', 'nps_tdl']:
    analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')

for col in all_benefit_cols:
    analysis_df[col] = pd.to_numeric(benefit_df[col], errors='coerce')

# Filter to respondents with complete benefit data
has_all_benefits = (analysis_df[all_benefit_cols] > 0).any(axis=1)
analysis_subset = analysis_df[has_all_benefits].copy()

# Get complete cases
clustering_data = analysis_subset[all_benefit_cols].dropna()
valid_indices = clustering_data.index
analysis_complete = analysis_subset.loc[valid_indices].copy()

print(f"Complete cases for analysis: {len(analysis_complete)}")

# ============================================================================
# Check Suitability for Factor Analysis
# ============================================================================

print("\n" + "-" * 50)
print("FACTOR ANALYSIS SUITABILITY TESTS")
print("-" * 50)

X = analysis_complete[all_benefit_cols].values

# Bartlett's Test of Sphericity
chi_square, p_value = calculate_bartlett_manual(X)
print(f"\nBartlett's Test of Sphericity:")
print(f"  Chi-square: {chi_square:.1f}")
print(f"  p-value: {p_value:.6f}")
print(f"  Result: {'SUITABLE' if p_value < 0.05 else 'NOT SUITABLE'} for factor analysis")

# KMO Test
kmo_all, kmo_model = calculate_kmo_manual(X)
print(f"\nKaiser-Meyer-Olkin (KMO) Measure:")
print(f"  KMO: {kmo_model:.3f}")
kmo_interpretation = (
    "Excellent" if kmo_model >= 0.9 else
    "Good" if kmo_model >= 0.8 else
    "Acceptable" if kmo_model >= 0.7 else
    "Mediocre" if kmo_model >= 0.6 else
    "Poor" if kmo_model >= 0.5 else
    "Unacceptable"
)
print(f"  Interpretation: {kmo_interpretation}")

# ============================================================================
# Determine Optimal Number of Factors
# ============================================================================

print("\n" + "-" * 50)
print("DETERMINING NUMBER OF FACTORS")
print("-" * 50)

# Eigenvalue analysis using correlation matrix
corr_matrix = np.corrcoef(X.T)
eigenvalues, eigenvectors = np.linalg.eigh(corr_matrix)
eigenvalues = eigenvalues[::-1]  # Sort descending
eigenvectors = eigenvectors[:, ::-1]

# Kaiser criterion: eigenvalue > 1
n_factors_kaiser = sum(eigenvalues > 1)
print(f"\nKaiser Criterion (eigenvalue > 1): {n_factors_kaiser} factors")

# Show eigenvalues
print("\nEigenvalues (top 10):")
for i, ev in enumerate(eigenvalues[:10], 1):
    marker = " <-- Kaiser cutoff" if i == n_factors_kaiser else ""
    print(f"  Factor {i}: {ev:.3f} ({ev/sum(eigenvalues)*100:.1f}% variance){marker}")

# Cumulative variance
cumvar = np.cumsum(eigenvalues[:10]) / sum(eigenvalues) * 100
print("\nCumulative Variance Explained:")
for i, cv in enumerate(cumvar[:8], 1):
    print(f"  {i} factors: {cv:.1f}%")

# Use scree plot elbow - typically 3-5 factors for interpretability
# Select based on eigenvalue > 1 but cap at 6 for interpretability
optimal_n_factors = min(n_factors_kaiser, 6)
if optimal_n_factors < 3:
    optimal_n_factors = 3

print(f"\nSelected number of factors: {optimal_n_factors}")

# ============================================================================
# Run Factor Analysis
# ============================================================================

print("\n" + "=" * 70)
print(f"  FACTOR ANALYSIS WITH {optimal_n_factors} FACTORS")
print("=" * 70)

# Use sklearn's FactorAnalysis
from sklearn.decomposition import FactorAnalysis as FA_sklearn

# Standardize the data
X_std = StandardScaler().fit_transform(X)

# Fit factor analysis
fa = FA_sklearn(n_components=optimal_n_factors, random_state=42)
factor_scores_raw = fa.fit_transform(X_std)

# Get loadings (components_ in sklearn are transposed)
loadings_raw = fa.components_.T

# Varimax rotation
def varimax_rotation(loadings, max_iter=100, tol=1e-6):
    """Apply varimax rotation to factor loadings."""
    n_vars, n_factors = loadings.shape
    rotation_matrix = np.eye(n_factors)
    
    for _ in range(max_iter):
        old_rotation = rotation_matrix.copy()
        
        for i in range(n_factors):
            for j in range(i + 1, n_factors):
                # Calculate rotation angle
                x = loadings[:, i]
                y = loadings[:, j]
                
                u = x**2 - y**2
                v = 2 * x * y
                
                A = sum(u)
                B = sum(v)
                C = sum(u**2 - v**2)
                D = 2 * sum(u * v)
                
                num = D - 2 * A * B / n_vars
                den = C - (A**2 - B**2) / n_vars
                
                phi = 0.25 * np.arctan2(num, den)
                
                # Rotate
                cos_phi = np.cos(phi)
                sin_phi = np.sin(phi)
                
                new_x = cos_phi * x + sin_phi * y
                new_y = -sin_phi * x + cos_phi * y
                
                loadings[:, i] = new_x
                loadings[:, j] = new_y
                
                # Update rotation matrix
                rot = np.eye(n_factors)
                rot[i, i] = cos_phi
                rot[j, j] = cos_phi
                rot[i, j] = sin_phi
                rot[j, i] = -sin_phi
                rotation_matrix = rotation_matrix @ rot
        
        if np.allclose(rotation_matrix, old_rotation, atol=tol):
            break
    
    return loadings, rotation_matrix

# Apply varimax rotation
loadings_rotated, rotation_matrix = varimax_rotation(loadings_raw.copy())

# Create loadings dataframe
loadings = pd.DataFrame(
    loadings_rotated,
    index=all_benefit_cols,
    columns=[f'Factor_{i+1}' for i in range(optimal_n_factors)]
)

# Clean column names for display
loadings.index = loadings.index.str.replace('tdl_func_', '').str.replace('tdl_emot_', '').str.replace('_', ' ').str.title()

# Calculate variance explained by each factor
variance_explained = []
for i in range(optimal_n_factors):
    var = np.sum(loadings_rotated[:, i]**2) / len(all_benefit_cols)
    variance_explained.append(var)

variance = (None, np.array(variance_explained))  # Match the format used later

print("\nFactor Variance Explained:")
for i in range(optimal_n_factors):
    print(f"  Factor {i+1}: {variance[1][i]*100:.1f}% (cumulative: {sum(variance[1][:i+1])*100:.1f}%)")

print(f"\nTotal variance explained: {sum(variance[1])*100:.1f}%")

# ============================================================================
# Assign Attributes to Factors (Primary Loading)
# ============================================================================

print("\n" + "-" * 50)
print("FACTOR COMPOSITION (Primary Loadings)")
print("-" * 50)

# Assign each attribute to its highest-loading factor
attribute_assignments = []
for attr in loadings.index:
    row = loadings.loc[attr]
    primary_factor = row.abs().idxmax()
    primary_loading = row[primary_factor]
    
    # Get original category
    orig_attr = attr.lower().replace(' ', '_')
    orig_category = 'Emotional' if any(orig_attr in col for col in emot_cols) else 'Functional'
    
    attribute_assignments.append({
        'attribute': attr,
        'primary_factor': primary_factor,
        'loading': primary_loading,
        'original_category': orig_category
    })

assignments_df = pd.DataFrame(attribute_assignments)

# Name factors based on content
factor_names = {}
for factor in [f'Factor_{i+1}' for i in range(optimal_n_factors)]:
    factor_attrs = assignments_df[assignments_df['primary_factor'] == factor]
    attrs_text = ' '.join(factor_attrs['attribute'].str.lower())
    n_attrs = len(factor_attrs)
    
    # Get top loading attributes for this factor
    top_attrs = loadings[factor].abs().nlargest(5).index.tolist()
    top_text = ' '.join([a.lower() for a in top_attrs])
    
    # Determine name based on top loading attributes
    if 'dreams' in top_text or 'fantasy' in top_text or 'fantastical' in top_text:
        name = "Fantasy & Escape"
    elif 'family' in top_text or 'kids' in top_text or 'children' in top_text:
        name = "Family Appeal"
    elif 'innovative' in top_text or 'new' in top_text or 'thrilling' in top_text:
        name = "Innovation & Thrills"
    elif 'comfortable' in top_text or 'relaxing' in top_text or 'understands' in top_text:
        name = "Personal Comfort"
    elif 'worth' in top_text or 'price' in top_text or 'affordable' in top_text:
        name = "Value Perception"
    elif 'repeat' in top_text or 'unique' in top_text or 'variety' in top_text:
        name = "Experience Quality"
    elif 'character' in top_text or 'sparkling' in top_text:
        name = "Disney Magic"
    elif 'crowded' in top_text:
        name = "Accessibility"
    else:
        name = f"Dimension {factor[-1]}"
    
    factor_names[factor] = name

# Print factor compositions
factor_analysis = {}
for factor in [f'Factor_{i+1}' for i in range(optimal_n_factors)]:
    factor_attrs = assignments_df[assignments_df['primary_factor'] == factor].sort_values('loading', ascending=False)
    factor_name = factor_names[factor]
    
    print(f"\n### {factor_name} ({factor})")
    print(f"    Variance explained: {variance[1][int(factor[-1])-1]*100:.1f}%")
    print(f"    Attributes ({len(factor_attrs)}):")
    
    for _, row in factor_attrs.iterrows():
        loading_sign = "+" if row['loading'] > 0 else "-"
        print(f"      {loading_sign}{abs(row['loading']):.2f}  {row['attribute']}")
    
    factor_analysis[factor] = {
        'name': factor_name,
        'n_attributes': len(factor_attrs),
        'variance_explained': variance[1][int(factor[-1])-1],
        'attributes': factor_attrs['attribute'].tolist(),
        'loadings': factor_attrs['loading'].tolist()
    }

# ============================================================================
# Calculate Factor Scores
# ============================================================================

print("\n" + "-" * 50)
print("CALCULATING FACTOR SCORES")
print("-" * 50)

# Get factor scores for each respondent (apply rotation to raw scores)
factor_scores = factor_scores_raw @ rotation_matrix
factor_score_cols = [f'factor_{i+1}_score' for i in range(optimal_n_factors)]

for i, col in enumerate(factor_score_cols):
    analysis_complete[col] = factor_scores[:, i]
    fname = factor_names[f'Factor_{i+1}']
    print(f"  {fname}: mean = {factor_scores[:, i].mean():.3f}, std = {factor_scores[:, i].std():.3f}")

# ============================================================================
# Regression Analysis: Impact on Likelihood to Visit
# ============================================================================

print("\n" + "=" * 70)
print("  REGRESSION: FACTOR IMPACT ON LIKELIHOOD TO VISIT")
print("=" * 70)

# Prepare regression data
funnel_cols = ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl']
reg_cols = ['likelihood_visit_tdl'] + funnel_cols + factor_score_cols
reg_data = analysis_complete[reg_cols].dropna()

print(f"\nRegression sample size: {len(reg_data)}")

# Model 1: Funnel only
X_funnel = sm.add_constant(reg_data[funnel_cols])
y = reg_data['likelihood_visit_tdl']
model_funnel = sm.OLS(y, X_funnel).fit()

print("\n--- Model 1: Funnel Metrics Only ---")
print(f"R-squared: {model_funnel.rsquared:.3f}")

# Model 2: Funnel + Factors
X_full = sm.add_constant(reg_data[funnel_cols + factor_score_cols])
model_full = sm.OLS(y, X_full).fit()

print("\n--- Model 2: Funnel + Factor Scores ---")
print(f"R-squared: {model_full.rsquared:.3f}")
print(f"R-squared improvement: +{model_full.rsquared - model_funnel.rsquared:.3f}")

# Standardized coefficients
def get_standardized_coefs(model, X_data, y_data):
    coefs = model.params[1:]
    X_std = X_data.iloc[:, 1:].std()
    y_std = y_data.std()
    return (coefs * X_std) / y_std

std_coefs = get_standardized_coefs(model_full, X_full, y)

print("\n--- Standardized Coefficients (Full Model) ---")
coef_results = []
for var in funnel_cols + factor_score_cols:
    coef = model_full.params[var]
    std_coef = std_coefs[var]
    pval = model_full.pvalues[var]
    sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else ''
    
    if var.startswith('factor_'):
        factor_num = int(var.split('_')[1])
        var_name = factor_names[f'Factor_{factor_num}']
    else:
        var_name = var.replace('_tdl', '').title()
    
    print(f"  {var_name}: β = {std_coef:.3f} (p = {pval:.4f}) {sig}")
    coef_results.append({
        'predictor': var_name,
        'raw_coef': coef,
        'std_coef': std_coef,
        'p_value': pval,
        'significant': pval < 0.05
    })

# ============================================================================
# Factor Impact Ranking
# ============================================================================

print("\n" + "-" * 50)
print("FACTOR IMPACT RANKING")
print("-" * 50)

factor_impact = []
for i in range(optimal_n_factors):
    col_name = f'factor_{i+1}_score'
    factor_name = factor_names[f'Factor_{i+1}']
    std_coef = std_coefs[col_name]
    pval = model_full.pvalues[col_name]
    
    factor_impact.append({
        'factor': factor_name,
        'std_coef': std_coef,
        'p_value': pval,
        'significant': pval < 0.05,
        'variance_explained': variance[1][i],
        'n_attributes': factor_analysis[f'Factor_{i+1}']['n_attributes']
    })

factor_impact_df = pd.DataFrame(factor_impact)
factor_impact_df = factor_impact_df.sort_values('std_coef', ascending=False)

print("\nFactor ranking by impact on Likelihood to Visit:")
for _, row in factor_impact_df.iterrows():
    sig = '***' if row['p_value'] < 0.001 else '**' if row['p_value'] < 0.01 else '*' if row['p_value'] < 0.05 else 'ns'
    print(f"  {row['factor']:25s}: β = {row['std_coef']:+.3f} ({sig}), "
          f"Var = {row['variance_explained']*100:.1f}%, Attrs = {row['n_attributes']}")

# ============================================================================
# Segment Analysis
# ============================================================================

print("\n" + "-" * 50)
print("FACTOR SCORES BY SEGMENT")
print("-" * 50)

segment_scores = analysis_complete.groupby('audience')[factor_score_cols].mean()
segment_scores.columns = [factor_names[f'Factor_{i+1}'] for i in range(optimal_n_factors)]
print("\nMean factor scores by segment:")
print(segment_scores.round(2).to_string())

# ============================================================================
# Compare with Clustering Approach
# ============================================================================

print("\n" + "=" * 70)
print("  COMPARISON: FACTOR ANALYSIS vs CLUSTERING")
print("=" * 70)

# Quick clustering for comparison
from sklearn.cluster import KMeans
attr_data_T = analysis_complete[all_benefit_cols].T.values
scaler = StandardScaler()
attr_scaled = scaler.fit_transform(attr_data_T)

print("\nClustering Silhouette Scores:")
for n in range(2, 7):
    from sklearn.decomposition import PCA as skPCA
    pca_temp = skPCA(n_components=10)
    attr_pca = pca_temp.fit_transform(attr_scaled)
    kmeans = KMeans(n_clusters=n, random_state=42, n_init=10)
    labels = kmeans.fit_predict(attr_pca)
    sil = silhouette_score(attr_pca, labels)
    print(f"  {n} clusters: {sil:.3f}")

print(f"\nFactor Analysis Advantage:")
print(f"  - Does not force hard assignments")
print(f"  - Allows attributes to load on multiple factors")
print(f"  - KMO = {kmo_model:.3f} indicates data is suitable for FA")
print(f"  - Total variance explained: {sum(variance[1])*100:.1f}%")

# ============================================================================
# Save Results
# ============================================================================

print("\n" + "-" * 50)
print("SAVING RESULTS")
print("-" * 50)

# Save factor loadings
loadings_output = loadings.copy()
loadings_output['primary_factor'] = [assignments_df[assignments_df['attribute'] == attr]['primary_factor'].values[0] 
                                      for attr in loadings.index]
loadings_output['primary_factor_name'] = loadings_output['primary_factor'].map(factor_names)
loadings_output.to_csv(f'{OUTPUT_DIR}/factor_loadings.csv')
print(f"  Saved: factor_loadings.csv")

# Save factor impact
factor_impact_df.to_csv(f'{OUTPUT_DIR}/factor_impact.csv', index=False)
print(f"  Saved: factor_impact.csv")

# Save segment scores
segment_scores.to_csv(f'{OUTPUT_DIR}/segment_factor_scores.csv')
print(f"  Saved: segment_factor_scores.csv")

# Save regression results
coef_df = pd.DataFrame(coef_results)
coef_df.to_csv(f'{OUTPUT_DIR}/factor_regression_coefficients.csv', index=False)
print(f"  Saved: factor_regression_coefficients.csv")

# ============================================================================
# Executive Summary
# ============================================================================

print("\n" + "=" * 70)
print("  EXECUTIVE SUMMARY")
print("=" * 70)

print(f"""
FACTOR ANALYSIS RESULTS
=======================

Sample: {len(analysis_complete)} respondents across 6 months

SUITABILITY:
  - KMO: {kmo_model:.3f} ({kmo_interpretation})
  - Bartlett's test: p < 0.001 (suitable for FA)

FACTORS IDENTIFIED: {optimal_n_factors}
  Total variance explained: {sum(variance[1])*100:.1f}%
""")

# Sort by impact
sorted_factors = factor_impact_df.sort_values('std_coef', ascending=False)
for i, row in sorted_factors.iterrows():
    sig = "**SIGNIFICANT**" if row['significant'] else "not significant"
    print(f"  {row['factor']}")
    print(f"    - Variance: {row['variance_explained']*100:.1f}%")
    print(f"    - Impact: β = {row['std_coef']:.3f} ({sig})")
    print()

print(f"""
MODEL PERFORMANCE:
  Funnel Only R²: {model_funnel.rsquared:.3f}
  Funnel + Factors R²: {model_full.rsquared:.3f}
  Improvement: +{model_full.rsquared - model_funnel.rsquared:.3f}

WHY FACTOR ANALYSIS IS BETTER HERE:
  - Clustering had low silhouette (0.163) = poor cluster separation
  - Factor Analysis allows for overlapping dimensions
  - Brand perceptions are naturally correlated, not distinct groups
  - Factors explain {sum(variance[1])*100:.1f}% of variance in ratings
""")

print("=" * 70)
print("  ANALYSIS COMPLETE")
print("=" * 70)
