#!/usr/bin/env python3
"""
TDL Real Data Analysis
Using validated Likert scale mappings from Relabeled Raw Data.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("  TDL REAL DATA ANALYSIS")
print("=" * 70)
print()

# ============================================================================
# Load Data
# ============================================================================

print("Loading TDL survey data...")
data = pd.read_csv("dbt_project/seeds/survey_responses_tdl.csv")
print(f"Loaded {len(data)} respondents")

# ============================================================================
# Data Preparation
# ============================================================================

print("\nPreparing data...")

# Convert columns to numeric
numeric_cols = [
    'familiarity_tdl', 'familiarity_tds', 'familiarity_usj',
    'opinion_tdl', 'opinion_tds', 'opinion_usj',
    'consideration_tdl', 'consideration_tds', 'consideration_usj',
    'likelihood_visit_tdl', 'likelihood_visit_tds', 'likelihood_visit_usj',
    'nps_tdl', 'nps_tds', 'nps_usj'
]

# TDL functional attributes
func_cols = [c for c in data.columns if c.startswith('tdl_func_')]
# TDL emotional attributes
emot_cols = [c for c in data.columns if c.startswith('tdl_emot_')]
# Bipolar columns
bipolar_cols = [c for c in data.columns if c.startswith('bipolar_')]

for col in numeric_cols + func_cols + emot_cols + bipolar_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Replace 99 and 0 with NaN (missing values)
# 0 = not answered, 99 = don't know
data = data.replace(99, np.nan)
for col in func_cols + emot_cols + bipolar_cols:
    data.loc[data[col] == 0, col] = np.nan

# Create analysis dataset
analysis = data.copy()
analysis['segment'] = analysis['audience']
analysis['gender'] = analysis['gender'].map({'1': 'Male', '2': 'Female'})
analysis['age'] = pd.to_numeric(analysis['age'], errors='coerce')

# Valid responses for funnel analysis
funnel_valid = analysis[analysis['familiarity_tdl'].notna() & 
                        analysis['likelihood_visit_tdl'].notna()].copy()
print(f"Analysis sample: {len(funnel_valid)} respondents")

# ============================================================================
# Descriptive Statistics
# ============================================================================

print("\n" + "-" * 50)
print("DESCRIPTIVE STATISTICS")
print("-" * 50)

# Sample by segment
segment_summary = funnel_valid.groupby('segment').agg({
    'respondent_id': 'count',
    'age': 'mean',
    'gender': lambda x: (x == 'Female').mean() * 100
}).round(1)
segment_summary.columns = ['n', 'mean_age', 'pct_female']
segment_summary['pct'] = (segment_summary['n'] / len(funnel_valid) * 100).round(1)

print("\nSample by Segment:")
print(segment_summary[['n', 'pct', 'mean_age', 'pct_female']])

# Funnel metrics by segment
print("\nFunnel Metrics by Segment (Scale 1-5, 5=Best):")
funnel_by_segment = funnel_valid.groupby('segment').agg({
    'familiarity_tdl': 'mean',
    'opinion_tdl': 'mean',
    'consideration_tdl': 'mean',
    'likelihood_visit_tdl': 'mean',
    'nps_tdl': 'mean'
}).round(2)
print(funnel_by_segment)

# ============================================================================
# Overall Funnel
# ============================================================================

print("\n" + "-" * 50)
print("OVERALL TDL FUNNEL (Scale 1-5)")
print("-" * 50)

overall = funnel_valid[['familiarity_tdl', 'opinion_tdl', 
                        'consideration_tdl', 'likelihood_visit_tdl']].mean()
print(f"\n  Familiarity:    {overall['familiarity_tdl']:.2f}")
print(f"  Opinion:        {overall['opinion_tdl']:.2f}")
print(f"  Consideration:  {overall['consideration_tdl']:.2f}")
print(f"  Likelihood:     {overall['likelihood_visit_tdl']:.2f}")

# Funnel tier distribution
print("\nFunnel Tier Distribution:")
for col, label in [('familiarity_tdl', 'Familiarity'), 
                   ('opinion_tdl', 'Opinion'),
                   ('consideration_tdl', 'Consideration'),
                   ('likelihood_visit_tdl', 'Likelihood')]:
    high = (funnel_valid[col] >= 4).mean() * 100
    med = ((funnel_valid[col] == 3)).mean() * 100
    low = (funnel_valid[col] <= 2).mean() * 100
    print(f"  {label}: High={high:.1f}%, Medium={med:.1f}%, Low={low:.1f}%")

# ============================================================================
# Attribute Analysis
# ============================================================================

print("\n" + "-" * 50)
print("TDL ATTRIBUTE RATINGS (Scale 1-5, 5=Best)")
print("-" * 50)

# Functional attributes
func_means = funnel_valid[func_cols].mean().sort_values(ascending=False)
print("\nFunctional Attributes (Top 10):")
for attr, score in func_means.head(10).items():
    attr_name = attr.replace('tdl_func_', '')
    print(f"  {attr_name}: {score:.2f}")

print("\nFunctional Attributes (Bottom 5):")
for attr, score in func_means.tail(5).items():
    attr_name = attr.replace('tdl_func_', '')
    print(f"  {attr_name}: {score:.2f}")

# Emotional attributes
emot_means = funnel_valid[emot_cols].mean().sort_values(ascending=False)
print("\nEmotional Attributes:")
for attr, score in emot_means.items():
    attr_name = attr.replace('tdl_emot_', '')
    print(f"  {attr_name}: {score:.2f}")

# ============================================================================
# TDR vs USJ Comparison
# ============================================================================

print("\n" + "-" * 50)
print("TDR vs USJ BIPOLAR COMPARISON")
print("-" * 50)
print("(Scale: 1=Definitely TDR, 4=Neutral, 7=Definitely USJ)")

bipolar_means = funnel_valid[bipolar_cols].mean().sort_values()
print("\nTDR Strengths (score < 4):")
for attr, score in bipolar_means.items():
    if score < 4 and not pd.isna(score):
        attr_name = attr.replace('bipolar_', '')
        print(f"  {attr_name}: {score:.2f}")

print("\nUSJ Strengths (score > 4):")
for attr, score in bipolar_means.items():
    if score > 4 and not pd.isna(score):
        attr_name = attr.replace('bipolar_', '')
        print(f"  {attr_name}: {score:.2f}")

# ============================================================================
# Correlation Analysis
# ============================================================================

print("\n" + "-" * 50)
print("KEY CORRELATIONS WITH LIKELIHOOD")
print("-" * 50)

# Create composite scores
funnel_valid['functional_mean'] = funnel_valid[func_cols].mean(axis=1)
funnel_valid['emotional_mean'] = funnel_valid[emot_cols].mean(axis=1)

# Correlations with likelihood
cor_cols = ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl',
            'functional_mean', 'emotional_mean', 'nps_tdl']
correlations = funnel_valid[cor_cols + ['likelihood_visit_tdl']].corr()['likelihood_visit_tdl']

print("\nCorrelations with Likelihood to Visit:")
for col, corr in correlations.drop('likelihood_visit_tdl').sort_values(ascending=False).items():
    print(f"  {col}: r = {corr:.3f}")

# ============================================================================
# Segment Comparison
# ============================================================================

print("\n" + "-" * 50)
print("SEGMENT PERFORMANCE COMPARISON")
print("-" * 50)

segment_perf = funnel_valid.groupby('segment').agg({
    'likelihood_visit_tdl': 'mean',
    'consideration_tdl': 'mean',
    'functional_mean': 'mean',
    'emotional_mean': 'mean',
    'nps_tdl': 'mean',
    'respondent_id': 'count'
}).round(2)
segment_perf.columns = ['likelihood', 'consideration', 'functional', 'emotional', 'nps', 'n']
segment_perf = segment_perf.sort_values('likelihood', ascending=False)

print("\nRanked by Likelihood to Visit:")
print(segment_perf)

# ============================================================================
# TDL vs Competitor Gaps
# ============================================================================

print("\n" + "-" * 50)
print("TDL vs COMPETITOR GAPS")
print("-" * 50)

gap_analysis = pd.DataFrame({
    'TDL': [
        funnel_valid['familiarity_tdl'].mean(),
        funnel_valid['opinion_tdl'].mean(),
        funnel_valid['consideration_tdl'].mean(),
        funnel_valid['likelihood_visit_tdl'].mean()
    ],
    'TDS': [
        funnel_valid['familiarity_tds'].mean(),
        funnel_valid['opinion_tds'].mean(),
        funnel_valid['consideration_tds'].mean(),
        funnel_valid['likelihood_visit_tds'].mean()
    ],
    'USJ': [
        funnel_valid['familiarity_usj'].mean(),
        funnel_valid['opinion_usj'].mean(),
        funnel_valid['consideration_usj'].mean(),
        funnel_valid['likelihood_visit_usj'].mean()
    ]
}, index=['Familiarity', 'Opinion', 'Consideration', 'Likelihood'])

gap_analysis['TDL_vs_USJ'] = gap_analysis['TDL'] - gap_analysis['USJ']
gap_analysis['TDL_vs_TDS'] = gap_analysis['TDL'] - gap_analysis['TDS']

print("\nFunnel Comparison:")
print(gap_analysis.round(2))

# ============================================================================
# Generate Output Files
# ============================================================================

print("\n" + "-" * 50)
print("SAVING RESULTS")
print("-" * 50)

output_dir = Path("output/reports")
output_dir.mkdir(parents=True, exist_ok=True)

segment_summary.to_csv(output_dir / "tdl_segment_summary.csv")
funnel_by_segment.to_csv(output_dir / "tdl_funnel_by_segment.csv")
segment_perf.to_csv(output_dir / "tdl_segment_performance.csv")
gap_analysis.to_csv(output_dir / "tdl_competitor_gaps.csv")

# Save attribute rankings
func_means.to_csv(output_dir / "tdl_functional_attributes.csv")
emot_means.to_csv(output_dir / "tdl_emotional_attributes.csv")

print(f"Saved reports to {output_dir}/")

# ============================================================================
# Executive Summary
# ============================================================================

print("\n" + "=" * 70)
print("  TDL ANALYSIS - EXECUTIVE SUMMARY")
print("=" * 70)

print(f"\n1. SAMPLE: {len(funnel_valid)} respondents")

print("\n2. OVERALL FUNNEL (Scale 1-5, 5=Best):")
print(f"   Familiarity:   {overall['familiarity_tdl']:.2f}")
print(f"   Opinion:       {overall['opinion_tdl']:.2f}")
print(f"   Consideration: {overall['consideration_tdl']:.2f}")
print(f"   Likelihood:    {overall['likelihood_visit_tdl']:.2f}")

print("\n3. TOP SEGMENT:")
print(f"   {segment_perf.index[0]} (Likelihood: {segment_perf['likelihood'].iloc[0]:.2f})")

print("\n4. TOP ATTRIBUTES:")
for i, (attr, score) in enumerate(func_means.head(3).items()):
    print(f"   {i+1}. {attr.replace('tdl_func_', '')}: {score:.2f}")

print("\n5. KEY DRIVERS (Correlation with Likelihood):")
for col, corr in correlations.drop('likelihood_visit_tdl').sort_values(ascending=False).head(3).items():
    print(f"   - {col}: r = {corr:.3f}")

print("\n6. VS COMPETITORS:")
if gap_analysis.loc['Likelihood', 'TDL_vs_USJ'] > 0:
    print(f"   TDL outperforms USJ on Likelihood (+{gap_analysis.loc['Likelihood', 'TDL_vs_USJ']:.2f})")
else:
    print(f"   USJ outperforms TDL on Likelihood ({gap_analysis.loc['Likelihood', 'TDL_vs_USJ']:.2f})")

print("\n" + "=" * 70)
print("  ANALYSIS COMPLETE")
print("=" * 70)
print()
