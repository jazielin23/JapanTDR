# TDL Brand Benefit Analysis: Full SEM Model

A comprehensive analysis combining the **Marketing Funnel** path model with **Brand Benefit Factors** to understand what drives visit intent for Tokyo Disneyland (TDL).

---

## Overview

| Metric | Value |
|--------|-------|
| **Sample Size** | n = 1,096 respondents with complete data |
| **Time Period** | 6 months (February - July) |
| **Funnel Metrics** | Familiarity, Opinion, Consideration, Likelihood |
| **Benefit Attributes** | 36 (26 functional + 10 emotional) |
| **Benefit Factors** | 4 data-driven dimensions |

> **Note**: Data cleaning removed invalid codes (0, 99) from funnel variables to ensure proper 1-5 Likert scale values.

---

## Full SEM Model Results

### Model Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                     MARKETING FUNNEL                                  │
│                                                                       │
│   Familiarity ──(0.67)──► Opinion ──(0.48)──► Consideration          │
│        │                      │                     │                 │
│        │                      │               (0.59)│                 │
│        └──────(0.32)──────────┼─────────────────────┘                 │
│        │                      │                     │                 │
│   (0.08)                 (0.11)                     ▼                 │
│        └──────────────────────┼────────────► LIKELIHOOD              │
│                               └────────────────────►▲                 │
└────────────────────────────────────────────────────┬─────────────────┘
                                                      │
┌────────────────────────────────────────────────────┬─────────────────┐
│                   BENEFIT FACTORS                   │                 │
│                                                     │                 │
│   Core TDL Experience ──────(0.13)──────────────────┤                 │
│   Value & Accessibility ────(0.07)──────────────────┤                 │
│   Thrills & Innovation ─────(ns)────────────────────┤                 │
│   Family & Kids Focus ──────(ns)────────────────────┘                 │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Marketing Funnel Path Coefficients

| Path | Standardized β | p-value | Significance |
|------|----------------|---------|--------------|
| **Familiarity → Opinion** | **0.667** | < 0.001 | *** |
| **Opinion → Consideration** | **0.476** | < 0.001 | *** |
| **Familiarity → Consideration** | **0.321** | < 0.001 | *** |

**Key Findings**:
- Familiarity has a very strong effect on Opinion (β = 0.667) - the more familiar people are with TDL, the better their opinion
- Opinion strongly drives Consideration (β = 0.476) - positive opinions lead to active consideration
- Familiarity also directly influences Consideration (β = 0.321) beyond its effect through Opinion

---

## Full Model: Funnel + Benefit Factors → Likelihood

| Predictor | Standardized β | p-value | Significance |
|-----------|----------------|---------|--------------|
| **Consideration** | **0.587** | < 0.001 | *** |
| **Core TDL Experience** | **0.126** | < 0.001 | *** |
| **Opinion** | **0.112** | < 0.001 | *** |
| Familiarity | 0.076 | 0.002 | ** |
| **Value & Accessibility** | **0.071** | < 0.001 | *** |
| Thrills & Innovation | 0.021 | 0.213 | ns |
| Family & Kids Focus | 0.020 | 0.256 | ns |

### Interpretation

**Funnel Effects**:
- **Consideration** (β = 0.587) remains the strongest predictor - once someone is considering TDL, they're very likely to intend to visit
- **Opinion** (β = 0.112) is significant - positive opinions directly increase visit intent
- **Familiarity** (β = 0.076) has a smaller but significant direct effect

**Benefit Factor Effects**:
- **Core TDL Experience** (β = 0.126) is the strongest benefit factor - the emotional/experiential perception of TDL drives visit intent
- **Value & Accessibility** (β = 0.071) is also significant - perceptions of affordability and accessibility matter
- Thrills & Innovation and Family & Kids Focus are not significant when controlling for funnel metrics

---

## Model Fit & Comparison

| Metric | Funnel Only | Full Model |
|--------|-------------|------------|
| **R²** | 0.670 | **0.682** |
| **Adjusted R²** | 0.669 | **0.680** |
| **AIC** | 1988.9 | **1957.3** |
| **BIC** | 2008.9 | **1997.3** |

