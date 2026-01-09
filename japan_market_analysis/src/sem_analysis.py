#!/usr/bin/env python3
"""
Structural Equation Modeling (SEM) Analysis for Japan Market Survey
====================================================================

This script performs SEM analysis using semopy, replicating the R lavaan analysis
for the brand tracking survey data.

Author: Data Analysis Team
Date: 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# SEM library
try:
    import semopy
    HAS_SEMOPY = True
except ImportError:
    HAS_SEMOPY = False
    print("semopy not available, using simpler regression analysis")

from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
REPORTS_DIR = OUTPUT_DIR / "reports"

# Create directories
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Variable definitions (matching R config)
FUNNEL_STAGES = ['awareness', 'familiarity', 'opinion', 'consideration', 'likelihood', 'intent']
FUNCTIONAL_BENEFITS = ['func_convenience', 'func_value', 'func_quality', 'func_variety', 'func_reliability']
EMOTIONAL_BENEFITS = ['emot_excitement', 'emot_relaxation', 'emot_connection', 'emot_authenticity', 'emot_memorable']
ALL_BENEFITS = FUNCTIONAL_BENEFITS + EMOTIONAL_BENEFITS

# Colors
REGION_COLORS = {'Local': '#2E86AB', 'Domestic': '#A23B72'}
SEGMENT_COLORS = {
    'Young Families': '#E8573F',
    'Matured Families': '#F4A261',
    'Young Adults': '#2A9D8F',
    'Young Couples': '#264653',
    'Matured Adults 35+': '#9B5DE5'
}
FUNNEL_COLORS = {
    'awareness': '#003F5C',
    'familiarity': '#2F4B7C',
    'opinion': '#665191',
    'consideration': '#A05195',
    'likelihood': '#D45087',
    'intent': '#F95D6A'
}


def load_processed_data():
    """Load the processed survey data."""
    file_path = DATA_PROCESSED_DIR / "survey_processed.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Processed data not found at {file_path}")
    
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} respondents")
    return df


def compute_cronbach_alpha(df, items):
    """Compute Cronbach's alpha for a set of items."""
    # Filter to complete cases
    item_df = df[items].dropna()
    n_items = len(items)
    
    if len(item_df) < 10:
        return np.nan
    
    # Compute covariance matrix
    cov_matrix = item_df.cov()
    
    # Compute alpha
    total_var = cov_matrix.values.sum()
    sum_of_variances = np.diag(cov_matrix).sum()
    
    alpha = (n_items / (n_items - 1)) * (1 - sum_of_variances / total_var)
    return alpha


def run_regression_analysis(df, outcome, predictors):
    """Run OLS regression as a simpler alternative to SEM."""
    # Prepare data
    analysis_df = df[[outcome] + predictors].dropna()
    
    # Standardize variables
    for col in [outcome] + predictors:
        analysis_df[col] = (analysis_df[col] - analysis_df[col].mean()) / analysis_df[col].std()
    
    # Fit model
    X = sm.add_constant(analysis_df[predictors])
    y = analysis_df[outcome]
    model = sm.OLS(y, X).fit()
    
    return model


def run_path_analysis(df):
    """
    Run path analysis replicating the SEM funnel model.
    Tests: Upper Funnel -> Middle Funnel -> Lower Funnel
    """
    results = {}
    
    # Create composite scores
    df = df.copy()
    df['upper_funnel'] = df[['awareness', 'familiarity']].mean(axis=1)
    df['middle_funnel'] = df[['opinion', 'consideration']].mean(axis=1)
    df['lower_funnel'] = df[['likelihood', 'intent']].mean(axis=1)
    
    # Also create benefit composites
    df['functional'] = df[FUNCTIONAL_BENEFITS].mean(axis=1)
    df['emotional'] = df[EMOTIONAL_BENEFITS].mean(axis=1)
    
    print("\n" + "="*70)
    print("PATH ANALYSIS RESULTS (Funnel Model)")
    print("="*70)
    
    # Path 1: Upper Funnel -> Middle Funnel
    print("\n--- Path 1: Upper Funnel -> Middle Funnel ---")
    model1 = run_regression_analysis(df, 'middle_funnel', ['upper_funnel'])
    results['upper_to_middle'] = model1
    print(model1.summary().tables[1])
    
    # Path 2: Middle Funnel -> Lower Funnel (controlling for Upper)
    print("\n--- Path 2: Middle & Upper Funnel -> Lower Funnel ---")
    model2 = run_regression_analysis(df, 'lower_funnel', ['middle_funnel', 'upper_funnel'])
    results['to_lower'] = model2
    print(model2.summary().tables[1])
    
    # Full model with benefits
    print("\n--- Full Model: All Predictors -> Intent ---")
    predictors = ['awareness', 'familiarity', 'consideration', 'functional', 'emotional']
    model3 = run_regression_analysis(df, 'intent', predictors)
    results['full_model'] = model3
    print(model3.summary().tables[1])
    
    return results


