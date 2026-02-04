# TDL Brand Benefit Analysis: Full SEM Model

A comprehensive analysis combining the **Marketing Funnel** path model with **Brand Benefit Factors** to understand what drives visit intent for Tokyo Disneyland (TDL).

---

## Overview

| Metric | Value |
|--------|-------|
| **Sample Size** | n = 1,101 respondents with complete data |
| **Time Period** | 6 months (February - July) |
| **Funnel Metrics** | Familiarity, Opinion, Consideration, Likelihood |
| **Benefit Attributes** | 36 (26 functional + 10 emotional) |
| **Benefit Factors** | 4 data-driven dimensions |

---

## Full SEM Model Results

### Model Architecture

```
                    ┌─────────────────────────────────────────┐
                    │        MARKETING FUNNEL                 │
                    │                                          │
                    │  Familiarity ──(0.65)──► Consideration   │
                    │                               │          │
                    │                         (0.62)           │
                    │                               ▼          │
                    │  Familiarity ──(0.11)──► LIKELIHOOD      │
                    │                               ▲          │
                    └───────────────────────────────┼──────────┘
                                                    │
                    ┌───────────────────────────────┼──────────┐
                    │        BENEFIT FACTORS        │          │
                    │                               │          │
                    │  Family Bonding ──(0.17)──────┤          │
                    │  Value & Access ──(0.07)──────┤          │
                    │  Innovation ──(ns)────────────┤          │
                    │  Affordability ──(ns)─────────┘          │
                    │                                          │
                    └──────────────────────────────────────────┘
```

---

## Marketing Funnel Path Coefficients

Path analysis showing how funnel stages relate to each other:

| Path | Standardized β | p-value | Significance |
|------|----------------|---------|--------------|
| Familiarity → Consideration | **0.647** | < 0.001 | *** |
| Opinion → Consideration | 0.038 | 0.105 | ns |

**Key Finding**: Familiarity has a very strong direct effect on Consideration (β = 0.647), while Opinion's effect is not significant in this sample. This suggests brand familiarity is the primary driver of getting TDL into consumers' consideration sets.

---

## Full Model: Funnel + Benefit Factors → Likelihood

All predictors of Likelihood to Visit in a single model:

| Predictor | Standardized β | p-value | Significance | Interpretation |
|-----------|----------------|---------|--------------|----------------|
| **Consideration** | **0.617** | < 0.001 | *** | Strongest funnel driver |
| **Family Bonding** | **0.167** | < 0.001 | *** | Strongest benefit factor |
| Familiarity | 0.106 | < 0.001 | *** | Direct effect on Likelihood |
| **Value & Access** | **0.069** | < 0.001 | *** | Significant benefit factor |
| Opinion | 0.027 | 0.119 | ns | Not significant when controlling for others |
| Innovation & Thrills | -0.025 | 0.152 | ns | Not significant |
| Affordability | 0.017 | 0.314 | ns | Not significant |

### Interpretation

**Funnel Effects:**
- **Consideration** (β = 0.617) is the strongest predictor overall - once someone is considering TDL, they're very likely to intend to visit
- **Familiarity** (β = 0.106) has a significant direct effect beyond its influence through Consideration

**Benefit Factor Effects:**
- **Family Bonding** (β = 0.167) is the strongest benefit factor - perceptions of family experience, memories, and bonding drive visit intent
- **Value & Access** (β = 0.069) is also significant - perceptions of affordability and accessibility matter
- Innovation & Thrills and standalone Affordability factors are not significant when controlling for funnel metrics

---

## Model Fit & Comparison

| Metric | Funnel Only | Full Model (Funnel + Benefits) |
|--------|-------------|--------------------------------|
| **R²** | 0.659 | **0.677** |
| **Adjusted R²** | 0.658 | **0.675** |
| **AIC** | 2039.2 | **1987.4** (lower is better) |
| **BIC** | 2059.2 | **2027.5** (lower is better) |

**Model Improvement:**
- R² improvement: **+0.018** (1.8 percentage points)
- F-test: F(4, 1093) = 15.24, **p < 0.001**
- **Conclusion**: Adding benefit factors significantly improves model fit

---

## Segment Analysis

Path coefficients by demographic segment:

| Segment | n | R² | Consideration → Likelihood |
|---------|---|-----|---------------------------|
| E. Adults 35+ (no kids in HH) | 221 | **0.760** | **0.685** |
| D. Couples 18-34 (no kids in HH) | 220 | **0.700** | **0.645** |
| A. Young Families | 220 | 0.690 | 0.613 |
| C. Adults 18-34 (no kids in HH) | 220 | 0.651 | 0.476 |
| B. Older Families | 220 | 0.624 | 0.582 |

