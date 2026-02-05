#!/usr/bin/env python3
"""
SEM with Penalized Logistic Regression - Top Box Analysis
=========================================================

This script implements an SEM-like path model using penalized logistic regression
with TOP BOX coding: Likert scale = 5 -> 1, otherwise -> 0

Uses Factor Analysis for brand benefits (per brand-benefit-clusters approach).

Author: Data Analysis Team
Date: 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FactorAnalysis
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
import statsmodels.api as sm
from scipy import stats

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "Final Data for 6 waves.csv"
OUTPUT_DIR = PROJECT_ROOT / "output" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("  SEM WITH PENALIZED LOGISTIC REGRESSION - TOP BOX ANALYSIS")
print("=" * 70)
print()

# =============================================================================
# Load Data
# =============================================================================

print("Loading 6-wave real data...")
df = pd.read_csv(DATA_FILE)
print(f"Raw data: {len(df)} rows, {len(df.columns)} columns")

# Clean column names - handle multi-line headers
df.columns = df.columns.str.replace('\n', ' ').str.strip()

# =============================================================================
# Identify Key Columns
# =============================================================================

# Find funnel columns for TDL
funnel_cols_raw = {
    'familiarity': [c for c in df.columns if 'Familiarity' in c and 'TDL' in c][0] if any('Familiarity' in c and 'TDL' in c for c in df.columns) else None,
    'opinion': [c for c in df.columns if 'Opinion' in c and 'TDL' in c][0] if any('Opinion' in c and 'TDL' in c for c in df.columns) else None,
    'consideration': [c for c in df.columns if 'Consideration' in c and 'TDL' in c][0] if any('Consideration' in c and 'TDL' in c for c in df.columns) else None,
    'likelihood': [c for c in df.columns if 'Likelihood' in c and 'TDL' in c][0] if any('Likelihood' in c and 'TDL' in c for c in df.columns) else None,
}

print("\nFunnel columns found:")
for key, col in funnel_cols_raw.items():
    if col:
        print(f"  {key}: {col[:60]}...")

# Find TDL Functional benefit columns (ending with "- F")
func_cols = [c for c in df.columns if '- TDL' in c and c.endswith('- F')]
print(f"\nFunctional benefit columns (TDL): {len(func_cols)}")

# Find TDL Emotional benefit columns (ending with "- E")
emot_cols = [c for c in df.columns if '- TDL' in c and c.endswith('- E')]
print(f"Emotional benefit columns (TDL): {len(emot_cols)}")

# Audience/Segment column
audience_col = 'Audience'

# Wave column
wave_col = 'Wave'

# =============================================================================
# Create Clean Working Dataset
# =============================================================================

print("\n" + "-" * 50)
print("CREATING CLEAN DATASET WITH TOP-BOX CODING")
print("-" * 50)

# Create analysis dataframe
analysis_df = df[[wave_col, audience_col]].copy()
analysis_df.columns = ['wave', 'segment']

# Add funnel variables (raw)
for name, col in funnel_cols_raw.items():
    if col:
        analysis_df[f'{name}_raw'] = pd.to_numeric(df[col], errors='coerce')

# Add benefit variables (raw)
for i, col in enumerate(func_cols):
    clean_name = col.replace(' - TDL (5=high; 1=low) - F', '').strip()
    clean_name = clean_name.replace(' ', '_').lower()[:30]
    analysis_df[f'func_{i:02d}_{clean_name}'] = pd.to_numeric(df[col], errors='coerce')

for i, col in enumerate(emot_cols):
    clean_name = col.replace(' - TDL (5=high; 1=low) - E', '').strip()
    clean_name = clean_name.replace(' ', '_').lower()[:30]
    analysis_df[f'emot_{i:02d}_{clean_name}'] = pd.to_numeric(df[col], errors='coerce')

# Get clean column names
func_clean_cols = [c for c in analysis_df.columns if c.startswith('func_')]
emot_clean_cols = [c for c in analysis_df.columns if c.startswith('emot_')]
all_benefit_cols = func_clean_cols + emot_clean_cols

print(f"Functional columns: {len(func_clean_cols)}")
print(f"Emotional columns: {len(emot_clean_cols)}")

# =============================================================================
# APPLY TOP-BOX CODING
# =============================================================================

print("\n" + "-" * 50)
print("TOP-BOX CODING: Value = 5 -> 1, else -> 0")
print("-" * 50)

# Top-box coding for funnel variables
funnel_vars = ['familiarity', 'opinion', 'consideration', 'likelihood']
for var in funnel_vars:
    raw_col = f'{var}_raw'
    if raw_col in analysis_df.columns:
        # Clean invalid values first (keep only 1-5)
        raw_vals = analysis_df[raw_col].copy()
        raw_vals[(raw_vals < 1) | (raw_vals > 5)] = np.nan
        
        # Top-box: 5 = 1, else = 0
        analysis_df[f'{var}_tb'] = (raw_vals == 5).astype(float)
        analysis_df.loc[raw_vals.isna(), f'{var}_tb'] = np.nan
        
        # Report stats
        valid = analysis_df[f'{var}_tb'].notna()
        top_box_pct = analysis_df.loc[valid, f'{var}_tb'].mean() * 100
        print(f"{var}: {top_box_pct:.1f}% top-box (n={valid.sum()})")

# Top-box coding for benefit variables
for col in all_benefit_cols:
    raw_vals = analysis_df[col].copy()
    # Clean invalid values (keep only 1-5)
    raw_vals[(raw_vals < 1) | (raw_vals > 5)] = np.nan
    # Top-box
    analysis_df[f'{col}_tb'] = (raw_vals == 5).astype(float)
    analysis_df.loc[raw_vals.isna(), f'{col}_tb'] = np.nan

# Get top-box column names
func_tb_cols = [f'{c}_tb' for c in func_clean_cols]
emot_tb_cols = [f'{c}_tb' for c in emot_clean_cols]
all_benefit_tb_cols = func_tb_cols + emot_tb_cols

# =============================================================================
# FILTER TO COMPLETE CASES
# =============================================================================

print("\n" + "-" * 50)
print("FILTERING TO COMPLETE CASES")
print("-" * 50)

# Required funnel columns
required_funnel = [f'{v}_tb' for v in funnel_vars]

# For benefit analysis, we need at least some benefit data
has_benefits = analysis_df[all_benefit_tb_cols].notna().any(axis=1)
has_funnel = analysis_df[required_funnel].notna().all(axis=1)

# Dataset 1: Full funnel analysis (larger sample)
funnel_complete = analysis_df[has_funnel].copy()
print(f"Funnel analysis sample: n = {len(funnel_complete)}")

# Dataset 2: Funnel + Benefits (smaller sample)
benefits_complete = analysis_df[has_funnel & has_benefits].copy()
benefits_complete = benefits_complete.dropna(subset=all_benefit_tb_cols)
print(f"Full model sample (with benefits): n = {len(benefits_complete)}")

# =============================================================================
# FACTOR ANALYSIS ON TOP-BOX BENEFIT DATA
# =============================================================================

print("\n" + "=" * 70)
print("  FACTOR ANALYSIS ON TOP-BOX BRAND BENEFITS")
print("=" * 70)

if len(benefits_complete) > 50:
    # Get benefit data (top-box coded)
    X_benefits = benefits_complete[all_benefit_tb_cols].values
    
    # Standardize
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X_benefits)
    
    # Factor Analysis with 4 factors (per brand-benefit-clusters approach)
    n_factors = 4
    fa = FactorAnalysis(n_components=n_factors, random_state=42)
    factor_scores = fa.fit_transform(X_std)
    
    # Get loadings
    loadings = fa.components_.T
    
    # Analyze factors
    factor_names = {
        0: "Core_Experience",  # Primary positive experience
        1: "Value_Accessibility",  # Affordability, crowding
        2: "Thrills_Innovation",  # Active, adventurous, new
        3: "Family_Kids"  # Family-specific attributes
    }
    
    print("\nFactor Structure (Top-Box):")
    for i in range(n_factors):
        sorted_idx = np.argsort(np.abs(loadings[:, i]))[::-1]
        top_attrs = []
        for idx in sorted_idx[:5]:
            col_name = all_benefit_tb_cols[idx].replace('_tb', '').replace('func_', 'F:').replace('emot_', 'E:')
            top_attrs.append((col_name[:40], loadings[idx, i]))
        
        print(f"\n  Factor {i+1}: {factor_names[i]}")
        for attr, loading in top_attrs:
            print(f"    {loading:+.3f}  {attr}")
    
    # Add factor scores to dataset
    for i in range(n_factors):
        benefits_complete[f'factor_{factor_names[i]}'] = factor_scores[:, i]
    
    factor_cols = [f'factor_{factor_names[i]}' for i in range(n_factors)]
else:
    print("Insufficient sample for factor analysis")
    factor_cols = []

# =============================================================================
# PENALIZED LOGISTIC REGRESSION: FUNNEL PATH MODEL
# =============================================================================

print("\n" + "=" * 70)
print("  PENALIZED LOGISTIC REGRESSION: MARKETING FUNNEL PATHS")
print("=" * 70)

results = []

def fit_penalized_logistic(X, y, name, penalty='l1'):
    """Fit penalized logistic regression with cross-validation."""
    # Remove missing values
    valid_idx = ~(X.isna().any(axis=1) | y.isna())
    X_clean = X[valid_idx].values
    y_clean = y[valid_idx].values
    
    if len(np.unique(y_clean)) < 2:
        print(f"  {name}: Skipped - only one class present")
        return None
    
    # Fit L1 (LASSO) penalized logistic regression with CV
    model = LogisticRegressionCV(
        cv=5,
        penalty=penalty,
        solver='saga',
        max_iter=2000,
        random_state=42,
        Cs=10  # 10 values of regularization to try
    )
    model.fit(X_clean, y_clean)
    
    # Calculate AUC
    y_prob = model.predict_proba(X_clean)[:, 1]
    auc = roc_auc_score(y_clean, y_prob)
    
    # Cross-validated AUC
    cv_scores = cross_val_score(model, X_clean, y_clean, cv=5, scoring='roc_auc')
    
    return {
        'model': model,
        'auc': auc,
        'cv_auc_mean': cv_scores.mean(),
        'cv_auc_std': cv_scores.std(),
        'n': len(y_clean),
        'n_positive': y_clean.sum(),
        'C': model.C_[0],  # Selected regularization
        'coefs': dict(zip(X.columns, model.coef_[0]))
    }

# Path 1: Familiarity -> Opinion (top-box)
print("\n--- Path 1: Familiarity_TB -> Opinion_TB ---")
X = funnel_complete[['familiarity_tb']]
y = funnel_complete['opinion_tb']
result1 = fit_penalized_logistic(X, y, "Fam -> Opinion")
if result1:
    print(f"  AUC: {result1['auc']:.3f} (CV: {result1['cv_auc_mean']:.3f} +/- {result1['cv_auc_std']:.3f})")
    print(f"  Regularization C: {result1['C']:.4f}")
    print(f"  Coefficients: {result1['coefs']}")
    results.append({'path': 'Familiarity -> Opinion', **result1})

# Path 2: Familiarity + Opinion -> Consideration (top-box)
print("\n--- Path 2: Familiarity_TB + Opinion_TB -> Consideration_TB ---")
X = funnel_complete[['familiarity_tb', 'opinion_tb']]
y = funnel_complete['consideration_tb']
result2 = fit_penalized_logistic(X, y, "Fam+Op -> Consider")
if result2:
    print(f"  AUC: {result2['auc']:.3f} (CV: {result2['cv_auc_mean']:.3f} +/- {result2['cv_auc_std']:.3f})")
    print(f"  Regularization C: {result2['C']:.4f}")
    print(f"  Coefficients: {result2['coefs']}")
    results.append({'path': 'Fam+Opinion -> Consider', **result2})

# Path 3: Funnel -> Likelihood (top-box)
print("\n--- Path 3: Full Funnel -> Likelihood_TB ---")
X = funnel_complete[['familiarity_tb', 'opinion_tb', 'consideration_tb']]
y = funnel_complete['likelihood_tb']
result3 = fit_penalized_logistic(X, y, "Funnel -> Likelihood")
if result3:
    print(f"  AUC: {result3['auc']:.3f} (CV: {result3['cv_auc_mean']:.3f} +/- {result3['cv_auc_std']:.3f})")
    print(f"  Regularization C: {result3['C']:.4f}")
    print(f"  Coefficients:")
    for var, coef in sorted(result3['coefs'].items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"    {var}: {coef:+.3f}")
    results.append({'path': 'Full Funnel -> Likelihood', **result3})

# =============================================================================
# FULL MODEL: FUNNEL + BENEFIT FACTORS -> LIKELIHOOD
# =============================================================================

print("\n" + "=" * 70)
print("  FULL MODEL: FUNNEL + BENEFIT FACTORS -> LIKELIHOOD")
print("=" * 70)

if len(benefits_complete) > 50 and factor_cols:
    # Funnel-only model (on benefits sample for fair comparison)
    print("\n--- Funnel-Only Model (on benefits subsample) ---")
    X_funnel = benefits_complete[['familiarity_tb', 'opinion_tb', 'consideration_tb']]
    y = benefits_complete['likelihood_tb']
    result_funnel = fit_penalized_logistic(X_funnel, y, "Funnel Only")
    if result_funnel:
        print(f"  AUC: {result_funnel['auc']:.3f} (CV: {result_funnel['cv_auc_mean']:.3f})")
    
    # Full model with factors
    print("\n--- Full Model: Funnel + Benefit Factors ---")
    X_full = benefits_complete[['familiarity_tb', 'opinion_tb', 'consideration_tb'] + factor_cols]
    result_full = fit_penalized_logistic(X_full, y, "Full Model")
    if result_full:
        print(f"  AUC: {result_full['auc']:.3f} (CV: {result_full['cv_auc_mean']:.3f} +/- {result_full['cv_auc_std']:.3f})")
        print(f"  Regularization C: {result_full['C']:.4f}")
        print(f"  Coefficients (sorted by abs value):")
        for var, coef in sorted(result_full['coefs'].items(), key=lambda x: abs(x[1]), reverse=True):
            sig = "*" if abs(coef) > 0.1 else ""
            print(f"    {var:35s}: {coef:+.4f} {sig}")
        
        results.append({'path': 'Funnel + Factors -> Likelihood', **result_full})
    
    # Model comparison
    if result_funnel and result_full:
        print("\n--- Model Comparison ---")
        print(f"  Funnel-Only AUC:  {result_funnel['auc']:.3f}")
        print(f"  Full Model AUC:   {result_full['auc']:.3f}")
        print(f"  AUC Improvement:  {result_full['auc'] - result_funnel['auc']:+.3f}")

# =============================================================================
# COMPARISON: L1 (LASSO) vs L2 (Ridge) PENALTY
# =============================================================================

print("\n" + "=" * 70)
print("  PENALTY COMPARISON: L1 (LASSO) vs L2 (Ridge)")
print("=" * 70)

X = funnel_complete[['familiarity_tb', 'opinion_tb', 'consideration_tb']]
y = funnel_complete['likelihood_tb']

# L1 (LASSO)
result_l1 = fit_penalized_logistic(X, y, "L1", penalty='l1')
print(f"\nL1 (LASSO) Penalized:")
print(f"  AUC: {result_l1['auc']:.3f}")
for var, coef in result_l1['coefs'].items():
    print(f"    {var}: {coef:+.4f}")

# L2 (Ridge)
result_l2 = fit_penalized_logistic(X, y, "L2", penalty='l2')
print(f"\nL2 (Ridge) Penalized:")
print(f"  AUC: {result_l2['auc']:.3f}")
for var, coef in result_l2['coefs'].items():
    print(f"    {var}: {coef:+.4f}")

# ElasticNet (needs l1_ratio parameter)
try:
    model_en = LogisticRegressionCV(
        cv=5, penalty='elasticnet', solver='saga', 
        max_iter=2000, random_state=42, Cs=10, l1_ratios=[0.5]
    )
    valid_idx = ~(X.isna().any(axis=1) | y.isna())
    X_clean = X[valid_idx].values
    y_clean = y[valid_idx].values
    model_en.fit(X_clean, y_clean)
    y_prob = model_en.predict_proba(X_clean)[:, 1]
    auc_en = roc_auc_score(y_clean, y_prob)
    
    print(f"\nElasticNet Penalized (L1 ratio=0.5):")
    print(f"  AUC: {auc_en:.3f}")
    for var, coef in zip(X.columns, model_en.coef_[0]):
        print(f"    {var}: {coef:+.4f}")
except Exception as e:
    print(f"\nElasticNet: Error - {e}")

# =============================================================================
# SEGMENT ANALYSIS
# =============================================================================

print("\n" + "=" * 70)
print("  SEGMENT ANALYSIS")
print("=" * 70)

segment_results = []
for segment in funnel_complete['segment'].unique():
    seg_data = funnel_complete[funnel_complete['segment'] == segment]
    if len(seg_data) < 50:
        continue
    
    X = seg_data[['familiarity_tb', 'opinion_tb', 'consideration_tb']]
    y = seg_data['likelihood_tb']
    
    try:
        result = fit_penalized_logistic(X, y, f"Segment {segment}")
        if result:
            segment_results.append({
                'segment': segment,
                'n': result['n'],
                'n_positive': result['n_positive'],
                'positive_rate': result['n_positive'] / result['n'],
                'auc': result['auc'],
                'cv_auc': result['cv_auc_mean'],
                **{f'coef_{k}': v for k, v in result['coefs'].items()}
            })
    except Exception as e:
        print(f"  {segment}: Error - {e}")

if segment_results:
    seg_df = pd.DataFrame(segment_results)
    print("\nSegment Results:")
    print(seg_df[['segment', 'n', 'positive_rate', 'auc', 'cv_auc']].to_string(index=False))

# =============================================================================
# ODDS RATIOS FOR INTERPRETATION
# =============================================================================

print("\n" + "=" * 70)
print("  ODDS RATIOS (Funnel -> Likelihood)")
print("=" * 70)

if result3:
    print("\nOdds Ratios (exp(coefficient)):")
    print(f"{'Variable':<25} {'Coef':>10} {'Odds Ratio':>12} {'Interpretation'}")
    print("-" * 70)
    for var, coef in result3['coefs'].items():
        odds_ratio = np.exp(coef)
        interp = "Increases likelihood" if coef > 0 else "Decreases likelihood"
        print(f"{var:<25} {coef:>+10.3f} {odds_ratio:>12.3f} {interp}")

# =============================================================================
# SAVE RESULTS
# =============================================================================

print("\n" + "=" * 70)
print("  SAVING RESULTS")
print("=" * 70)

# Summary results
summary_data = []
for r in results:
    if 'coefs' in r:
        row = {
            'path': r['path'],
            'n': r['n'],
            'auc': r['auc'],
            'cv_auc_mean': r['cv_auc_mean'],
            'cv_auc_std': r['cv_auc_std'],
            'regularization_C': r['C']
        }
        for k, v in r['coefs'].items():
            row[f'coef_{k}'] = v
        summary_data.append(row)

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(OUTPUT_DIR / 'sem_penalized_logistic_topbox.csv', index=False)
print(f"  Saved: sem_penalized_logistic_topbox.csv")

# Segment results
if segment_results:
    seg_df.to_csv(OUTPUT_DIR / 'sem_penalized_logistic_segments.csv', index=False)
    print(f"  Saved: sem_penalized_logistic_segments.csv")

# Top-box descriptives
topbox_stats = []
for var in funnel_vars:
    col = f'{var}_tb'
    if col in funnel_complete.columns:
        topbox_stats.append({
            'variable': var,
            'n': funnel_complete[col].notna().sum(),
            'top_box_pct': funnel_complete[col].mean() * 100,
            'top_box_n': funnel_complete[col].sum()
        })

topbox_df = pd.DataFrame(topbox_stats)
topbox_df.to_csv(OUTPUT_DIR / 'topbox_descriptives.csv', index=False)
print(f"  Saved: topbox_descriptives.csv")

# =============================================================================
# SUMMARY FOR README
# =============================================================================

print("\n" + "=" * 70)
print("  SUMMARY")
print("=" * 70)

print(f"""
## Penalized Logistic Regression SEM - Top Box Analysis

### Methodology
- **Top-Box Coding**: All Likert scale variables coded as 1 if value=5, 0 otherwise
- **Regularization**: L1 (LASSO) penalized logistic regression with 5-fold CV
- **Sample**: n = {len(funnel_complete)} (funnel analysis), n = {len(benefits_complete)} (with benefits)

### Top-Box Rates (% scoring 5)
""")

for stat in topbox_stats:
    print(f"- {stat['variable'].title()}: {stat['top_box_pct']:.1f}%")

print(f"""
### Key Findings

#### Funnel Path Coefficients (L1 Penalized)
""")

if result3:
    print("| Variable | Coefficient | Odds Ratio |")
    print("|----------|-------------|------------|")
    for var, coef in sorted(result3['coefs'].items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"| {var} | {coef:+.3f} | {np.exp(coef):.3f} |")

print(f"""
#### Model Performance
- Funnel -> Likelihood AUC: {result3['auc']:.3f} (CV: {result3['cv_auc_mean']:.3f})
""")

if result_full:
    print(f"- Full Model AUC: {result_full['auc']:.3f} (CV: {result_full['cv_auc_mean']:.3f})")

print("\n" + "=" * 70)
print("  ANALYSIS COMPLETE")
print("=" * 70)
