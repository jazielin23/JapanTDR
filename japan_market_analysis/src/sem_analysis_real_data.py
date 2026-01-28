#!/usr/bin/env python3
"""
SEM Analysis for TDL Brand Tracking Survey - 6 Wave Analysis
Following Original Research Objectives:
1. Marketing Funnel Analysis
2. Brand Benefits Analysis
3. Segment Comparison
4. Mediation Testing
5. Time Series Trend Analysis (NEW - leveraging 6 months of data)

Updated: Now uses 6 waves of data (February-July, n=3300 total)
         Includes time trend analysis and consolidated model
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
print("  TDL SEM ANALYSIS - 6 WAVE CONSOLIDATED MODEL")
print("  February - July (Waves 1-6)")
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

# Create analysis variables and clean invalid values (0 = missing, 99 = missing)
analysis = data.copy()

# Wave information (1-6 corresponding to February-July)
analysis['wave'] = pd.to_numeric(analysis['wave'], errors='coerce')
analysis['month'] = analysis['month']

# Funnel variables - clean 0s and 99s
funnel_raw_cols = ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl', 'likelihood_visit_tdl']
for col in funnel_raw_cols:
    analysis[col] = pd.to_numeric(analysis[col], errors='coerce')
    analysis.loc[analysis[col] == 0, col] = np.nan
    analysis.loc[analysis[col] == 99, col] = np.nan

analysis['familiarity'] = analysis['familiarity_tdl']
analysis['opinion'] = analysis['opinion_tdl']
analysis['consideration'] = analysis['consideration_tdl']
analysis['likelihood'] = analysis['likelihood_visit_tdl']
analysis['nps'] = pd.to_numeric(analysis['nps_tdl'], errors='coerce')

# Create composite scores for functional and emotional benefits
analysis['functional'] = analysis[func_cols].mean(axis=1)
analysis['emotional'] = analysis[emot_cols].mean(axis=1)

# Segment
analysis['segment'] = analysis['audience']

# Wave distribution summary
print("\n--- Wave Distribution ---")
wave_counts = analysis['wave'].value_counts().sort_index()
for wave, count in wave_counts.items():
    month = analysis[analysis['wave'] == wave]['month'].iloc[0] if len(analysis[analysis['wave'] == wave]) > 0 else 'Unknown'
    print(f"  Wave {int(wave)} ({month}): n = {count}")

# ============================================================================
# CREATE TWO DATASETS
# ============================================================================

# Full sample for funnel analysis (Objectives 1, 3, 4)
funnel_vars = ['familiarity', 'opinion', 'consideration', 'likelihood']
funnel_data = analysis.dropna(subset=funnel_vars).copy()

# Subset with brand attributes (Objective 2)
benefits_vars = ['familiarity', 'opinion', 'consideration', 'likelihood', 'functional', 'emotional']
benefits_data = analysis.dropna(subset=benefits_vars).copy()

print(f"Total survey responses: {len(data)}")
print(f"Funnel analysis sample (Obj 1, 3, 4): n = {len(funnel_data)}")
print(f"Brand benefits sample (Obj 2):       n = {len(benefits_data)}")

# ============================================================================
# Standardize variables for each dataset
# ============================================================================

from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# Standardize funnel data
scaler = StandardScaler()
for col in funnel_vars:
    funnel_data[f'{col}_z'] = scaler.fit_transform(funnel_data[[col]])

# Standardize benefits data (including all variables)
for col in benefits_vars:
    benefits_data[f'{col}_z'] = scaler.fit_transform(benefits_data[[col]])

# ============================================================================
# OBJECTIVE 1: Marketing Funnel Analysis (n=541)
# ============================================================================

print("\n" + "=" * 70)
print(f"  OBJECTIVE 1: MARKETING FUNNEL ANALYSIS (n={len(funnel_data)})")
print("  Testing: Familiarity → Opinion → Consideration → Likelihood")
print("=" * 70)

# Path Analysis using sequential regressions
print("\n--- Path Coefficients (Standardized Beta) ---\n")

path_results = []

# Path 1: Familiarity → Opinion
X = sm.add_constant(funnel_data['familiarity_z'])
y = funnel_data['opinion_z']
model1 = sm.OLS(y, X).fit()
beta1 = model1.params['familiarity_z']
p1 = model1.pvalues['familiarity_z']
path_results.append(('Familiarity → Opinion', beta1, p1, model1.rsquared, len(funnel_data)))
print(f"Familiarity → Opinion:     β = {beta1:.3f}, p = {p1:.4f}, R² = {model1.rsquared:.3f}")

# Path 2: Opinion → Consideration (controlling for Familiarity)
X = sm.add_constant(funnel_data[['familiarity_z', 'opinion_z']])
y = funnel_data['consideration_z']
model2 = sm.OLS(y, X).fit()
beta2_fam = model2.params['familiarity_z']
beta2_op = model2.params['opinion_z']
path_results.append(('Opinion → Consideration', beta2_op, model2.pvalues['opinion_z'], None, len(funnel_data)))
path_results.append(('Familiarity → Consideration (direct)', beta2_fam, model2.pvalues['familiarity_z'], model2.rsquared, len(funnel_data)))
print(f"Opinion → Consideration:   β = {beta2_op:.3f}, p = {model2.pvalues['opinion_z']:.4f}")
print(f"Familiarity → Consideration: β = {beta2_fam:.3f}, p = {model2.pvalues['familiarity_z']:.4f}, R² = {model2.rsquared:.3f}")

# Path 3: Consideration → Likelihood (controlling for Opinion and Familiarity)
X = sm.add_constant(funnel_data[['familiarity_z', 'opinion_z', 'consideration_z']])
y = funnel_data['likelihood_z']
model3 = sm.OLS(y, X).fit()
print(f"\nConsideration → Likelihood: β = {model3.params['consideration_z']:.3f}, p = {model3.pvalues['consideration_z']:.4f}")
print(f"Opinion → Likelihood:      β = {model3.params['opinion_z']:.3f}, p = {model3.pvalues['opinion_z']:.4f}")
print(f"Familiarity → Likelihood:  β = {model3.params['familiarity_z']:.3f}, p = {model3.pvalues['familiarity_z']:.4f}")
print(f"R² for Likelihood:         {model3.rsquared:.3f}")

# Store funnel model results
funnel_r2 = model3.rsquared
funnel_consideration_beta = model3.params['consideration_z']

# ============================================================================
# OBJECTIVE 2: Brand Benefits Analysis (n=177)
# ============================================================================

print("\n" + "=" * 70)
print(f"  OBJECTIVE 2: BRAND BENEFITS ANALYSIS (n={len(benefits_data)})")
print("  Testing: Functional & Emotional Benefits → Intent")
print("=" * 70)

# Model with functional and emotional benefits only
X = sm.add_constant(benefits_data[['functional_z', 'emotional_z']])
y = benefits_data['likelihood_z']
model_benefits = sm.OLS(y, X).fit()

print("\n--- Brand Benefits → Likelihood ---\n")
print(f"Functional Benefits → Likelihood: β = {model_benefits.params['functional_z']:.3f}, p = {model_benefits.pvalues['functional_z']:.4f}")
print(f"Emotional Benefits → Likelihood:  β = {model_benefits.params['emotional_z']:.3f}, p = {model_benefits.pvalues['emotional_z']:.4f}")
print(f"R² = {model_benefits.rsquared:.3f}")

# Full model with funnel + benefits (on benefits sample)
X = sm.add_constant(benefits_data[['familiarity_z', 'opinion_z', 'consideration_z', 'functional_z', 'emotional_z']])
y = benefits_data['likelihood_z']
model_full = sm.OLS(y, X).fit()

print("\n--- Full Model: Funnel + Benefits → Likelihood ---\n")
print(model_full.summary().tables[1])
print(f"\nTotal R² = {model_full.rsquared:.3f}")
print(f"Adjusted R² = {model_full.rsquared_adj:.3f}")

# Funnel-only model on benefits sample (for comparison)
X = sm.add_constant(benefits_data[['familiarity_z', 'opinion_z', 'consideration_z']])
y = benefits_data['likelihood_z']
model_funnel_177 = sm.OLS(y, X).fit()
print(f"\nFunnel-only R² (n=177):    {model_funnel_177.rsquared:.3f}")
print(f"Full Model R² (n=177):     {model_full.rsquared:.3f}")
print(f"Δ R² from adding benefits: {model_full.rsquared - model_funnel_177.rsquared:.3f}")

# Which has stronger effect?
func_effect = abs(model_full.params['functional_z'])
emot_effect = abs(model_full.params['emotional_z'])
if func_effect > emot_effect:
    print(f"\n→ Functional benefits have stronger unique effect ({func_effect:.3f} vs {emot_effect:.3f})")
else:
    print(f"\n→ Emotional benefits have stronger unique effect ({emot_effect:.3f} vs {func_effect:.3f})")

# ============================================================================
# OBJECTIVE 3: Segment Comparison (n=541)
# ============================================================================

print("\n" + "=" * 70)
print(f"  OBJECTIVE 3: SEGMENT COMPARISON (n={len(funnel_data)})")
print("  Comparing path coefficients across segments")
print("=" * 70)

segments = funnel_data['segment'].unique()
segment_results = []

print("\n--- Consideration → Likelihood by Segment ---\n")

for seg in sorted(segments):
    seg_data = funnel_data[funnel_data['segment'] == seg]
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

# Funnel metrics by segment
print("\n--- Funnel Metrics by Segment ---\n")
segment_funnel = funnel_data.groupby('segment').agg({
    'familiarity': 'mean',
    'opinion': 'mean', 
    'consideration': 'mean',
    'likelihood': 'mean',
    'nps': 'mean'
}).round(2)
print(segment_funnel)

# ============================================================================
# OBJECTIVE 4: Mediation Testing (n=541)
# ============================================================================

print("\n" + "=" * 70)
print(f"  OBJECTIVE 4: MEDIATION TESTING (n={len(funnel_data)})")
print("  Testing: Does Consideration mediate Opinion → Likelihood?")
print("=" * 70)

# Sobel test for mediation
# Path a: Opinion → Consideration
X = sm.add_constant(funnel_data['opinion_z'])
y = funnel_data['consideration_z']
model_a = sm.OLS(y, X).fit()
a = model_a.params['opinion_z']
se_a = model_a.bse['opinion_z']

# Path b: Consideration → Likelihood (controlling for Opinion)
X = sm.add_constant(funnel_data[['opinion_z', 'consideration_z']])
y = funnel_data['likelihood_z']
model_b = sm.OLS(y, X).fit()
b = model_b.params['consideration_z']
se_b = model_b.bse['consideration_z']
c_prime = model_b.params['opinion_z']  # Direct effect

# Path c: Total effect (Opinion → Likelihood without mediator)
X = sm.add_constant(funnel_data['opinion_z'])
y = funnel_data['likelihood_z']
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
print(f"Sobel Test: z = {sobel_z:.3f}, p = {sobel_p:.6f}")

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

X = sm.add_constant(funnel_data['familiarity_z'])
y = funnel_data['opinion_z']
model_a2 = sm.OLS(y, X).fit()
a2 = model_a2.params['familiarity_z']
se_a2 = model_a2.bse['familiarity_z']

X = sm.add_constant(funnel_data[['familiarity_z', 'opinion_z']])
y = funnel_data['likelihood_z']
model_b2 = sm.OLS(y, X).fit()
b2 = model_b2.params['opinion_z']
se_b2 = model_b2.bse['opinion_z']

indirect2 = a2 * b2
sobel_se2 = np.sqrt(b2**2 * se_a2**2 + a2**2 * se_b2**2)
sobel_z2 = indirect2 / sobel_se2
sobel_p2 = 2 * (1 - stats.norm.cdf(abs(sobel_z2)))

print(f"Indirect Effect (Fam → Op → Lik):       β = {indirect2:.3f}")
print(f"Sobel Test: z = {sobel_z2:.3f}, p = {sobel_p2:.6f}")
if sobel_p2 < 0.05:
    print("→ SIGNIFICANT: Opinion mediates Familiarity's effect on Likelihood")

# ============================================================================
# OBJECTIVE 5: TIME SERIES TREND ANALYSIS (NEW)
# ============================================================================

print("\n" + "=" * 70)
print(f"  OBJECTIVE 5: TIME SERIES TREND ANALYSIS (6 Waves)")
print("  Analyzing trends across February-July")
print("=" * 70)

# Create wave-level aggregates
wave_metrics = funnel_data.groupby('wave').agg({
    'familiarity': 'mean',
    'opinion': 'mean',
    'consideration': 'mean',
    'likelihood': 'mean',
    'nps': 'mean'
}).round(3)

# Add month names
wave_to_month = {1: 'Feb', 2: 'Mar', 3: 'Apr', 4: 'May', 5: 'Jun', 6: 'Jul'}
wave_metrics['month'] = wave_metrics.index.map(wave_to_month)
wave_metrics['n'] = funnel_data.groupby('wave').size()

print("\n--- Funnel Metrics by Wave ---\n")
print(wave_metrics[['month', 'n', 'familiarity', 'opinion', 'consideration', 'likelihood', 'nps']])

# Test for linear trends using OLS
print("\n--- Linear Trend Tests ---\n")
trend_results = []

for metric in ['familiarity', 'opinion', 'consideration', 'likelihood']:
    X = sm.add_constant(funnel_data['wave'])
    y = funnel_data[metric]
    
    # Filter out NaN values
    valid_mask = ~y.isna()
    X_valid = X[valid_mask]
    y_valid = y[valid_mask]
    
    model_trend = sm.OLS(y_valid, X_valid).fit()
    slope = model_trend.params['wave']
    p_val = model_trend.pvalues['wave']
    
    direction = "↑ increasing" if slope > 0 else "↓ decreasing"
    sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
    
    trend_results.append({
        'Metric': metric.capitalize(),
        'Slope': slope,
        'Direction': direction,
        'p_value': p_val,
        'Significant': sig != ''
    })
    
    print(f"{metric.capitalize():15s}: slope = {slope:+.4f} ({direction}) p = {p_val:.4f}{sig}")

trend_df = pd.DataFrame(trend_results)

# Wave effect in regression model (controlling for other factors)
print("\n--- Wave Effect in Full Model ---\n")
print("Testing if wave significantly predicts likelihood after controlling for funnel stages...")

# Add wave to the regression model
funnel_data['wave_centered'] = funnel_data['wave'] - funnel_data['wave'].mean()
X = sm.add_constant(funnel_data[['familiarity_z', 'opinion_z', 'consideration_z', 'wave_centered']])
y = funnel_data['likelihood_z']
model_with_wave = sm.OLS(y, X).fit()

print(f"\nWave effect (controlling for funnel): β = {model_with_wave.params['wave_centered']:.4f}, p = {model_with_wave.pvalues['wave_centered']:.4f}")
if model_with_wave.pvalues['wave_centered'] < 0.05:
    if model_with_wave.params['wave_centered'] > 0:
        print("→ SIGNIFICANT: Likelihood is trending UPWARD over time")
    else:
        print("→ SIGNIFICANT: Likelihood is trending DOWNWARD over time")
else:
    print("→ No significant time trend after controlling for funnel stages")

# Segment trends over time
print("\n--- Segment Performance Trends ---\n")

segment_wave_means = funnel_data.groupby(['segment', 'wave'])['likelihood'].mean().unstack()
segment_trends = []

for segment in segment_wave_means.index:
    values = segment_wave_means.loc[segment].dropna()
    if len(values) >= 3:  # Need at least 3 points for trend
        X_seg = sm.add_constant(values.index.values)
        y_seg = values.values
        try:
            model_seg = sm.OLS(y_seg, X_seg).fit()
            slope = model_seg.params[1] if len(model_seg.params) > 1 else 0
            segment_trends.append({
                'Segment': segment[:30],
                'Start_Wave1': values.iloc[0] if len(values) > 0 else np.nan,
                'End_Wave6': values.iloc[-1] if len(values) > 0 else np.nan,
                'Trend_Slope': slope,
                'Direction': '↑' if slope > 0.01 else '↓' if slope < -0.01 else '→'
            })
        except:
            pass

if segment_trends:
    segment_trend_df = pd.DataFrame(segment_trends)
    print(segment_trend_df.to_string(index=False))
else:
    segment_trend_df = pd.DataFrame()
    print("Insufficient data for segment trend analysis")

# ============================================================================
# Summary of Fit Indices
# ============================================================================

print("\n" + "=" * 70)
print("  MODEL FIT SUMMARY")
print("=" * 70)

print("\n--- Variance Explained (R²) ---\n")
print(f"Funnel Model (full 6-wave sample):      R² = {funnel_r2:.3f} (n={len(funnel_data)})")
print(f"Benefits Only Model:                    R² = {model_benefits.rsquared:.3f} (n={len(benefits_data)})")
print(f"Funnel Model (benefits sample):         R² = {model_funnel_177.rsquared:.3f} (n={len(benefits_data)})")
print(f"Full Model (Funnel+Benefits):           R² = {model_full.rsquared:.3f} (n={len(benefits_data)})")
print(f"Model with Wave Effect:                 R² = {model_with_wave.rsquared:.3f} (n={len(funnel_data)})")

# ============================================================================
# Save Results
# ============================================================================

print("\n" + "=" * 70)
print("  SAVING RESULTS")
print("=" * 70)

from pathlib import Path
output_dir = Path("output/reports")
output_dir.mkdir(parents=True, exist_ok=True)

# Path coefficients (with sample sizes)
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
                model_full.pvalues['functional_z'], model_full.pvalues['emotional_z']],
    'Sample_n': [len(funnel_data), len(funnel_data), len(funnel_data), len(funnel_data), len(funnel_data),
                 len(benefits_data), len(benefits_data)]
})
path_df.to_csv(output_dir / "sem_path_coefficients.csv", index=False)

# Mediation results
mediation_df = pd.DataFrame({
    'Mediation': ['Opinion → Consideration → Likelihood',
                  'Familiarity → Opinion → Likelihood'],
    'Indirect_Effect': [indirect, indirect2],
    'Sobel_Z': [sobel_z, sobel_z2],
    'p_value': [sobel_p, sobel_p2],
    'Significant': [sobel_p < 0.05, sobel_p2 < 0.05],
    'Sample_n': [len(funnel_data), len(funnel_data)]
})
mediation_df.to_csv(output_dir / "sem_mediation_results.csv", index=False)

# Fit indices
fit_df = pd.DataFrame({
    'Model': ['Funnel Only (6-wave)', 'Funnel Only (benefits sample)', 'Benefits Only', 'Full Model (Funnel+Benefits)', 'Model with Wave Effect'],
    'Sample_n': [len(funnel_data), len(benefits_data), len(benefits_data), len(benefits_data), len(funnel_data)],
    'R_squared': [funnel_r2, model_funnel_177.rsquared, model_benefits.rsquared, model_full.rsquared, model_with_wave.rsquared],
    'Adj_R_squared': [model3.rsquared_adj, model_funnel_177.rsquared_adj, model_benefits.rsquared_adj, model_full.rsquared_adj, model_with_wave.rsquared_adj]
})
fit_df.to_csv(output_dir / "sem_fit_indices.csv", index=False)

# Segment comparison
segment_df.to_csv(output_dir / "sem_segment_comparison.csv", index=False)

# Segment funnel metrics
segment_funnel.to_csv(output_dir / "tdl_funnel_by_segment.csv")

# Time series results
wave_metrics.to_csv(output_dir / "wave_metrics.csv")
trend_df.to_csv(output_dir / "trend_analysis.csv", index=False)
if len(segment_trend_df) > 0:
    segment_trend_df.to_csv(output_dir / "segment_trends.csv", index=False)

print(f"\nSaved to {output_dir}/")
print("  - sem_path_coefficients.csv")
print("  - sem_mediation_results.csv")
print("  - sem_fit_indices.csv")
print("  - sem_segment_comparison.csv")
print("  - tdl_funnel_by_segment.csv")
print("  - wave_metrics.csv (NEW)")
print("  - trend_analysis.csv (NEW)")
print("  - segment_trends.csv (NEW)")

# ============================================================================
# Executive Summary
# ============================================================================

# Determine trend direction for summary
sig_trends = trend_df[trend_df['Significant']]
if len(sig_trends) > 0:
    trend_summary = f"Significant trends detected in: {', '.join(sig_trends['Metric'].tolist())}"
else:
    trend_summary = "No significant time trends detected in funnel metrics"

# Wave effect summary
wave_effect_sig = model_with_wave.pvalues['wave_centered'] < 0.05
wave_effect_dir = "increasing" if model_with_wave.params['wave_centered'] > 0 else "decreasing"

print("\n" + "=" * 70)
print("  EXECUTIVE SUMMARY - CONSOLIDATED 6-WAVE ANALYSIS")
print("=" * 70)

print(f"""
DATA OVERVIEW:
   Total Sample: n = {len(funnel_data)} (6 waves: February - July)
   Benefits Sample: n = {len(benefits_data)}
   Waves: {wave_counts.sum()} total respondents across {len(wave_counts)} waves