- **R² Improvement**: +0.012 (1.2 percentage points)
- **F-test**: F(4, 1088) = 9.99, **p < 0.001**
- **Conclusion**: Benefit factors significantly improve model fit

---

## Benefit Factor Details

### Factor 1: Core TDL Experience (β = 0.126***)

**The strongest benefit factor - captures the magical, emotional, memorable TDL experience.**

| Attribute | Loading | Type |
|-----------|---------|------|
| **Feel Good** | 0.851 | Emotional |
| **Lifelong Memories** | 0.830 | Functional |
| **Great For Adults** | 0.825 | Functional |
| **Heartwarming** | 0.821 | Emotional |
| **Great For All Family** | 0.816 | Functional |
| **Repeat Experience** | 0.814 | Functional |
| **Premium Feeling** | 0.808 | Emotional |
| **Enjoy Myself** | 0.808 | Functional |
| **Bond Family Friends** | 0.800 | Functional |
| **Longing Aspiring** | 0.798 | Emotional |

**Composition**: 6 functional + 4 emotional attributes

**Interpretation**: This is the "Disney Magic" factor - combining emotional resonance (heartwarming, feel good, premium) with experiential benefits (memories, repeat visits, enjoyment). This drives visit intent beyond the marketing funnel.

---

### Factor 2: Value & Accessibility (β = 0.071***)

**Significant driver - perceptions of affordability and convenience.**

| Attribute | Loading | Type |
|-----------|---------|------|
| **Affordable** | 0.628 | Functional |
| **Not Crowded** | 0.591 | Functional |
| Relaxing | 0.342 | Functional |
| Removed From Reality | 0.310 | Emotional |
| Ticket Options | 0.290 | Functional |
| Understands What I Like | 0.287 | Functional |
| Want Children Experience | 0.275 | Functional |
| Thrilling | 0.273 | Functional |
| Worth Price | 0.272 | Functional |
| Great For Kids 7-17 | 0.268 | Functional |

**Composition**: 9 functional + 1 emotional attributes

**Interpretation**: Despite low absolute ratings on Affordability (2.31/5) and Crowding (2.12/5), improvements in these perceptions do increase visit intent.

---

### Factor 3: Thrills & Innovation (β = 0.021, ns)

**Not significant when controlling for funnel and other factors.**

| Attribute | Loading | Type |
|-----------|---------|------|
| Soothing Healing | 0.254 | Emotional |
| Active Adventurous | 0.253 | Functional |
| Heartwarming | 0.243 | Emotional |
| Longing Aspiring | 0.223 | Emotional |
| New Innovative | 0.216 | Functional |
| Feel Good | 0.213 | Emotional |
| Premium Feeling | 0.212 | Emotional |
| Something New | 0.196 | Functional |
| Keeping Up With Times | 0.195 | Functional |
| Feeling Safe | 0.192 | Emotional |

**Composition**: 4 functional + 6 emotional attributes

---

### Factor 4: Family & Kids Focus (β = 0.020, ns)

**Not significant when controlling for funnel and other factors.**

| Attribute | Loading | Type |
|-----------|---------|------|
| Want Children Experience | 0.280 | Functional |
| Great For Kids Under 6 | 0.272 | Functional |
| Relaxing | 0.242 | Functional |
| Affordable | 0.239 | Functional |
| Expand Child Worldview | 0.227 | Functional |
| Active Adventurous | 0.217 | Functional |
| Something New | 0.211 | Functional |
| Not Crowded | 0.202 | Functional |
| Great For Kids 7-17 | 0.201 | Functional |
| New Innovative | 0.179 | Functional |

**Composition**: 10 functional + 0 emotional attributes

---

## Segment Analysis

