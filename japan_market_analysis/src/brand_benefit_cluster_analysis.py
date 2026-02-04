#!/usr/bin/env python3
"""
Brand Benefit Cluster Analysis
Clusters brand benefits based on data patterns rather than predefined categories.
Uses 6 months of TDL survey data.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.stats import pearsonr, spearmanr
import statsmodels.api as sm
import warnings
import os
import json

warnings.filterwarnings('ignore')

# Output directories
OUTPUT_DIR = 'output/reports'
FIGURES_DIR = 'output/figures'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 70)
print("  BRAND BENEFIT CLUSTER ANALYSIS - 6 MONTH DATA")
print("=" * 70)
print()

# ============================================================================
# Load Data
# ============================================================================

print("Loading TDL survey data...")
df = pd.read_csv('dbt_project/seeds/survey_responses_tdl.csv')
print(f"Total records: {len(df)}")
print(f"Months in data: {df['month'].unique()}")

# Define brand benefit columns
func_cols = [col for col in df.columns if col.startswith('tdl_func_')]
emot_cols = [col for col in df.columns if col.startswith('tdl_emot_')]
all_benefit_cols = func_cols + emot_cols

print(f"\nFunctional attributes: {len(func_cols)}")
print(f"Emotional attributes: {len(emot_cols)}")
print(f"Total brand benefit attributes: {len(all_benefit_cols)}")

# ============================================================================
# Data Preparation
# ============================================================================

print("\n" + "-" * 50)
print("DATA PREPARATION")
print("-" * 50)

# Clean benefit data - replace 0 with NaN (missing values)
benefit_df = df[all_benefit_cols].replace(0, np.nan)

# Create analysis dataset with key variables
analysis_df = df[['respondent_id', 'wave', 'month', 'audience', 'geography',
                   'familiarity_tdl', 'opinion_tdl', 'consideration_tdl', 
                   'likelihood_visit_tdl', 'nps_tdl']].copy()

# Convert to numeric
for col in ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl', 
            'likelihood_visit_tdl', 'nps_tdl']:
    analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')

# Add benefit columns
for col in all_benefit_cols:
    analysis_df[col] = pd.to_numeric(benefit_df[col], errors='coerce')

# Filter to respondents with brand benefit data (non-zero values)
benefit_mask = analysis_df[all_benefit_cols].notna().any(axis=1)
has_all_benefits = (analysis_df[all_benefit_cols] > 0).any(axis=1)
analysis_subset = analysis_df[has_all_benefits].copy()

print(f"Respondents with brand benefit data: {len(analysis_subset)}")

# Get complete cases for clustering
clustering_data = analysis_subset[all_benefit_cols].dropna()
valid_indices = clustering_data.index
analysis_complete = analysis_subset.loc[valid_indices].copy()

print(f"Complete cases for analysis: {len(analysis_complete)}")

# ============================================================================
# Attribute-Level Clustering (Cluster the attributes, not the respondents)
# ============================================================================

print("\n" + "-" * 50)
print("CLUSTERING BRAND BENEFIT ATTRIBUTES")
print("-" * 50)

# Calculate correlation matrix of attributes
benefit_corr = analysis_complete[all_benefit_cols].corr()

# Try multiple clustering approaches and select the best

# Approach 1: Hierarchical clustering on correlation distance
distance_matrix = 1 - benefit_corr
linkage_matrix = linkage(distance_matrix, method='average')  # average linkage for correlation

# Approach 2: K-Means on transposed data (cluster attributes based on response patterns)
# Transpose: rows = attributes, columns = respondents
attr_data_T = analysis_complete[all_benefit_cols].T.values
scaler = StandardScaler()
attr_data_scaled = scaler.fit_transform(attr_data_T)

# Use K-Means for more balanced clustering
print("\nUsing K-Means clustering on attribute response patterns...")
print("Evaluating cluster solutions:")

# Use PCA for dimensionality reduction before clustering
pca = PCA(n_components=min(10, len(attr_data_scaled[0])))
attr_pca = pca.fit_transform(attr_data_scaled)
print(f"  PCA variance explained: {sum(pca.explained_variance_ratio_[:5]):.1%} (first 5 components)")

silhouette_scores = {}
cluster_solutions = {}

for n_clusters in range(3, 8):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(attr_pca)
    
    score = silhouette_score(attr_pca, cluster_labels)
    silhouette_scores[n_clusters] = score
    cluster_solutions[n_clusters] = cluster_labels
    
    # Check cluster sizes
    unique, counts = np.unique(cluster_labels, return_counts=True)
    min_size = counts.min()
    max_size = counts.max()
    
    print(f"  {n_clusters} clusters: silhouette = {score:.3f}, "
          f"sizes = {dict(zip(unique + 1, counts))}")

# Choose 4-5 clusters for marketing actionability
# Higher is better for actionable insights, balanced with silhouette
best_score = -1
optimal_n_clusters = 4

for n in [4, 5, 6]:
    labels = cluster_solutions[n]
    unique, counts = np.unique(labels, return_counts=True)
    min_size = counts.min()
    
    # Combined score favoring balanced clusters with at least 3 attributes each
    if min_size >= 3:
        combined_score = silhouette_scores[n] * (min_size / 5)
        if combined_score > best_score:
            best_score = combined_score
            optimal_n_clusters = n

# If no solution has min_size >= 3, default to 4
if best_score == -1:
    optimal_n_clusters = 5  # Use 5 for more granularity

print(f"\nSelected number of clusters: {optimal_n_clusters}")

# Get final cluster labels (0-indexed, convert to 1-indexed)
final_cluster_labels = cluster_solutions[optimal_n_clusters] + 1

# Final cluster labels already obtained from K-Means above

# Create attribute-to-cluster mapping
attribute_clusters = pd.DataFrame({
    'attribute': all_benefit_cols,
    'cluster': final_cluster_labels,
    'original_category': ['Functional' if 'func' in col else 'Emotional' for col in all_benefit_cols]
})

# Clean attribute names for display
attribute_clusters['attribute_clean'] = attribute_clusters['attribute'].str.replace('tdl_func_', '').str.replace('tdl_emot_', '').str.replace('_', ' ').str.title()

print("\n" + "=" * 70)
print("  CLUSTER COMPOSITION")
print("=" * 70)

# Analyze each cluster
cluster_analysis = {}
for cluster_id in range(1, optimal_n_clusters + 1):
    cluster_attrs = attribute_clusters[attribute_clusters['cluster'] == cluster_id]
    
    # Calculate mean ratings for this cluster's attributes
    cluster_attr_names = cluster_attrs['attribute'].tolist()
    mean_ratings = analysis_complete[cluster_attr_names].mean()
    
    cluster_analysis[cluster_id] = {
        'n_attributes': len(cluster_attrs),
        'attributes': cluster_attrs['attribute_clean'].tolist(),
        'n_functional': (cluster_attrs['original_category'] == 'Functional').sum(),
        'n_emotional': (cluster_attrs['original_category'] == 'Emotional').sum(),
        'mean_rating': mean_ratings.mean(),
        'min_rating': mean_ratings.min(),
        'max_rating': mean_ratings.max()
    }
    
    print(f"\n### CLUSTER {cluster_id}: {len(cluster_attrs)} attributes")
    print(f"    Composition: {cluster_analysis[cluster_id]['n_functional']} functional, "
          f"{cluster_analysis[cluster_id]['n_emotional']} emotional")
    print(f"    Mean rating: {cluster_analysis[cluster_id]['mean_rating']:.2f}")
    print(f"    Attributes:")
    for attr in cluster_attrs['attribute_clean'].values:
        rating = mean_ratings[cluster_attrs[cluster_attrs['attribute_clean'] == attr]['attribute'].values[0]]
        print(f"      - {attr} ({rating:.2f})")

# ============================================================================
# Name the Clusters Based on Content
# ============================================================================

print("\n" + "-" * 50)
print("CLUSTER NAMING (Based on Thematic Analysis)")
print("-" * 50)

# Analyze cluster content to determine themes - more sophisticated naming
cluster_names = {}
used_names = set()

for cluster_id in range(1, optimal_n_clusters + 1):
    attrs = cluster_analysis[cluster_id]['attributes']
    attrs_lower = [a.lower() for a in attrs]
    attrs_text = ' '.join(attrs_lower)
    n_attrs = len(attrs)
    
    # Theme detection based on attribute content - prioritized matching
    name = None
    
    # Single attribute clusters get specific names
    if n_attrs == 1:
        if 'affordable' in attrs_text:
            name = "Affordability"
        elif 'crowded' in attrs_text:
            name = "Crowd Management"
        else:
            name = attrs[0]
    # Multi-attribute clusters - check dominant themes
    elif 'dreams' in attrs_text or 'fantasy' in attrs_text or 'fantastical' in attrs_text:
        if 'sparkling' in attrs_text or 'premium' in attrs_text:
            name = "Magic & Enchantment"
        else:
            name = "Fantasy & Escape"
    elif ('kids' in attrs_text or 'child' in attrs_text) and 'family' in attrs_text:
        name = "Family & Kids Appeal"
    elif 'family' in attrs_text or 'bond' in attrs_text:
        name = "Family Bonding"
    elif 'repeat' in attrs_text and ('innovative' in attrs_text or 'new' in attrs_text):
        name = "Experience & Innovation"
    elif 'thrilling' in attrs_text and 'adventurous' in attrs_text:
        name = "Thrills & Adventure"
    elif 'innovative' in attrs_text or ('new' in attrs_text and 'something' in attrs_text):
        if 'worth' in attrs_text or 'price' in attrs_text:
            name = "Experience Value"
        else:
            name = "Innovation & Novelty"
    elif 'comfortable' in attrs_text or 'relaxing' in attrs_text:
        if 'repeat' in attrs_text or 'worth' in attrs_text:
            name = "Experience Quality"
        else:
            name = "Comfort & Relaxation"
    elif 'worth' in attrs_text or 'price' in attrs_text or 'ticket' in attrs_text:
        name = "Value & Practicality"
    elif 'unique' in attrs_text or 'character' in attrs_text:
        name = "Unique Experiences"
    elif 'memories' in attrs_text or 'enjoy' in attrs_text:
        name = "Core Experience"
    elif 'adults' in attrs_text:
        name = "Adult Appeal"
    else:
        name = f"Experience Cluster {cluster_id}"
    
    # Ensure unique names
    original_name = name
    counter = 2
    while name in used_names:
        name = f"{original_name} {counter}"
        counter += 1
    
    used_names.add(name)
    cluster_names[cluster_id] = name
    print(f"Cluster {cluster_id}: {name}")

# ============================================================================
# Create Cluster Composite Scores
# ============================================================================

print("\n" + "-" * 50)
print("CREATING CLUSTER COMPOSITE SCORES")
print("-" * 50)

for cluster_id in range(1, optimal_n_clusters + 1):
    cluster_attrs = attribute_clusters[attribute_clusters['cluster'] == cluster_id]['attribute'].tolist()
    col_name = f'cluster_{cluster_id}_score'
    analysis_complete[col_name] = analysis_complete[cluster_attrs].mean(axis=1)
    print(f"  {cluster_names[cluster_id]}: mean = {analysis_complete[col_name].mean():.2f}, "
          f"std = {analysis_complete[col_name].std():.2f}")

# ============================================================================
# Regression Analysis: Impact on Likelihood to Visit
# ============================================================================

print("\n" + "=" * 70)
print("  REGRESSION: CLUSTER IMPACT ON LIKELIHOOD TO VISIT")
print("=" * 70)

# Prepare regression data
cluster_score_cols = [f'cluster_{i}_score' for i in range(1, optimal_n_clusters + 1)]
funnel_cols = ['familiarity_tdl', 'opinion_tdl', 'consideration_tdl']

# Filter to complete cases
reg_cols = ['likelihood_visit_tdl'] + funnel_cols + cluster_score_cols
reg_data = analysis_complete[reg_cols].dropna()

print(f"\nRegression sample size: {len(reg_data)}")

# Model 1: Funnel only
X_funnel = sm.add_constant(reg_data[funnel_cols])
y = reg_data['likelihood_visit_tdl']
model_funnel = sm.OLS(y, X_funnel).fit()

print("\n--- Model 1: Funnel Metrics Only ---")
print(f"R-squared: {model_funnel.rsquared:.3f}")
print(f"Adj R-squared: {model_funnel.rsquared_adj:.3f}")

# Model 2: Funnel + Benefit Clusters
X_full = sm.add_constant(reg_data[funnel_cols + cluster_score_cols])
model_full = sm.OLS(y, X_full).fit()

print("\n--- Model 2: Funnel + Benefit Clusters ---")
print(f"R-squared: {model_full.rsquared:.3f}")
print(f"Adj R-squared: {model_full.rsquared_adj:.3f}")
print(f"R-squared improvement: +{model_full.rsquared - model_funnel.rsquared:.3f}")

# Standardized coefficients for comparison
def get_standardized_coefs(model, X_data, y_data):
    """Calculate standardized regression coefficients."""
    coefs = model.params[1:]  # Exclude intercept
    X_std = X_data.iloc[:, 1:].std()  # Exclude constant
    y_std = y_data.std()
    return (coefs * X_std) / y_std

std_coefs = get_standardized_coefs(model_full, X_full, y)

print("\n--- Standardized Coefficients (Full Model) ---")
coef_results = []
for var in funnel_cols + cluster_score_cols:
    coef = model_full.params[var]
    std_coef = std_coefs[var]
    pval = model_full.pvalues[var]
    sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else ''
    
    if var.startswith('cluster_'):
        cluster_id = int(var.split('_')[1])
        var_name = cluster_names[cluster_id]
    else:
        var_name = var.replace('_tdl', '').title()
    
    print(f"  {var_name}: β = {std_coef:.3f} (p = {pval:.3f}) {sig}")
    coef_results.append({
        'predictor': var_name,
        'raw_coef': coef,
        'std_coef': std_coef,
        'p_value': pval,
        'significant': sig
    })

# ============================================================================
# Identify Most Impactful Clusters
# ============================================================================

print("\n" + "-" * 50)
print("IMPACT RANKING OF BENEFIT CLUSTERS")
print("-" * 50)

cluster_impact = []
for cluster_id in range(1, optimal_n_clusters + 1):
    col_name = f'cluster_{cluster_id}_score'
    std_coef = std_coefs[col_name]
    pval = model_full.pvalues[col_name]
    mean_score = reg_data[col_name].mean()
    
    cluster_impact.append({
        'cluster_id': cluster_id,
        'cluster_name': cluster_names[cluster_id],
        'std_coef': std_coef,
        'p_value': pval,
        'mean_score': mean_score,
        'significant': pval < 0.05,
        'n_attributes': cluster_analysis[cluster_id]['n_attributes']
    })

cluster_impact_df = pd.DataFrame(cluster_impact)
cluster_impact_df = cluster_impact_df.sort_values('std_coef', ascending=False)

print("\nCluster ranking by impact on Likelihood to Visit:")
for i, row in cluster_impact_df.iterrows():
    sig = '***' if row['p_value'] < 0.001 else '**' if row['p_value'] < 0.01 else '*' if row['p_value'] < 0.05 else 'ns'
    print(f"  {row['cluster_name']:25s}: β = {row['std_coef']:+.3f} ({sig}), "
          f"Mean Score = {row['mean_score']:.2f}, Attrs = {row['n_attributes']}")

# ============================================================================
# Attribute-Level Analysis Within Clusters
# ============================================================================

print("\n" + "=" * 70)
print("  DETAILED ATTRIBUTE ANALYSIS BY CLUSTER")
print("=" * 70)

attribute_details = []
for cluster_id in range(1, optimal_n_clusters + 1):
    cluster_attrs = attribute_clusters[attribute_clusters['cluster'] == cluster_id]
    
    print(f"\n### {cluster_names[cluster_id]} (Cluster {cluster_id})")
    print("-" * 40)
    
    for _, attr_row in cluster_attrs.iterrows():
        attr = attr_row['attribute']
        attr_clean = attr_row['attribute_clean']
        
        # Calculate correlation with likelihood
        valid_data = analysis_complete[[attr, 'likelihood_visit_tdl']].dropna()
        if len(valid_data) > 30:
            corr, pval = pearsonr(valid_data[attr], valid_data['likelihood_visit_tdl'])
        else:
            corr, pval = np.nan, np.nan
        
        mean_score = analysis_complete[attr].mean()
        
        sig = '***' if pval < 0.001 else '**' if pval < 0.01 else '*' if pval < 0.05 else ''
        
        print(f"  {attr_clean:35s}: Mean = {mean_score:.2f}, Corr with Likelihood = {corr:.2f} {sig}")
        
        attribute_details.append({
            'cluster_id': cluster_id,
            'cluster_name': cluster_names[cluster_id],
            'attribute': attr_clean,
            'original_category': attr_row['original_category'],
            'mean_score': mean_score,
            'correlation_likelihood': corr,
            'correlation_pvalue': pval
        })

# ============================================================================
# Segment Analysis
# ============================================================================

print("\n" + "=" * 70)
print("  CLUSTER SCORES BY SEGMENT")
print("=" * 70)

segment_cluster_scores = analysis_complete.groupby('audience')[cluster_score_cols].mean()
segment_cluster_scores.columns = [cluster_names[int(col.split('_')[1])] for col in cluster_score_cols]

print("\nMean cluster scores by segment:")
print(segment_cluster_scores.round(2))

# ============================================================================
# Save Results
# ============================================================================

print("\n" + "-" * 50)
print("SAVING RESULTS")
print("-" * 50)

# Save attribute clustering results
attribute_results = attribute_clusters.copy()
attribute_results['cluster_name'] = attribute_results['cluster'].map(cluster_names)
attribute_results.to_csv(f'{OUTPUT_DIR}/benefit_cluster_assignments.csv', index=False)
print(f"  Saved: benefit_cluster_assignments.csv")

# Save cluster impact analysis
cluster_impact_df.to_csv(f'{OUTPUT_DIR}/benefit_cluster_impact.csv', index=False)
print(f"  Saved: benefit_cluster_impact.csv")

# Save attribute-level details
attribute_details_df = pd.DataFrame(attribute_details)
attribute_details_df.to_csv(f'{OUTPUT_DIR}/benefit_attribute_details.csv', index=False)
print(f"  Saved: benefit_attribute_details.csv")

# Save segment cluster scores
segment_cluster_scores.to_csv(f'{OUTPUT_DIR}/segment_cluster_scores.csv')
print(f"  Saved: segment_cluster_scores.csv")

# Save regression coefficients
coef_df = pd.DataFrame(coef_results)
coef_df.to_csv(f'{OUTPUT_DIR}/benefit_regression_coefficients.csv', index=False)
print(f"  Saved: benefit_regression_coefficients.csv")

# ============================================================================
# Generate Summary for README
# ============================================================================

print("\n" + "=" * 70)
print("  GENERATING README CONTENT")
print("=" * 70)

readme_data = {
    'n_respondents': len(analysis_complete),
    'n_months': df['month'].nunique(),
    'months': df['month'].unique().tolist(),
    'n_clusters': optimal_n_clusters,
    'clusters': {},
    'model_r_squared_funnel': model_funnel.rsquared,
    'model_r_squared_full': model_full.rsquared,
    'r_squared_improvement': model_full.rsquared - model_funnel.rsquared
}

for cluster_id in range(1, optimal_n_clusters + 1):
    cluster_attrs = attribute_clusters[attribute_clusters['cluster'] == cluster_id]
    cluster_name = cluster_names[cluster_id]
    
    # Get impact data
    impact_row = cluster_impact_df[cluster_impact_df['cluster_id'] == cluster_id].iloc[0]
    
    # Get attribute details for this cluster
    cluster_attr_details = attribute_details_df[attribute_details_df['cluster_id'] == cluster_id]
    top_attrs = cluster_attr_details.nlargest(5, 'mean_score')[['attribute', 'mean_score']].to_dict('records')
    
    readme_data['clusters'][cluster_name] = {
        'n_attributes': int(impact_row['n_attributes']),
        'std_coef': float(impact_row['std_coef']),
        'p_value': float(impact_row['p_value']),
        'mean_score': float(impact_row['mean_score']),
        'significant': bool(impact_row['significant']),
        'top_attributes': top_attrs
    }

# Save README data as JSON for processing
with open(f'{OUTPUT_DIR}/readme_data.json', 'w') as f:
    json.dump(readme_data, f, indent=2, default=str)
print(f"  Saved: readme_data.json")

# ============================================================================
# Final Summary
# ============================================================================

print("\n" + "=" * 70)
print("  EXECUTIVE SUMMARY")
print("=" * 70)

print(f"""
BRAND BENEFIT CLUSTER ANALYSIS RESULTS
======================================

