#!/usr/bin/env python3
"""
Full SEM Model: Marketing Funnel + Brand Benefit Factors
Combines funnel path analysis with factor-based brand benefits
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FactorAnalysis
import statsmodels.api as sm
from scipy.stats import pearsonr
import warnings
import os

warnings.filterwarnings('ignore')

OUTPUT_DIR = 'output/reports'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("  FULL SEM MODEL: MARKETING FUNNEL + BRAND BENEFIT FACTORS")
print("=" * 70)
print()

# ============================================================================
# Load and Prepare Data
# ============================================================================

print("Loading data...")
df = pd.read_csv('dbt_project/seeds/survey_responses_tdl.csv')

# Get benefit columns
func_cols = [col for col in df.columns if col.startswith('tdl_func_')]
emot_cols = [col for col in df.columns if col.startswith('tdl_emot_')]
all_benefit_cols = func_cols + emot_cols

# Prepare analysis dataframe
benefit_df = df[all_benefit_cols].replace(0, np.nan)
analysis_df = df[['respondent_id', 'month', 'audience', 
                   'familiarity_tdl', 'opinion_tdl', 'consideration_tdl', 
                   'likelihood_visit_tdl']].copy()

for col in ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl', 'likelihood_visit_tdl']:
    analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')

for col in all_benefit_cols:
    analysis_df[col] = pd.to_numeric(benefit_df[col], errors='coerce')

# Filter to complete cases with benefit data
has_benefits = (analysis_df[all_benefit_cols] > 0).any(axis=1)
analysis_complete = analysis_df[has_benefits].copy()
analysis_complete = analysis_complete.dropna(subset=['familiarity_tdl', 'opinion_tdl', 
                                                       'consideration_tdl', 'likelihood_visit_tdl'] + all_benefit_cols)

print(f"Sample size: n = {len(analysis_complete)}")
print(f"Months: {analysis_complete['month'].nunique()} ({', '.join(analysis_complete['month'].unique())})")

# ============================================================================
# Factor Analysis on Brand Benefits
# ============================================================================

print("\n" + "-" * 50)
print("FACTOR ANALYSIS: BRAND BENEFITS")
print("-" * 50)

X_benefits = analysis_complete[all_benefit_cols].values
X_std = StandardScaler().fit_transform(X_benefits)

# 4 factors based on Kaiser criterion
fa = FactorAnalysis(n_components=4, random_state=42)
factor_scores_raw = fa.fit_transform(X_std)

# Get loadings
loadings = fa.components_.T

# Determine factor names by examining top loading attributes
factor_names = {}
used_names = set()

for i in range(4):
    top_idx = np.argsort(np.abs(loadings[:, i]))[-5:][::-1]
    top_attrs = [all_benefit_cols[j].replace('tdl_func_', '').replace('tdl_emot_', '') for j in top_idx]
    
    # Name based on content
    attrs_text = ' '.join(top_attrs)
    if 'dreams' in attrs_text or 'fantastical' in attrs_text or 'sparkling' in attrs_text:
        name = "Disney Magic"
    elif 'affordable' in attrs_text and 'crowded' in attrs_text:
        name = "Value & Access"
    elif 'affordable' in attrs_text:
        name = "Affordability"
    elif 'crowded' in attrs_text:
        name = "Crowd Concerns"
    elif 'innovative' in attrs_text or 'adventurous' in attrs_text or 'thrilling' in attrs_text:
        name = "Innovation & Thrills"
    elif ('kids' in attrs_text or 'children' in attrs_text) and 'family' in attrs_text:
        name = "Family & Kids"
    elif 'kids' in attrs_text or 'children' in attrs_text:
        name = "Kids Experience"
    elif 'family' in attrs_text or 'bond' in attrs_text:
        name = "Family Bonding"
    elif 'feel_good' in attrs_text or 'memories' in attrs_text or 'enjoy' in attrs_text:
        name = "Core Experience"
    elif 'comfortable' in attrs_text or 'relaxing' in attrs_text:
        name = "Comfort & Relaxation"
    else:
        name = f"Benefit Dimension {i+1}"
    
    # Ensure unique names
    original_name = name
    counter = 2
    while name in used_names:
        name = f"{original_name} {counter}"
        counter += 1
    used_names.add(name)
    
    factor_names[i] = name
    print(f"\nFactor {i+1}: {name}")
    print(f"  Top attributes: {', '.join(top_attrs[:3])}")

# Flip factor scores so higher = more of that attribute (for interpretability)
# Check if majority of loadings are negative
for i in range(4):
    if np.mean(loadings[:, i]) < 0:
        factor_scores_raw[:, i] *= -1
        loadings[:, i] *= -1

# Add factor scores to dataframe
for i in range(4):
    analysis_complete[f'F{i+1}_{factor_names[i].replace(" & ", "_").replace(" ", "_")}'] = factor_scores_raw[:, i]

factor_cols = [col for col in analysis_complete.columns if col.startswith('F')]
print(f"\nFactor columns: {factor_cols}")

# ============================================================================
# PART 1: MARKETING FUNNEL PATH MODEL
# ============================================================================

print("\n" + "=" * 70)
print("  PART 1: MARKETING FUNNEL PATH MODEL")
print("=" * 70)

def standardized_coef(model, X_data, y_data, var_name):
    """Calculate standardized coefficient."""
    return model.params[var_name] * X_data[var_name].std() / y_data.std()

results = []

# Path: Familiarity -> Opinion
X = sm.add_constant(analysis_complete[['familiarity_tdl']])
y = analysis_complete['opinion_tdl']
m = sm.OLS(y, X).fit()
beta = standardized_coef(m, analysis_complete, y, 'familiarity_tdl')
results.append({
    'path': 'Familiarity → Opinion',
    'beta': beta,
    'p_value': m.pvalues['familiarity_tdl'],
    'r_squared': m.rsquared
})
print(f"\nFamiliarity → Opinion")
print(f"  β = {beta:.3f}, p = {m.pvalues['familiarity_tdl']:.4f}, R² = {m.rsquared:.3f}")

# Path: Familiarity + Opinion -> Consideration
X = sm.add_constant(analysis_complete[['familiarity_tdl', 'opinion_tdl']])
y = analysis_complete['consideration_tdl']
m = sm.OLS(y, X).fit()
beta_fam = standardized_coef(m, analysis_complete, y, 'familiarity_tdl')
beta_op = standardized_coef(m, analysis_complete, y, 'opinion_tdl')
results.append({'path': 'Familiarity → Consideration', 'beta': beta_fam, 'p_value': m.pvalues['familiarity_tdl'], 'r_squared': m.rsquared})
results.append({'path': 'Opinion → Consideration', 'beta': beta_op, 'p_value': m.pvalues['opinion_tdl'], 'r_squared': m.rsquared})
print(f"\nFamiliarity → Consideration")
print(f"  β = {beta_fam:.3f}, p = {m.pvalues['familiarity_tdl']:.4f}")
print(f"\nOpinion → Consideration")
print(f"  β = {beta_op:.3f}, p = {m.pvalues['opinion_tdl']:.4f}")
print(f"  Model R² = {m.rsquared:.3f}")

# Path: Funnel -> Likelihood (without benefits)
X = sm.add_constant(analysis_complete[['familiarity_tdl', 'opinion_tdl', 'consideration_tdl']])
y = analysis_complete['likelihood_visit_tdl']
m_funnel = sm.OLS(y, X).fit()

print(f"\nFunnel → Likelihood (without benefit factors)")
for var in ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl']:
    beta = standardized_coef(m_funnel, analysis_complete, y, var)
    sig = '***' if m_funnel.pvalues[var] < 0.001 else '**' if m_funnel.pvalues[var] < 0.01 else '*' if m_funnel.pvalues[var] < 0.05 else ''
    name = var.replace('_tdl', '').title()
    print(f"  {name} → Likelihood: β = {beta:.3f}, p = {m_funnel.pvalues[var]:.4f} {sig}")

print(f"  Funnel-Only Model R² = {m_funnel.rsquared:.3f}")

# ============================================================================
# PART 2: FULL MODEL - FUNNEL + BENEFIT FACTORS
# ============================================================================

print("\n" + "=" * 70)
print("  PART 2: FULL MODEL - FUNNEL + BENEFIT FACTORS")
print("=" * 70)

# Full model with funnel + factors
all_predictors = ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl'] + factor_cols
X = sm.add_constant(analysis_complete[all_predictors])
y = analysis_complete['likelihood_visit_tdl']
m_full = sm.OLS(y, X).fit()

print(f"\nFull Model: Funnel + Benefit Factors")
print(f"{'='*60}")
print(f"{'Predictor':<30} {'β':>8} {'p-value':>12} {'Sig':>6}")
print(f"{'-'*60}")

full_results = []
for var in all_predictors:
    beta = standardized_coef(m_full, analysis_complete, y, var)
    pval = m_full.pvalues[var]
    sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else ''
    
    if var.endswith('_tdl'):
        name = var.replace('_tdl', '').title()
    else:
        name = var.split('_', 1)[1].replace('_', ' ')
    
    print(f"{name:<30} {beta:>8.3f} {pval:>12.4f} {sig:>6}")
    
    full_results.append({
        'predictor': name,
        'beta': beta,
        'raw_coef': m_full.params[var],
        'std_error': m_full.bse[var],
        'p_value': pval,
        'significant': pval < 0.05
    })

print(f"{'-'*60}")
print(f"{'Model R²':<30} {m_full.rsquared:>8.3f}")
print(f"{'Adjusted R²':<30} {m_full.rsquared_adj:>8.3f}")
print(f"{'R² Improvement (vs Funnel)':<30} {m_full.rsquared - m_funnel.rsquared:>8.3f}")
print(f"{'F-statistic':<30} {m_full.fvalue:>8.1f}")
print(f"{'Prob (F-statistic)':<30} {m_full.f_pvalue:>12.2e}")

# ============================================================================
# PART 3: MODEL COMPARISON
# ============================================================================

print("\n" + "=" * 70)
print("  PART 3: MODEL COMPARISON")
print("=" * 70)

print(f"""
Model Comparison:
{'-'*50}
                              Funnel Only    Full Model
{'-'*50}
R-squared                        {m_funnel.rsquared:.3f}          {m_full.rsquared:.3f}
Adjusted R-squared               {m_funnel.rsquared_adj:.3f}          {m_full.rsquared_adj:.3f}
AIC                           {m_funnel.aic:.1f}       {m_full.aic:.1f}
BIC                           {m_funnel.bic:.1f}       {m_full.bic:.1f}
{'-'*50}
Improvement in R²                              +{m_full.rsquared - m_funnel.rsquared:.3f}
""")

# F-test for nested models
from scipy import stats
df1 = len(factor_cols)  # additional parameters
df2 = len(analysis_complete) - len(all_predictors) - 1  # residual df
ss_reduced = m_funnel.ssr
ss_full = m_full.ssr
f_stat = ((ss_reduced - ss_full) / df1) / (ss_full / df2)
f_pval = 1 - stats.f.cdf(f_stat, df1, df2)

print(f"F-test for adding benefit factors:")
print(f"  F({df1}, {df2}) = {f_stat:.2f}, p = {f_pval:.4f}")
print(f"  Result: Benefit factors {'significantly' if f_pval < 0.05 else 'do not significantly'} improve model fit")

# ============================================================================
# PART 4: SEGMENT ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("  PART 4: SEGMENT ANALYSIS")
print("=" * 70)

segment_results = []
for segment in analysis_complete['audience'].unique():
    seg_data = analysis_complete[analysis_complete['audience'] == segment]
    if len(seg_data) < 50:
        continue
    
    X = sm.add_constant(seg_data[all_predictors])
    y = seg_data['likelihood_visit_tdl']
    m = sm.OLS(y, X).fit()
    
    seg_row = {'segment': segment, 'n': len(seg_data), 'r_squared': m.rsquared}
    for var in all_predictors:
        beta = m.params[var] * seg_data[var].std() / y.std()
        if var.endswith('_tdl'):
            name = var.replace('_tdl', '')
        else:
            name = var.split('_', 1)[1].replace('_', ' ')
        seg_row[f'beta_{name}'] = beta
        seg_row[f'sig_{name}'] = m.pvalues[var] < 0.05
    
    segment_results.append(seg_row)

seg_df = pd.DataFrame(segment_results)
print("\nPath Coefficients by Segment (Consideration → Likelihood):")
print(seg_df[['segment', 'n', 'r_squared', 'beta_consideration']].to_string(index=False))

# ============================================================================
# Save Results
# ============================================================================

print("\n" + "-" * 50)
print("SAVING RESULTS")
print("-" * 50)

# Save full model results
full_df = pd.DataFrame(full_results)
full_df.to_csv(f'{OUTPUT_DIR}/sem_full_model_results.csv', index=False)
print(f"  Saved: sem_full_model_results.csv")

# Save model comparison
comparison = {
    'metric': ['R-squared', 'Adjusted R-squared', 'AIC', 'BIC', 'F-statistic', 'n'],
    'funnel_only': [m_funnel.rsquared, m_funnel.rsquared_adj, m_funnel.aic, m_funnel.bic, m_funnel.fvalue, len(analysis_complete)],
    'full_model': [m_full.rsquared, m_full.rsquared_adj, m_full.aic, m_full.bic, m_full.fvalue, len(analysis_complete)]
}
pd.DataFrame(comparison).to_csv(f'{OUTPUT_DIR}/sem_model_comparison.csv', index=False)
print(f"  Saved: sem_model_comparison.csv")

# Save segment results
seg_df.to_csv(f'{OUTPUT_DIR}/sem_segment_results.csv', index=False)
print(f"  Saved: sem_segment_results.csv")

# ============================================================================
# Summary for README
# ============================================================================

print("\n" + "=" * 70)
print("  SUMMARY FOR README")
print("=" * 70)

print(f"""
## Full SEM Model Results