**Key Findings:**
- **Adults 35+** has highest model R² (0.760) and strongest Consideration → Likelihood path (0.685)
- **Adults 18-34 (no kids)** has weakest conversion from Consideration to Likelihood (0.476)
- All segments show Consideration as a significant predictor

---

## Benefit Factor Details

### Factor 1: Family Bonding (β = 0.167***)

**The strongest benefit factor driving visit intent.**

| Attribute | Factor Loading |
|-----------|---------------|
| Feel Good | High |
| Lifelong Memories | High |
| Great For Adults | High |
| Bond Family Friends | High |
| Enjoy Myself | High |

This factor captures the core emotional experience of visiting TDL - creating memories, bonding with loved ones, and having a feel-good experience.

### Factor 2: Value & Access (β = 0.069***)

**Significant but moderate effect on visit intent.**

| Attribute | Factor Loading |
|-----------|---------------|
| Affordable | High |
| Not Crowded | High |
| Relaxing | Moderate |

This factor combines value perception with accessibility concerns. Despite low ratings on affordability (2.31/5) and crowding (2.12/5), improvements in these perceptions do increase visit intent.

### Factor 3: Innovation & Thrills (β = -0.025, ns)

| Attribute | Factor Loading |
|-----------|---------------|
| Active Adventurous | High |
| Thrilling | High |
| New Innovative | High |

Not a significant predictor when controlling for funnel metrics and other factors.

### Factor 4: Affordability (β = 0.017, ns)

Contains kids experience and relaxation attributes. Not significant in the full model.

---

## Key Strategic Insights

### 1. Consideration is the Critical Conversion Point

With β = 0.617, getting consumers to actively consider TDL is the most important factor. Focus on moving people from "aware" to "considering."

### 2. Family Bonding Benefits Drive Decisions

The strongest benefit factor (β = 0.167) emphasizes:
- Creating memories together
- Bonding with family/friends
- Feel-good experiences
- Experiences adults enjoy too

**Implication**: Marketing should emphasize emotional connection and shared experiences, not just kid-focused messaging.

### 3. Value Perceptions Matter (But Aren't Dealbreakers)

Value & Access (β = 0.069) is significant, but:
- Current ratings are low (Affordable: 2.31, Not Crowded: 2.12)
- Effect size is smaller than Family Bonding
- People visit despite knowing it's expensive and crowded

**Implication**: Value messaging helps, but emotional benefits are more powerful drivers.

### 4. Innovation/Thrills Don't Differentiate

Innovation & Thrills factor is not significant. This may mean:
- TDL is not positioned as a thrill-seeking destination
- Visitors come for the experience, not the rides
- USJ may own this positioning more strongly

### 5. Segment-Specific Strategies

| Segment | Strategy Focus |
|---------|---------------|
| Adults 35+ | High conversion once considering - focus on getting them to consider |
| Adults 18-34 | Weakest conversion - may need different value proposition |
| Couples 18-34 | Strong performers - maintain relationship, upsell |
| Young Families | Core segment - reinforce family messaging |
| Older Families | Lower conversion - research specific barriers |

---

## Technical Details

### Factor Analysis

- **Method**: Sklearn FactorAnalysis with varimax rotation
- **Factors**: 4 (based on Kaiser criterion)
- **KMO**: 0.985 (Excellent)
- **Bartlett's Test**: χ² = 32,895, p < 0.001

### Why Factor Analysis over Clustering

Initial clustering had silhouette score of 0.163 (poor cluster separation). Factor Analysis is more appropriate because:
1. Brand perceptions are **correlated dimensions**, not distinct groups
2. Attributes can load on **multiple factors**
3. Better suited for Likert-scale perception data

### Regression Model

- **Method**: OLS with standardized coefficients
- **Dependent Variable**: Likelihood to Visit (1-5 scale)
- **Sample**: n = 1,101 with complete funnel and benefit data

---

## Files Generated

| File | Description |
|------|-------------|
| `output/reports/sem_full_model_results.csv` | Full model coefficients |
| `output/reports/sem_model_comparison.csv` | Funnel vs Full model comparison |
| `output/reports/sem_segment_results.csv` | Segment-level analysis |
| `output/reports/factor_loadings.csv` | Factor loadings for all attributes |

---

## Running the Analysis

```bash
cd japan_market_analysis

# Run full SEM model with benefits
python3 src/full_sem_with_benefits.py

# Run factor analysis only
python3 src/brand_benefit_factor_analysis.py

# Run clustering analysis (for comparison)
python3 src/brand_benefit_cluster_analysis.py
```

**Requirements**: pandas, numpy, scikit-learn, scipy, statsmodels

---

*Analysis completed using 6 months of TDL Brand Tracking Survey data (n = 1,101)*