| Segment | n | Model R² | Consideration → Likelihood |
|---------|---|----------|---------------------------|
| E. Adults 35+ (no kids) | 221 | **0.760** | **0.685** |
| D. Couples 18-34 (no kids) | 217 | **0.700** | 0.586 |
| A. Young Families | 220 | 0.690 | 0.614 |
| C. Adults 18-34 (no kids) | 220 | 0.651 | 0.477 |
| B. Older Families | 218 | 0.646 | 0.522 |

**Key Findings**:
- **Adults 35+** has highest R² (0.760) and strongest Consideration → Likelihood path
- **Adults 18-34 (no kids)** has weakest conversion from Consideration to Likelihood (0.477)

---

## Key Strategic Insights

### 1. The Funnel Works as Expected

With cleaned data, the full funnel path is significant:
- Familiarity → Opinion (β = 0.667) - Building familiarity improves opinions
- Opinion → Consideration (β = 0.476) - Better opinions drive consideration
- Consideration → Likelihood (β = 0.587) - Consideration converts to intent

### 2. "Core TDL Experience" is the Key Benefit Driver

Beyond the funnel, the strongest benefit factor (β = 0.126) combines:
- **Emotional warmth**: Feel Good, Heartwarming, Premium Feeling
- **Memory-making**: Lifelong Memories, Bond Family Friends
- **Personal enjoyment**: Enjoy Myself, Great For Adults, Repeat Experience

### 3. Value Perceptions Add Incremental Impact

Value & Accessibility (β = 0.071) is significant:
- Current ratings are low (Affordable: 2.31, Not Crowded: 2.12)
- Improving these would provide incremental gains
- But Core TDL Experience matters almost twice as much

### 4. Opinion Has Independent Value

Opinion (β = 0.112) is significant even controlling for Consideration and benefit factors. This means:
- Opinion building is valuable beyond just driving consideration
- Brand sentiment has direct effects on visit intent

---

## Recommendations

### For Marketing Strategy

| Priority | Focus Area | Rationale |
|----------|------------|-----------|
| 1 | **Build Familiarity** | Strongest upper-funnel driver (β = 0.667 → Opinion) |
| 2 | **Emotional Experience Messaging** | Core TDL Experience is strongest benefit factor |
| 3 | **Convert Consideration** | Strongest predictor of Likelihood (β = 0.587) |
| 4 | **Value Communications** | Incremental benefit, especially for price-sensitive segments |

### For Segment Targeting

| Segment | Strategy |
|---------|----------|
| Adults 35+ | High conversion - focus on acquisition |
| Adults 18-34 (no kids) | Weakest conversion - research barriers |
| Couples 18-34 | Strong performers - upsell opportunities |
| Young Families | Core segment - maintain emotional messaging |
| Older Families | Lower conversion - may have scheduling barriers |

---

## Technical Details

### Data Cleaning
- Removed invalid codes (0, 99) from funnel variables
- All funnel metrics validated to 1-5 Likert scale range

### Factor Analysis
- **Method**: Sklearn FactorAnalysis (4 components)
- **KMO**: 0.985 (Excellent)
- **Bartlett's Test**: p < 0.001
- **Why Factor Analysis**: Clustering had silhouette of 0.163 (poor) - Factor Analysis handles correlated attributes better

### Regression Model
- **Method**: OLS with standardized coefficients
- **Sample**: n = 1,096 with complete funnel and benefit data
- **Model R²**: 0.682

---

## Files Generated

| File | Description |
|------|-------------|
| `output/reports/sem_full_model_results.csv` | Full model coefficients |
| `output/reports/sem_model_comparison.csv` | Funnel vs Full model comparison |
| `output/reports/sem_segment_results.csv` | Segment-level analysis |
| `output/reports/factor_attribute_details.csv` | All factor loadings by attribute |

---

## Running the Analysis

```bash
cd japan_market_analysis

# Run full SEM model with benefits (recommended)
python3 src/full_sem_with_benefits.py

# Run factor analysis only
python3 src/brand_benefit_factor_analysis.py
```

**Requirements**: pandas, numpy, scikit-learn, scipy, statsmodels

---

*Analysis completed using 6 months of TDL Brand Tracking Survey data (n = 1,096)*