### Sample
- **n = {len(analysis_complete)}** respondents with complete funnel and benefit data
- **6 months**: {', '.join(analysis_complete['month'].unique())}

### Marketing Funnel Path Coefficients

| Path | β | p-value | Significance |
|------|---|---------|--------------|
| Familiarity → Opinion | {results[0]['beta']:.3f} | {results[0]['p_value']:.4f} | {'***' if results[0]['p_value'] < 0.001 else '**' if results[0]['p_value'] < 0.01 else '*' if results[0]['p_value'] < 0.05 else 'ns'} |
| Familiarity → Consideration | {results[1]['beta']:.3f} | {results[1]['p_value']:.4f} | {'***' if results[1]['p_value'] < 0.001 else '**' if results[1]['p_value'] < 0.01 else '*' if results[1]['p_value'] < 0.05 else 'ns'} |
| Opinion → Consideration | {results[2]['beta']:.3f} | {results[2]['p_value']:.4f} | {'***' if results[2]['p_value'] < 0.001 else '**' if results[2]['p_value'] < 0.01 else '*' if results[2]['p_value'] < 0.05 else 'ns'} |
""")

print("### Full Model: Funnel + Benefit Factors → Likelihood")
print()
print("| Predictor | β | p-value | Significance |")
print("|-----------|---|---------|--------------|")
for r in full_results:
    sig = '***' if r['p_value'] < 0.001 else '**' if r['p_value'] < 0.01 else '*' if r['p_value'] < 0.05 else ''
    print(f"| {r['predictor']} | {r['beta']:.3f} | {r['p_value']:.4f} | {sig} |")

print(f"""
### Model Fit

| Metric | Funnel Only | Full Model |
|--------|-------------|------------|
| R² | {m_funnel.rsquared:.3f} | {m_full.rsquared:.3f} |
| Adjusted R² | {m_funnel.rsquared_adj:.3f} | {m_full.rsquared_adj:.3f} |
| AIC | {m_funnel.aic:.1f} | {m_full.aic:.1f} |

**F-test**: F({df1}, {df2}) = {f_stat:.2f}, p = {f_pval:.4f}
""")

print("=" * 70)
print("  ANALYSIS COMPLETE")
print("=" * 70)