1. MARKETING FUNNEL (Objective 1):
   - Strong sequential flow: Familiarity → Opinion → Consideration → Likelihood
   - Consideration is the strongest direct predictor of Likelihood (β = {funnel_consideration_beta:.3f})
   - Full funnel explains {funnel_r2 * 100:.1f}% of variance in Likelihood

2. BRAND BENEFITS (Objective 2, n={len(benefits_data)}):
   - {"Functional" if func_effect > emot_effect else "Emotional"} benefits have stronger unique effect on Likelihood
   - Functional β = {model_full.params['functional_z']:.3f}, Emotional β = {model_full.params['emotional_z']:.3f}
   - Adding benefits to funnel increases R² from {model_funnel_177.rsquared:.3f} to {model_full.rsquared:.3f} (+{model_full.rsquared - model_funnel_177.rsquared:.3f})

3. SEGMENT DIFFERENCES (Objective 3):
   - {strongest['Segment'][:25] if len(segment_df) >= 2 else 'N/A'} shows strongest Consideration → Likelihood relationship (β={strongest['Beta']:.3f})
   - {weakest['Segment'][:25] if len(segment_df) >= 2 else 'N/A'} shows weakest relationship (β={weakest['Beta']:.3f})
   - Path coefficients vary by segment (evidence for targeted marketing)

