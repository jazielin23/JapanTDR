# TDL Brand Benefit Cluster Analysis

A data-driven analysis of Tokyo Disneyland (TDL) brand benefits using cluster analysis on 6 months of survey data. Rather than using predefined functional/emotional categories, this analysis lets the data reveal natural groupings of brand attributes.

---

## Overview

| Metric | Value |
|--------|-------|
| **Sample Size** | 1,101 respondents with brand benefit data |
| **Time Period** | 6 months (February - July) |
| **Attributes Analyzed** | 36 brand benefit attributes |
| **Clusters Identified** | 5 data-driven clusters |

---

## Data-Driven Benefit Clusters

The clustering algorithm identified **5 distinct groupings** of brand benefits based on how respondents rate them together:

### Cluster Summary

| Cluster | Attributes | Mean Rating | Impact on Visit Intent | Significance |
|---------|------------|-------------|------------------------|--------------|
| **Experience & Innovation** | 12 | 3.68 | β = 0.116 | **Significant** |
| Magic & Enchantment | 13 | 4.03 | β = 0.024 | Not significant |
| Family & Kids Appeal | 9 | 3.97 | β = 0.023 | Not significant |
| Affordability | 1 | 2.31 | β = 0.025 | Not significant |
| Crowd Management | 1 | 2.12 | β = 0.003 | Not significant |

**Key Finding**: Only the **Experience & Innovation** cluster significantly predicts likelihood to visit (β = 0.116, p = 0.004).

---

## Detailed Cluster Analysis

### 1. Experience & Innovation (THE KEY DRIVER)

**Impact**: β = 0.116 (p = 0.004) - **Significantly predicts visit intent**

This cluster contains practical experience attributes that drive actual visit decisions:

| Attribute | Mean Score | Correlation with Visit Intent |
|-----------|------------|-------------------------------|
| Repeat Experience | 3.87 | **0.63** |
| Understands What I Like | 3.62 | **0.60** |
| Worth Price | 3.51 | **0.50** |
| Feel Comfortable | 3.70 | 0.50 |
| New Innovative | 3.84 | 0.48 |
| Relaxing | 3.42 | 0.46 |
| Something New | 3.86 | 0.45 |
| Active Adventurous | 3.85 | 0.45 |
| Keeping Up With Times | 3.77 | 0.43 |
| Worth Short Vacation | 3.69 | 0.41 |
| Thrilling | 3.53 | 0.36 |
| Ticket Options | 3.45 | 0.36 |

**Strategic Insight**: The attributes with the highest correlation to visit intent are about repeat visitation, personal relevance, and perceived value - not magic or fantasy.

---

### 2. Magic & Enchantment

**Impact**: β = 0.024 (not significant) - Does not incrementally predict visit intent beyond funnel metrics

This cluster captures the fantasy/emotional experience of TDL:

| Attribute | Mean Score | Correlation with Visit Intent |
|-----------|------------|-------------------------------|
| Removed From Reality | 4.33 | 0.39 |
| Land Of Dreams | 4.31 | 0.40 |
| Sparkling | 4.14 | 0.44 |
| Unique Experiences | 4.11 | 0.45 |
| Fantastical | 4.06 | 0.44 |
| Feel Good | 4.04 | 0.55 |
| Variety Of Things | 3.99 | 0.49 |
| Character Interaction | 3.98 | 0.43 |
| Heartwarming | 3.94 | 0.52 |
| Premium Feeling | 3.88 | 0.51 |
| Longing Aspiring | 3.88 | 0.54 |
| Feeling Safe | 3.86 | 0.48 |
| Soothing Healing | 3.85 | 0.52 |

**Strategic Insight**: TDL scores very high on these magical attributes (4.0+ average), but this doesn't differentiate visitors from non-visitors. Everyone already perceives TDL as magical.

---

### 3. Family & Kids Appeal

**Impact**: β = 0.023 (not significant)

| Attribute | Mean Score | Correlation with Visit Intent |
|-----------|------------|-------------------------------|
| Great For Kids 7-17 | 4.06 | 0.38 |
| Lifelong Memories | 4.02 | 0.49 |
| Want Children Experience | 4.00 | 0.44 |
| Expand Child Worldview | 4.00 | 0.43 |
| Great For Adults | 3.99 | 0.53 |
| Great For All Family | 3.98 | 0.50 |
| Bond Family Friends | 3.90 | 0.51 |
| Enjoy Myself | 3.89 | **0.61** |
| Great For Kids Under 6 | 3.85 | 0.38 |

**Note**: "Enjoy Myself" has the highest correlation (0.61) in this cluster, suggesting personal enjoyment matters more than family-oriented messaging.

---

### 4. Affordability

**Impact**: β = 0.025 (not significant)

| Attribute | Mean Score | Correlation with Visit Intent |
|-----------|------------|-------------------------------|
| Affordable | 2.31 | 0.22 |

**Key Weakness**: This is TDL's lowest-rated attribute. While it correlates with visit intent, improving affordability perception may not be the most effective lever.

---