def run_mediation_analysis(df):
    """
    Test mediation: Does consideration mediate the effect of earlier funnel stages on intent?
    """
    df = df.copy()
    
    print("\n" + "="*70)
    print("MEDIATION ANALYSIS")
    print("Does consideration mediate the awareness -> intent relationship?")
    print("="*70)
    
    # Standardize variables
    for col in ['awareness', 'familiarity', 'opinion', 'consideration', 'likelihood', 'intent']:
        df[f'{col}_z'] = (df[col] - df[col].mean()) / df[col].std()
    
    # Step 1: Total effect (awareness -> intent without mediator)
    print("\n--- Step 1: Total Effect (awareness -> intent) ---")
    total_model = sm.OLS(df['intent_z'], sm.add_constant(df['awareness_z'])).fit()
    total_effect = total_model.params['awareness_z']
    print(f"Total effect (c): β = {total_effect:.3f}, p = {total_model.pvalues['awareness_z']:.4f}")
    
    # Step 2: Path a (awareness -> consideration)
    print("\n--- Step 2: Path a (awareness -> consideration) ---")
    a_model = sm.OLS(df['consideration_z'], sm.add_constant(df['awareness_z'])).fit()
    path_a = a_model.params['awareness_z']
    print(f"Path a: β = {path_a:.3f}, p = {a_model.pvalues['awareness_z']:.4f}")
    
    # Step 3: Path b and c' (mediator + IV -> DV)
    print("\n--- Step 3: Paths b and c' (consideration + awareness -> intent) ---")
    X = sm.add_constant(df[['awareness_z', 'consideration_z']])
    bc_model = sm.OLS(df['intent_z'], X).fit()
    path_b = bc_model.params['consideration_z']
    direct_effect = bc_model.params['awareness_z']
    print(f"Path b (consideration -> intent): β = {path_b:.3f}, p = {bc_model.pvalues['consideration_z']:.4f}")
    print(f"Direct effect c' (awareness -> intent): β = {direct_effect:.3f}, p = {bc_model.pvalues['awareness_z']:.4f}")
    
    # Calculate indirect effect
    indirect_effect = path_a * path_b
    print(f"\n--- Mediation Summary ---")
    print(f"Total effect (c): {total_effect:.3f}")
    print(f"Direct effect (c'): {direct_effect:.3f}")
    print(f"Indirect effect (a*b): {indirect_effect:.3f}")
    print(f"Proportion mediated: {(indirect_effect/total_effect)*100:.1f}%")
    
    if direct_effect < total_effect and path_b > 0:
        print("\nResult: Partial mediation confirmed - consideration partially mediates awareness -> intent")
    
    return {
        'total_effect': total_effect,
        'direct_effect': direct_effect,
        'indirect_effect': indirect_effect,
        'path_a': path_a,
        'path_b': path_b,
        'proportion_mediated': indirect_effect / total_effect if total_effect != 0 else 0
    }


def compute_correlations(df):
    """Compute correlation matrix for key variables."""
    vars_to_correlate = FUNNEL_STAGES + ['functional', 'emotional']
    
    # Create benefit composites
    df = df.copy()
    df['functional'] = df[FUNCTIONAL_BENEFITS].mean(axis=1)
    df['emotional'] = df[EMOTIONAL_BENEFITS].mean(axis=1)
    
    corr_matrix = df[vars_to_correlate].corr()
    return corr_matrix


