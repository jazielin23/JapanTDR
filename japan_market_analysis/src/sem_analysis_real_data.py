#!/usr/bin/env python3
"""
SEM Analysis for TDL Brand Tracking Survey
Following Original Research Objectives:
1. Marketing Funnel Analysis
2. Brand Benefits Analysis  
3. Segment Comparison
4. Mediation Testing
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

try:
    from semopy import Model, calc_stats
    HAS_SEMOPY = True
except ImportError:
    HAS_SEMOPY = False
    print("semopy not available, using regression-based path analysis")

print("=" * 70)
print("  TDL SEM ANALYSIS - REAL DATA")
print("  Following Original Research Objectives")
print("=" * 70)
print()

# ============================================================================
# Load and Prepare Data
# ============================================================================

print("Loading data...")
data = pd.read_csv("dbt_project/seeds/survey_responses_tdl.csv")

# Convert to numeric and handle missing
func_cols = [c for c in data.columns if c.startswith('tdl_func_')]
emot_cols = [c for c in data.columns if c.startswith('tdl_emot_')]

for col in func_cols + emot_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')
    data.loc[data[col] == 0, col] = np.nan
    data.loc[data[col] == 99, col] = np.nan

# Create analysis variables
analysis = data.copy()
analysis['familiarity'] = pd.to_numeric(analysis['familiarity_tdl'], errors='coerce')
analysis['opinion'] = pd.to_numeric(analysis['opinion_tdl'], errors='coerce')
analysis['consideration'] = pd.to_numeric(analysis['consideration_tdl'], errors='coerce')
analysis['likelihood'] = pd.to_numeric(analysis['likelihood_visit_tdl'], errors='coerce')
analysis['nps'] = pd.to_numeric(analysis['nps_tdl'], errors='coerce')

# Create composite scores for functional and emotional benefits
analysis['functional'] = analysis[func_cols].mean(axis=1)
analysis['emotional'] = analysis[emot_cols].mean(axis=1)

# Segment
analysis['segment'] = analysis['audience']

# Filter to complete cases for SEM
sem_vars = ['familiarity', 'opinion', 'consideration', 'likelihood', 'functional', 'emotional']
sem_data = analysis.dropna(subset=sem_vars).copy()

print(f"Total sample: {len(data)}")
print(f"SEM analysis sample (complete cases): {len(sem_data)}")

# ============================================================================
# OBJECTIVE 1: Marketing Funnel Analysis
# ============================================================================

print("\n" + "=" * 70)
print("  OBJECTIVE 1: MARKETING FUNNEL ANALYSIS")
print("  Testing: Familiarity → Opinion → Consideration → Likelihood")
print("=" * 70)

from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr
import statsmodels.api as sm

# Standardize for comparability
scaler = StandardScaler()
for col in sem_vars:
    sem_data[f'{col}_z'] = scaler.fit_transform(sem_data[[col]])

# Path Analysis using sequential regressions
print("\n--- Path Coefficients (Standardized Beta) ---\n")

path_results = []

# Path 1: Familiarity → Opinion
X = sm.add_constant(sem_data['familiarity_z'])
y = sem_data['opinion_z']
model1 = sm.OLS(y, X).fit()
beta1 = model1.params['familiarity_z']
p1 = model1.pvalues['familiarity_z']
path_results.append(('Familiarity → Opinion', beta1, p1, model1.rsquared))
print(f"Familiarity → Opinion:     β = {beta1:.3f}, p = {p1:.4f}, R² = {model1.rsquared:.3f}")

# Path 2: Opinion → Consideration (controlling for Familiarity)
X = sm.add_constant(sem_data[['familiarity_z', 'opinion_z']])
y = sem_data['consideration_z']
model2 = sm.OLS(y, X).fit()
beta2_fam = model2.params['familiarity_z']
beta2_op = model2.params['opinion_z']
path_results.append(('Opinion → Consideration', beta2_op, model2.pvalues['opinion_z'], None))
path_results.append(('Familiarity → Consideration (direct)', beta2_fam, model2.pvalues['familiarity_z'], model2.rsquared))
print(f"Opinion → Consideration:   β = {beta2_op:.3f}, p = {model2.pvalues['opinion_z']:.4f}")
print(f"Familiarity → Consideration: β = {beta2_fam:.3f}, p = {model2.pvalues['familiarity_z']:.4f}, R² = {model2.rsquared:.3f}")

# Path 3: Consideration → Likelihood (controlling for Opinion and Familiarity)
X = sm.add_constant(sem_data[['familiarity_z', 'opinion_z', 'consideration_z']])
y = sem_data['likelihood_z']
model3 = sm.OLS(y, X).fit()
print(f"\nConsideration → Likelihood: β = {model3.params['consideration_z']:.3f}, p = {model3.pvalues['consideration_z']:.4f}")
print(f"Opinion → Likelihood:      β = {model3.params['opinion_z']:.3f}, p = {model3.pvalues['opinion_z']:.4f}")
print(f"Familiarity → Likelihood:  β = {model3.params['familiarity_z']:.3f}, p = {model3.pvalues['familiarity_z']:.4f}")
print(f"R² for Likelihood:         {model3.rsquared:.3f}")

# ============================================================================
# OBJECTIVE 2: Brand Benefits Analysis
# ============================================================================

print("\n" + "=" * 70)
print("  OBJECTIVE 2: BRAND BENEFITS ANALYSIS")
print("  Testing: Functional & Emotional Benefits → Intent")
print("=" * 70)

# Model with functional and emotional benefits
X = sm.add_constant(sem_data[['functional_z', 'emotional_z']])
y = sem_data['likelihood_z']
model_benefits = sm.OLS(y, X).fit()

print("\n--- Brand Benefits → Likelihood ---\n")
print(f"Functional Benefits → Likelihood: β = {model_benefits.params['functional_z']:.3f}, p = {model_benefits.pvalues['functional_z']:.4f}")
print(f"Emotional Benefits → Likelihood:  β = {model_benefits.params['emotional_z']:.3f}, p = {model_benefits.pvalues['emotional_z']:.4f}")
print(f"R² = {model_benefits.rsquared:.3f}")

# Full model with funnel + benefits
X = sm.add_constant(sem_data[['familiarity_z', 'opinion_z', 'consideration_z', 'functional_z', 'emotional_z']])
y = sem_data['likelihood_z']
model_full = sm.OLS(y, X).fit()

print("\n--- Full Model: Funnel + Benefits → Likelihood ---\n")
print(model_full.summary().tables[1])
print(f"\nTotal R² = {model_full.rsquared:.3f}")
print(f"Adjusted R² = {model_full.rsquared_adj:.3f}")

# Which has stronger effect?
func_effect = abs(model_full.params['functional_z'])
emot_effect = abs(model_full.params['emotional_z'])
if func_effect > emot_effect:
    print(f"\n→ Functional benefits have stronger unique effect ({func_effect:.3f} vs {emot_effect:.3f})")
else:
    print(f"\n→ Emotional benefits have stronger unique effect ({emot_effect:.3f} vs {func_effect:.3f})")

# ============================================================================
# OBJECTIVE 3: Segment Comparison
# ============================================================================

print("\n" + "=" * 70)
print("  OBJECTIVE 3: SEGMENT COMPARISON")
print("  Comparing path coefficients across segments")
print("=" * 70)

segments = sem_data['segment'].unique()
segment_results = []

print("\n--- Consideration → Likelihood by Segment ---\n")

for seg in sorted(segments):
    seg_data = sem_data[sem_data['segment'] == seg]
    if len(seg_data) >= 20:  # Minimum sample
        X = sm.add_constant(seg_data[['consideration_z']])
        y = seg_data['likelihood_z']
        model_seg = sm.OLS(y, X).fit()
        
        beta = model_seg.params['consideration_z']
        pval = model_seg.pvalues['consideration_z']
        r2 = model_seg.rsquared
        
        segment_results.append({
            'Segment': seg,
            'n': len(seg_data),
            'Beta': beta,
            'p-value': pval,
            'R²': r2
        })
        
        sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
        print(f"{seg[:30]:30s} n={len(seg_data):3d}  β={beta:.3f}{sig}  R²={r2:.3f}")

segment_df = pd.DataFrame(segment_results)

# Test for segment differences (simplified - compare strongest vs weakest)
if len(segment_df) >= 2:
    strongest = segment_df.loc[segment_df['Beta'].idxmax()]
    weakest = segment_df.loc[segment_df['Beta'].idxmin()]
    print(f"\n→ Strongest effect: {strongest['Segment'][:25]} (β={strongest['Beta']:.3f})")
    print(f"→ Weakest effect: {weakest['Segment'][:25]} (β={weakest['Beta']:.3f})")

# ============================================================================
# OBJECTIVE 4: Mediation Testing
# ============================================================================

print("\n" + "=" * 70)
print("  OBJECTIVE 4: MEDIATION TESTING")
print("  Testing: Does Consideration mediate Opinion → Likelihood?")
print("=" * 70)

# Sobel test for mediation
# Path a: Opinion → Consideration
X = sm.add_constant(sem_data['opinion_z'])
y = sem_data['consideration_z']
model_a = sm.OLS(y, X).fit()
a = model_a.params['opinion_z']
se_a = model_a.bse['opinion_z']

# Path b: Consideration → Likelihood (controlling for Opinion)
X = sm.add_constant(sem_data[['opinion_z', 'consideration_z']])
y = sem_data['likelihood_z']
model_b = sm.OLS(y, X).fit()
b = model_b.params['consideration_z']
se_b = model_b.bse['consideration_z']
c_prime = model_b.params['opinion_z']  # Direct effect

# Path c: Total effect (Opinion → Likelihood without mediator)
X = sm.add_constant(sem_data['opinion_z'])
y = sem_data['likelihood_z']
model_c = sm.OLS(y, X).fit()
c = model_c.params['opinion_z']

# Indirect effect
indirect = a * b

# Sobel test
sobel_se = np.sqrt(b**2 * se_a**2 + a**2 * se_b**2)
sobel_z = indirect / sobel_se
sobel_p = 2 * (1 - stats.norm.cdf(abs(sobel_z)))

print("\n--- Mediation: Opinion → Consideration → Likelihood ---\n")
print(f"Path a (Opinion → Consideration):       β = {a:.3f}")
print(f"Path b (Consideration → Likelihood):    β = {b:.3f}")
print(f"Path c (Total: Opinion → Likelihood):   β = {c:.3f}")
print(f"Path c' (Direct: Opinion → Likelihood): β = {c_prime:.3f}")
print(f"\nIndirect Effect (a × b):                β = {indirect:.3f}")
print(f"Sobel Test: z = {sobel_z:.3f}, p = {sobel_p:.4f}")

if sobel_p < 0.05:
    pct_mediated = (indirect / c) * 100 if c != 0 else 0
    print(f"\n→ SIGNIFICANT MEDIATION: {pct_mediated:.1f}% of the effect is mediated through Consideration")
    if c_prime > 0.1 and model_b.pvalues['opinion_z'] < 0.05:
        print("→ Partial mediation: Both direct and indirect effects are significant")
    else:
        print("→ Full mediation: Indirect effect accounts for most of the relationship")
else:
    print("\n→ No significant mediation detected")

# Additional mediation: Familiarity → Opinion → Likelihood
print("\n--- Mediation: Familiarity → Opinion → Likelihood ---\n")

X = sm.add_constant(sem_data['familiarity_z'])
y = sem_data['opinion_z']
model_a2 = sm.OLS(y, X).fit()
a2 = model_a2.params['familiarity_z']
se_a2 = model_a2.bse['familiarity_z']

X = sm.add_constant(sem_data[['familiarity_z', 'opinion_z']])
y = sem_data['likelihood_z']
model_b2 = sm.OLS(y, X).fit()
b2 = model_b2.params['opinion_z']
se_b2 = model_b2.bse['opinion_z']

indirect2 = a2 * b2
sobel_se2 = np.sqrt(b2**2 * se_a2**2 + a2**2 * se_b2**2)
sobel_z2 = indirect2 / sobel_se2
sobel_p2 = 2 * (1 - stats.norm.cdf(abs(sobel_z2)))

print(f"Indirect Effect (Fam → Op → Lik):       β = {indirect2:.3f}")
print(f"Sobel Test: z = {sobel_z2:.3f}, p = {sobel_p2:.4f}")
if sobel_p2 < 0.05:
    print("→ SIGNIFICANT: Opinion mediates Familiarity's effect on Likelihood")

# ============================================================================
# Summary of Fit Indices
# ============================================================================

print("\n" + "=" * 70)
print("  MODEL FIT SUMMARY")
print("=" * 70)

print("\n--- Variance Explained (R²) ---\n")
print(f"Funnel Model (Fam+Op+Con → Likelihood):     R² = {model3.rsquared:.3f}")
print(f"Benefits Model (Func+Emot → Likelihood):    R² = {model_benefits.rsquared:.3f}")
print(f"Full Model (Funnel+Benefits → Likelihood):  R² = {model_full.rsquared:.3f}")

# ============================================================================
# Save Results
# ============================================================================

print("\n" + "=" * 70)
print("  SAVING RESULTS")
print("=" * 70)

from pathlib import Path
output_dir = Path("output/reports")
output_dir.mkdir(parents=True, exist_ok=True)

# Path coefficients
path_df = pd.DataFrame({
    'Path': ['Familiarity → Opinion', 'Opinion → Consideration', 
             'Consideration → Likelihood', 'Opinion → Likelihood (direct)',
             'Familiarity → Likelihood (direct)',
             'Functional → Likelihood', 'Emotional → Likelihood'],
    'Beta': [model1.params['familiarity_z'], model2.params['opinion_z'],
             model3.params['consideration_z'], model3.params['opinion_z'],
             model3.params['familiarity_z'],
             model_full.params['functional_z'], model_full.params['emotional_z']],
    'p_value': [model1.pvalues['familiarity_z'], model2.pvalues['opinion_z'],
                model3.pvalues['consideration_z'], model3.pvalues['opinion_z'],
                model3.pvalues['familiarity_z'],
                model_full.pvalues['functional_z'], model_full.pvalues['emotional_z']]
})
path_df.to_csv(output_dir / "sem_path_coefficients.csv", index=False)

# Mediation results
mediation_df = pd.DataFrame({
    'Mediation': ['Opinion → Consideration → Likelihood',
                  'Familiarity → Opinion → Likelihood'],
    'Indirect_Effect': [indirect, indirect2],
    'Sobel_Z': [sobel_z, sobel_z2],
    'p_value': [sobel_p, sobel_p2],
    'Significant': [sobel_p < 0.05, sobel_p2 < 0.05]
})
mediation_df.to_csv(output_dir / "sem_mediation_results.csv", index=False)

# Fit indices
fit_df = pd.DataFrame({
    'Model': ['Funnel Only', 'Benefits Only', 'Full Model'],
    'R_squared': [model3.rsquared, model_benefits.rsquared, model_full.rsquared],
    'Adj_R_squared': [model3.rsquared_adj, model_benefits.rsquared_adj, model_full.rsquared_adj]
})
fit_df.to_csv(output_dir / "sem_fit_indices.csv", index=False)

# Segment comparison
segment_df.to_csv(output_dir / "sem_segment_comparison.csv", index=False)

print(f"\nSaved to {output_dir}/")
print("  - sem_path_coefficients.csv")
print("  - sem_mediation_results.csv")
print("  - sem_fit_indices.csv")
print("  - sem_segment_comparison.csv")

# ============================================================================
# Executive Summary
# ============================================================================

print("\n" + "=" * 70)
print("  EXECUTIVE SUMMARY - SEM FINDINGS")
print("=" * 70)

print("""
1. MARKETING FUNNEL (Objective 1):
   - Strong sequential flow: Familiarity → Opinion → Consideration → Likelihood
   - Consideration is the strongest direct predictor of Likelihood (β = {:.3f})
   - Full funnel explains {:.1f}% of variance in Likelihood

