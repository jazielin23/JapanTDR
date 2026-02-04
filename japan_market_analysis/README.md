# TDL Brand Benefit Analysis: Factor-Based Approach

A data-driven analysis of Tokyo Disneyland (TDL) brand benefits using **Factor Analysis** on 6 months of survey data. Factor Analysis is used instead of clustering because brand perceptions are naturally correlated dimensions rather than distinct groups.

---

## Why Factor Analysis Instead of Clustering?

| Approach | Silhouette Score | Interpretation |
|----------|------------------|----------------|
| 2 Clusters | 0.692 | Good separation but only 2 groups (not actionable) |
| 4 Clusters | 0.250 | Poor separation |
| 5 Clusters | 0.164 | Poor separation (used in initial analysis) |
| **Factor Analysis** | N/A | **Allows overlapping dimensions** |

**Key Statistics Supporting Factor Analysis:**
- **KMO = 0.985** (Excellent) - Data is highly suitable for factor analysis
- **Bartlett's Test: p < 0.001** - Correlations are significant, not random

Factor Analysis is more appropriate because:
1. Brand perceptions are **correlated** - people who rate "Land of Dreams" high also rate "Fantastical" high
2. Attributes can **load on multiple factors** - no forced hard assignments
3. Explains **63.2% of variance** with 4 interpretable dimensions

---

## Overview

| Metric | Value |
|--------|-------|
| **Sample Size** | 1,101 respondents with brand benefit data |
| **Time Period** | 6 months (February - July) |
| **Attributes Analyzed** | 36 brand benefit attributes |
| **Factors Identified** | 4 data-driven dimensions |
| **Total Variance Explained** | 63.2% |

---

## The Four Brand Benefit Dimensions

### Factor Summary

| Factor | Variance Explained | # Attributes | Impact on Visit Intent | Significance |
|--------|-------------------|--------------|------------------------|--------------|
| **Disney Magic** | 23.5% | 15 | β = 0.125 | *** Significant |
| **Family Appeal** | 16.8% | 7 | β = 0.059 | *** Significant |
| **Innovation & Thrills** | 15.2% | 10 | β = 0.093 | *** Significant |
| Personal Comfort | 7.6% | 4 | β = 0.034 | Not significant |

**Key Finding**: Three of four factors significantly predict likelihood to visit. **Disney Magic** has the strongest impact, followed by **Innovation & Thrills** and **Family Appeal**.

---

## Detailed Factor Analysis

### Factor 1: Disney Magic (Strongest Driver)

**Impact**: β = 0.125*** - **Strongest predictor of visit intent**

**Variance Explained**: 23.5%

This factor captures the emotional, aspirational quality of the TDL brand:

| Attribute | Loading | Mean Rating |
|-----------|---------|-------------|
| Feel Good | 0.72 | 4.04 |
| Heartwarming | 0.70 | 3.94 |
| Premium Feeling | 0.69 | 3.88 |
| Longing Aspiring | 0.69 | 3.88 |
| Sparkling | 0.69 | 4.14 |
| Soothing Healing | 0.66 | 3.85 |
| Fantastical | 0.62 | 4.06 |
| Removed From Reality | 0.61 | 4.33 |
| Land Of Dreams | 0.59 | 4.31 |
| Feeling Safe | 0.59 | 3.86 |
| Enjoy Myself | 0.56 | 3.89 |
| Repeat Experience | 0.54 | 3.87 |
| Great For Adults | 0.53 | 3.99 |
| Character Interaction | 0.51 | 3.98 |
| Worth Short Vacation | 0.37 | 3.69 |

**Strategic Insight**: This is the largest and most impactful factor. It combines emotional benefits (heartwarming, feel good, premium) with experiential ones (repeat experience, character interaction). The high mean ratings (3.8-4.3) indicate TDL performs strongly here.

---

### Factor 2: Innovation & Thrills

**Impact**: β = 0.093*** - **Second strongest driver**

**Variance Explained**: 15.2%

This factor represents excitement, novelty, and active experiences:

| Attribute | Loading | Mean Rating |
|-----------|---------|-------------|
| Active Adventurous | 0.68 | 3.85 |
| New Innovative | 0.67 | 3.84 |
| Something New | 0.65 | 3.86 |
| Keeping Up With Times | 0.60 | 3.77 |
| Thrilling | 0.57 | 3.53 |
| Variety Of Things | 0.57 | 3.99 |
| Unique Experiences | 0.53 | 4.11 |
| Understands What I Like | 0.48 | 3.62 |
| Feel Comfortable | 0.46 | 3.70 |
| Ticket Options | 0.37 | 3.45 |

**Strategic Insight**: Innovation and novelty matter for visit decisions. Attributes like "New Innovative" and "Something New" drive interest. This aligns with the importance of new attractions and experiences.

---

### Factor 3: Family Appeal

**Impact**: β = 0.059*** - **Significant but moderate driver**

**Variance Explained**: 16.8%

This factor captures family and child-oriented benefits:

| Attribute | Loading | Mean Rating |
|-----------|---------|-------------|
| Want Children Experience | 0.76 | 4.00 |
| Expand Child Worldview | 0.70 | 4.00 |
| Great For Kids 7-17 | 0.68 | 4.06 |
| Great For All Family | 0.62 | 3.98 |
| Great For Kids Under 6 | 0.60 | 3.85 |
| Bond Family Friends | 0.58 | 3.90 |
| Lifelong Memories | 0.55 | 4.02 |