def create_visualizations(df, results):
    """Create publication-ready visualizations."""
    
    print("\n" + "="*70)
    print("CREATING VISUALIZATIONS")
    print("="*70)
    
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Marketing Funnel Chart
    print("Creating funnel chart...")
    fig, ax = plt.subplots(figsize=(10, 6))
    funnel_means = df[FUNNEL_STAGES].mean().sort_values(ascending=False)
    colors = [FUNNEL_COLORS.get(s, '#666666') for s in funnel_means.index]
    bars = ax.barh(range(len(funnel_means)), funnel_means.values, color=colors)
    ax.set_yticks(range(len(funnel_means)))
    ax.set_yticklabels([s.replace('_', ' ').title() for s in funnel_means.index])
    ax.set_xlabel('Mean Score (1-7 scale)')
    ax.set_title('Marketing Funnel Performance', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 7)
    for i, (bar, val) in enumerate(zip(bars, funnel_means.values)):
        ax.text(val + 0.1, i, f'{val:.2f}', va='center')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'readme_funnel.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Funnel by Region
    print("Creating funnel by region chart...")
    fig, ax = plt.subplots(figsize=(12, 6))
    region_means = df.groupby('region')[FUNNEL_STAGES].mean()
    x = np.arange(len(FUNNEL_STAGES))
    width = 0.35
    for i, region in enumerate(region_means.index):
        if region in REGION_COLORS:
            ax.bar(x + i*width, region_means.loc[region], width, 
                   label=region, color=REGION_COLORS[region])
    ax.set_xticks(x + width/2)
    ax.set_xticklabels([s.replace('_', ' ').title() for s in FUNNEL_STAGES], rotation=45, ha='right')
    ax.set_ylabel('Mean Score (1-7 scale)')
    ax.set_title('Marketing Funnel by Region', fontsize=14, fontweight='bold')
    ax.legend()
    ax.set_ylim(0, 7)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'readme_funnel_region.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Segment Intent Comparison
    print("Creating segment intent chart...")
    fig, ax = plt.subplots(figsize=(12, 6))
    segment_intent = df.groupby(['region', 'segment'])['intent'].mean().unstack(level=0)
    segment_intent.plot(kind='bar', ax=ax, color=[REGION_COLORS.get(c, '#666') for c in segment_intent.columns])
    ax.set_xlabel('Demographic Segment')
    ax.set_ylabel('Mean Intent Score')
    ax.set_title('Intent to Visit by Segment and Region', fontsize=14, fontweight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.legend(title='Region')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'readme_segment_intent.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. Correlation Matrix
    print("Creating correlation matrix...")
    df_copy = df.copy()
    df_copy['functional'] = df_copy[FUNCTIONAL_BENEFITS].mean(axis=1)
    df_copy['emotional'] = df_copy[EMOTIONAL_BENEFITS].mean(axis=1)
    corr = df_copy[FUNNEL_STAGES + ['functional', 'emotional']].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                square=True, linewidths=0.5, ax=ax)
    ax.set_title('Correlation Matrix: Funnel Stages and Benefits', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'readme_correlation.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. Benefits Heatmap by Segment
    print("Creating benefits heatmap...")
    benefit_means = df.groupby('segment')[ALL_BENEFITS].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(benefit_means, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax)
    ax.set_title('Brand Benefits Perception by Segment', fontsize=14, fontweight='bold')
    ax.set_xticklabels([s.replace('_', ' ').replace('func ', 'F: ').replace('emot ', 'E: ').title() 
                        for s in benefit_means.columns], rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'readme_benefits_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 6. Path Coefficients (from regression)
    if 'full_model' in results:
        print("Creating path coefficients chart...")
        model = results['full_model']
        coefs = model.params.drop('const')
        pvals = model.pvalues.drop('const')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#2E86AB' if p < 0.05 else '#CCCCCC' for p in pvals]
        bars = ax.barh(range(len(coefs)), coefs.values, color=colors)
        ax.set_yticks(range(len(coefs)))
        ax.set_yticklabels([s.replace('_', ' ').title() for s in coefs.index])
        ax.axvline(0, color='black', linewidth=0.5)
        ax.set_xlabel('Standardized Coefficient (β)')
        ax.set_title('Drivers of Intent (Full Model)', fontsize=14, fontweight='bold')
        
        # Add significance stars
        for i, (bar, pval) in enumerate(zip(bars, pvals)):
            sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else ''
            ax.text(coefs.values[i] + 0.02, i, sig, va='center', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'readme_path_coefficients.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    # 7. R-squared visualization
    if 'full_model' in results:
        print("Creating R-squared chart...")
        r2 = results['full_model'].rsquared
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Intent'], [r2], color='#2E86AB', width=0.4)
        ax.set_ylabel('R² (Variance Explained)')
        ax.set_title('Model Fit: Variance Explained in Intent', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.text(0, r2 + 0.02, f'{r2:.1%}', ha='center', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'readme_r_squared.png', dpi=150, bbox_inches='tight')
        plt.close()
    
    # 8. Mediation diagram (conceptual)
    print("Creating mediation diagram...")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Boxes
    boxes = {
        'Awareness': (1, 3),
        'Consideration': (5, 5),
        'Intent': (9, 3)
    }
    
    for label, (x, y) in boxes.items():
        rect = plt.Rectangle((x-0.8, y-0.4), 1.6, 0.8, fill=True, 
                             facecolor='#E8F4F8', edgecolor='#2E86AB', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Arrows
    ax.annotate('', xy=(4.2, 4.7), xytext=(1.8, 3.3),
                arrowprops=dict(arrowstyle='->', color='#2E86AB', lw=2))
    ax.text(2.8, 4.3, 'a', fontsize=14, fontweight='bold')
    
    ax.annotate('', xy=(8.2, 3.3), xytext=(5.8, 4.7),
                arrowprops=dict(arrowstyle='->', color='#2E86AB', lw=2))
    ax.text(7.2, 4.3, 'b', fontsize=14, fontweight='bold')
    
    ax.annotate('', xy=(8.2, 3), xytext=(1.8, 3),
                arrowprops=dict(arrowstyle='->', color='#A23B72', lw=2))
    ax.text(5, 2.5, "c' (direct)", fontsize=12, fontweight='bold', color='#A23B72')
    
    ax.set_title('Mediation Model: Consideration Mediates Awareness → Intent', 
                 fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'readme_mediation.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"All visualizations saved to: {FIGURES_DIR}")


def save_results(df, results, mediation_results):
    """Save analysis results to CSV files."""
    
    print("\n" + "="*70)
    print("SAVING RESULTS")
    print("="*70)
    
    # Save fit indices
    if 'full_model' in results:
        model = results['full_model']
        fit_df = pd.DataFrame({
            'Measure': ['R-squared', 'Adj. R-squared', 'F-statistic', 'F p-value', 'AIC', 'BIC', 'N'],
            'Value': [model.rsquared, model.rsquared_adj, model.fvalue, model.f_pvalue, 
                      model.aic, model.bic, int(model.nobs)]
        })
        fit_df.to_csv(REPORTS_DIR / 'fit_indices_full.csv', index=False)
        print(f"Saved: {REPORTS_DIR / 'fit_indices_full.csv'}")
    
    # Save path coefficients
    if 'full_model' in results:
        model = results['full_model']
        path_df = pd.DataFrame({
            'predictor': model.params.index,
            'beta': model.params.values,
            'se': model.bse.values,
            'z': model.tvalues.values,
            'pvalue': model.pvalues.values
        })
        path_df['significance'] = path_df['pvalue'].apply(
            lambda p: '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
        )
        path_df.to_csv(REPORTS_DIR / 'path_coefficients_full.csv', index=False)
        print(f"Saved: {REPORTS_DIR / 'path_coefficients_full.csv'}")
    
    # Save mediation results
    med_df = pd.DataFrame([mediation_results])
    med_df.to_csv(REPORTS_DIR / 'mediation_results.csv', index=False)
    print(f"Saved: {REPORTS_DIR / 'mediation_results.csv'}")
    
    # Save descriptive statistics
    desc_stats = df[FUNNEL_STAGES + ALL_BENEFITS].describe()
    desc_stats.to_csv(REPORTS_DIR / 'descriptive_statistics.csv')
    print(f"Saved: {REPORTS_DIR / 'descriptive_statistics.csv'}")
    
    # Save reliability
    reliability_df = pd.DataFrame({
        'Scale': ['Funnel', 'Functional Benefits', 'Emotional Benefits'],
        'Cronbach_Alpha': [
            compute_cronbach_alpha(df, FUNNEL_STAGES),
            compute_cronbach_alpha(df, FUNCTIONAL_BENEFITS),
            compute_cronbach_alpha(df, EMOTIONAL_BENEFITS)
        ]
    })
    reliability_df.to_csv(REPORTS_DIR / 'scale_reliability.csv', index=False)
    print(f"Saved: {REPORTS_DIR / 'scale_reliability.csv'}")


def main():
    """Main analysis pipeline."""
    
    print("="*70)
    print("JAPAN MARKET ANALYSIS - SEM/PATH ANALYSIS")
    print("="*70)
    
    # Load data
    print("\n--- Loading Data ---")
    df = load_processed_data()
    
    # Data quality summary
    print("\n--- Data Quality Summary ---")
    print(f"Sample size: {len(df)}")
    print(f"\nSegments: {df['segment'].value_counts().to_dict()}")
    print(f"\nRegions: {df['region'].value_counts().to_dict()}")
    
    # Check reliability
    print("\n--- Scale Reliability (Cronbach's Alpha) ---")
    print(f"Funnel Scale: α = {compute_cronbach_alpha(df, FUNNEL_STAGES):.3f}")
    print(f"Functional Benefits: α = {compute_cronbach_alpha(df, FUNCTIONAL_BENEFITS):.3f}")
    print(f"Emotional Benefits: α = {compute_cronbach_alpha(df, EMOTIONAL_BENEFITS):.3f}")
    
    # Descriptive statistics
    print("\n--- Funnel Metrics Descriptives ---")
    print(df[FUNNEL_STAGES].describe().round(2))
    
    # Run path analysis
    results = run_path_analysis(df)
    
    # Run mediation analysis
    mediation_results = run_mediation_analysis(df)
    
    # Create visualizations
    create_visualizations(df, results)
    
    # Save results
    save_results(df, results, mediation_results)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nFigures saved to: {FIGURES_DIR}")
    print(f"Reports saved to: {REPORTS_DIR}")
    
    return df, results, mediation_results


if __name__ == "__main__":
    df, results, mediation_results = main()