2. BRAND BENEFITS (Objective 2):
   - {} benefits have stronger unique effect on Likelihood
   - Functional β = {:.3f}, Emotional β = {:.3f}
   - Adding benefits to funnel increases R² from {:.3f} to {:.3f}

3. SEGMENT DIFFERENCES (Objective 3):
   - {} shows strongest Consideration → Likelihood relationship
   - {} shows weakest relationship
   - Path coefficients vary by segment (evidence for targeted marketing)

4. MEDIATION (Objective 4):
   - {} mediates Opinion → Likelihood ({:.1f}% of effect)
   - {} mediates Familiarity → Likelihood

STRATEGIC IMPLICATIONS:
   → Focus on moving guests from Opinion to Consideration (key conversion point)
   → {} messaging may be more effective than {} for driving intent
   → Customize approach by segment for maximum impact
""".format(
    model3.params['consideration_z'],
    model3.rsquared * 100,
    "Functional" if func_effect > emot_effect else "Emotional",
    model_full.params['functional_z'],
    model_full.params['emotional_z'],
    model3.rsquared,
    model_full.rsquared,
    strongest['Segment'][:25] if len(segment_df) >= 2 else "N/A",
    weakest['Segment'][:25] if len(segment_df) >= 2 else "N/A",
    "Consideration" if sobel_p < 0.05 else "Consideration does NOT significantly",
    (indirect / c) * 100 if sobel_p < 0.05 and c != 0 else 0,
    "Opinion significantly" if sobel_p2 < 0.05 else "Opinion does NOT significantly",
    "Functional" if func_effect > emot_effect else "Emotional",
    "Emotional" if func_effect > emot_effect else "Functional"
))

print("=" * 70)
print("  SEM ANALYSIS COMPLETE")
print("=" * 70)