**Strategic Insight**: Family appeal matters for visit decisions, though less than Disney Magic or Innovation. The high mean ratings (3.9-4.1) indicate TDL performs well on these dimensions.

---

### Factor 4: Personal Comfort

**Impact**: β = 0.034 (Not significant)

**Variance Explained**: 7.6%

This factor groups value and accessibility concerns:

| Attribute | Loading | Mean Rating |
|-----------|---------|-------------|
| Affordable | 0.69 | **2.31** |
| Not Crowded | 0.62 | **2.12** |
| Relaxing | 0.55 | 3.42 |
| Worth Price | 0.45 | 3.51 |

**Strategic Insight**: While these attributes have the **lowest ratings** (especially Affordability at 2.31 and Crowding at 2.12), this factor does not significantly predict visit intent when controlling for funnel metrics. This suggests:
1. People are willing to visit despite knowing it's crowded/expensive
2. OR these concerns may affect satisfaction more than initial visit decision

---

## Segment Comparison

Factor scores by segment (standardized, 0 = average):

| Segment | Disney Magic | Personal Comfort | Innovation & Thrills | Family Appeal |
|---------|--------------|------------------|---------------------|---------------|
| E. Adults 35+ | +0.19 | -0.16 | +0.12 | +0.04 |
| B. Older Families | -0.09 | +0.04 | +0.06 | +0.04 |
| A. Young Families | -0.03 | **+0.20** | +0.09 | -0.02 |
| D. Couples 18-34 | -0.03 | -0.08 | -0.06 | -0.04 |
| C. Adults 18-34 | -0.04 | 0.00 | **-0.21** | -0.01 |

**Observations**:
- **Adults 35+** rate Disney Magic highest (more emotionally connected to the brand)
- **Young Families** rate Personal Comfort highest (most price/crowd sensitive)
- **Adults 18-34 (no kids)** rate Innovation & Thrills lowest (may seek more thrilling alternatives?)

---

## Model Performance

| Model | R-squared | Interpretation |
|-------|-----------|----------------|
| Funnel Only (Familiarity, Opinion, Consideration) | 0.659 | Explains 65.9% of visit intent variance |
| Funnel + Factor Scores | 0.677 | Explains 67.7% of variance |
| **Improvement** | **+0.018** | Factors add 1.8% explanatory power |

---

## Key Strategic Insights

### 1. Disney Magic is the Primary Driver

The emotional/aspirational dimension (Feel Good, Heartwarming, Premium, Sparkling) has the **strongest impact** on visit intent. This suggests:
- Emotional messaging DOES work for driving visits (contrary to initial clustering findings)
- Focus on feelings of warmth, aspiration, and premium experience

### 2. Innovation & Novelty Matter

The second-strongest factor emphasizes newness and innovation:
- "Always something new to see and do" messaging is effective
- New attractions and experiences drive visitation
- Keeping up with times is important

### 3. Family Benefits are Moderately Important

Family-oriented messaging works, but is less impactful than emotional/innovation messaging:
- Effective for family segments specifically
- Should be part of the mix, not the primary focus

### 4. Value/Crowding Doesn't Block Visits

Despite low ratings on Affordability (2.31) and Crowding (2.12):
- These factors don't significantly predict visit intent
- People visit despite knowing it's expensive and crowded
- May be more important for repeat visits and satisfaction

---

## Recommendations

### For Marketing Communications

1. **Lead with Emotional Magic** - "Feel good", "heartwarming", "premium", "sparkling" messaging resonates strongest
2. **Emphasize What's New** - Innovation and novelty are significant drivers
3. **Use Family Messaging as Secondary** - Important but not primary driver

### For Segment Targeting

| Segment | Priority Message | Rationale |
|---------|------------------|-----------|
| Adults 35+ | Disney Magic | Highest emotional connection |
| Young Families | Value + Family | Most price-sensitive |
| Adults 18-34 | Innovation & New | Seeking novelty |
| Couples 18-34 | Disney Magic | Romantic/aspirational |

### For Operations

- Affordability (2.31) and Crowding (2.12) are the weakest perceptions
- However, they don't block visits - may affect NPS/satisfaction more
- Consider addressing for repeat visitation strategy

---

## Technical Details

**Factor Analysis Method**: 
- Sklearn FactorAnalysis with Varimax rotation
- Kaiser criterion (eigenvalue > 1) identified 4 factors
- Variance explained: 63.2%

**Suitability Tests**:
- KMO: 0.985 (Excellent)
- Bartlett's Test: χ² = 32,895, p < 0.001

**Regression Model**:
- OLS with standardized coefficients
- Dependent variable: Likelihood to Visit (1-5 scale)
- Controls: Familiarity, Opinion, Consideration

---

## Files Generated

| File | Description |
|------|-------------|
| `output/reports/factor_loadings.csv` | Factor loadings for all attributes |
| `output/reports/factor_impact.csv` | Factor impact on visit intent |
| `output/reports/segment_factor_scores.csv` | Factor scores by segment |
| `output/reports/factor_regression_coefficients.csv` | Full regression results |

---

## Running the Analysis

```bash
cd japan_market_analysis

# Run factor analysis (recommended)
python3 src/brand_benefit_factor_analysis.py

# Run clustering analysis (for comparison)
python3 src/brand_benefit_cluster_analysis.py
```

**Requirements**: pandas, numpy, scikit-learn, scipy, statsmodels

---

*Analysis completed using 6 months of TDL Brand Tracking Survey data*