Sample: {len(analysis_complete)} respondents across {df['month'].nunique()} months
        ({', '.join(df['month'].unique())})

Total Attributes Analyzed: {len(all_benefit_cols)}
  - Original Functional: {len(func_cols)}
  - Original Emotional: {len(emot_cols)}

DATA-DRIVEN CLUSTERS IDENTIFIED: {optimal_n_clusters}
""")

for cluster_id in range(1, optimal_n_clusters + 1):
    name = cluster_names[cluster_id]
    info = cluster_analysis[cluster_id]
    impact = cluster_impact_df[cluster_impact_df['cluster_id'] == cluster_id].iloc[0]
    sig = '***' if impact['p_value'] < 0.001 else '**' if impact['p_value'] < 0.01 else '*' if impact['p_value'] < 0.05 else 'ns'
    
    print(f"  {cluster_id}. {name}")
    print(f"     - {info['n_attributes']} attributes ({info['n_functional']} functional, {info['n_emotional']} emotional)")
    print(f"     - Mean Rating: {info['mean_rating']:.2f}")
    print(f"     - Impact on Likelihood: β = {impact['std_coef']:.3f} ({sig})")
    print()

print(f"""
MODEL PERFORMANCE:
  Funnel Only R²: {model_funnel.rsquared:.3f}
  Funnel + Clusters R²: {model_full.rsquared:.3f}
  Improvement: +{model_full.rsquared - model_funnel.rsquared:.3f}

KEY INSIGHT:
The data-driven clustering reveals that brand benefits naturally group into
{optimal_n_clusters} distinct themes, which may differ from the traditional
Functional/Emotional categorization. This provides more nuanced strategic
insights for marketing communications.
""")

print("\n" + "=" * 70)
print("  ANALYSIS COMPLETE")
print("=" * 70)