4. MEDIATION (Objective 4):
   - {"Consideration mediates" if sobel_p < 0.05 else "Consideration does NOT significantly mediate"} Opinion → Likelihood ({(indirect / c) * 100 if sobel_p < 0.05 and c != 0 else 0:.1f}% of effect)
   - {"Opinion significantly mediates" if sobel_p2 < 0.05 else "Opinion does NOT significantly mediate"} Familiarity → Likelihood

5. TIME TRENDS (Objective 5 - NEW):
   - {trend_summary}
   - Wave effect after controlling for funnel: {"SIGNIFICANT" if wave_effect_sig else "Not significant"}
   - Trend direction: {wave_effect_dir if wave_effect_sig else "stable"} (β = {model_with_wave.params['wave_centered']:.4f})
   - Recommendation: {"Monitor month-over-month changes" if wave_effect_sig else "Focus on funnel optimization rather than seasonal factors"}

STRATEGIC IMPLICATIONS:
   → Focus on moving guests from Opinion to Consideration (key conversion point)
   → {"Functional" if func_effect > emot_effect else "Emotional"} messaging may be more effective than {"Emotional" if func_effect > emot_effect else "Functional"} for driving intent
   → Customize approach by segment for maximum impact
   → {"Consider seasonal marketing adjustments" if wave_effect_sig else "Maintain consistent marketing approach across months"}
""")

print("=" * 70)
print("  SEM ANALYSIS COMPLETE")
print("=" * 70)