### 5. Crowd Management

**Impact**: β = 0.003 (not significant)

| Attribute | Mean Score | Correlation with Visit Intent |
|-----------|------------|-------------------------------|
| Not Crowded | 2.12 | 0.12 |

**Key Weakness**: Also a very low rating (2.12/5), indicating crowding is a known issue. However, it has the weakest correlation with visit intent.

---

## Segment Comparison

How each segment rates the benefit clusters:

| Segment | Magic & Enchantment | Affordability | Family & Kids | Experience & Innovation | Crowd Mgmt |
|---------|---------------------|---------------|---------------|-------------------------|------------|
| C. Adults 18-34 | **4.13** | 2.42 | 4.02 | **3.78** | 2.20 |
| A. Young Families | 4.09 | 2.21 | **4.06** | 3.68 | 2.06 |
| B. Older Families | 4.06 | 2.31 | 4.03 | 3.72 | 2.05 |
| D. Couples 18-34 | 4.02 | **2.45** | 3.96 | 3.70 | **2.23** |
| E. Adults 35+ | 3.84 | 2.15 | 3.75 | 3.50 | 2.04 |

**Observations**:
- **Adults 18-34 (no kids)** rate TDL highest on both Magic & Enchantment AND Experience & Innovation
- **Young Families** rate Family & Kids Appeal highest
- **Couples 18-34** are most sensitive to Affordability and Crowding concerns
- **Adults 35+** rate all clusters lowest - a segment opportunity

---

## Model Performance

| Model | R-squared | Interpretation |
|-------|-----------|----------------|
| Funnel Only (Familiarity, Opinion, Consideration) | 0.659 | Explains 65.9% of visit intent variance |
| Funnel + Benefit Clusters | 0.675 | Explains 67.5% of variance |
| **Improvement** | **+0.016** | Clusters add 1.6% explanatory power |

---

## Key Strategic Insights

### 1. Experience & Innovation is the Only Significant Driver

When controlling for funnel metrics (familiarity, opinion, consideration), only the **Experience & Innovation** cluster significantly predicts likelihood to visit. This cluster emphasizes:
- **Repeat visitation** ("I want to experience this again")
- **Personal relevance** ("Understands what I like")
- **Value perception** ("Worth the price")
- **Comfort & innovation** (comfortable yet always something new)

### 2. Magic Doesn't Differentiate

TDL scores exceptionally high on magical/fantasy attributes (4.0+), but these don't predict who will actually visit. This suggests:
- Everyone already knows TDL is magical
- Magic-focused messaging may not drive incremental visits
- Magic may be a "table stakes" expectation rather than a decision driver

### 3. Practical Benefits Matter Most

The data suggests visitors are making practical assessments:
- "Is this worth my time and money?"
- "Will I enjoy this again?"
- "Does this park understand me?"

### 4. Affordability & Crowding are Pain Points

Both attributes score below 2.5 on a 5-point scale, indicating:
- Clear areas for operational improvement
- However, neither significantly impacts visit intent in the model
- May be more important for satisfaction than initial visit decision

---

## Recommendations

### For Marketing Communications

1. **Lead with Experience & Innovation** - Emphasize what's new, the value of repeat visits, and personal relevance
2. **Use Magic as Supporting Context** - Don't lead with "magical" messaging; it's expected
3. **Address Practical Concerns** - Value messaging may resonate more than fantasy messaging

### For Targeting

1. **Adults 35+** - Lowest scores across all clusters; opportunity segment needing different approach
2. **Couples 18-34** - Most price/crowd sensitive; may benefit from off-peak messaging
3. **Young Families** - Strong family appeal; maintain family-focused content

### For Operations

1. **Crowd Management** - While low impact on visit intent, likely impacts satisfaction and NPS
2. **Value Perception** - "Worth Price" (3.51) is notably lower than other experience attributes

---

## Technical Details

**Clustering Method**: K-Means on PCA-reduced attribute response patterns
- PCA captured 55.5% of variance in first 5 components
- 5-cluster solution selected for marketing actionability
- Silhouette score: 0.163

**Regression Model**: OLS with standardized coefficients
- Dependent variable: Likelihood to Visit (1-5 scale)
- Controls: Familiarity, Opinion, Consideration
- Predictors: 5 cluster composite scores

---

## Files Generated

| File | Description |
|------|-------------|
| `output/reports/benefit_cluster_assignments.csv` | Which cluster each attribute belongs to |
| `output/reports/benefit_cluster_impact.csv` | Cluster impact on visit intent |
| `output/reports/benefit_attribute_details.csv` | Individual attribute statistics |
| `output/reports/segment_cluster_scores.csv` | Cluster scores by segment |
| `output/reports/benefit_regression_coefficients.csv` | Full regression results |

---

## Running the Analysis

```bash
cd japan_market_analysis
python3 src/brand_benefit_cluster_analysis.py
```

**Requirements**: pandas, numpy, scikit-learn, scipy, statsmodels

---

*Analysis completed using 6 months of TDL Brand Tracking Survey data*
