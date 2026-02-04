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
                    │  Core TDL Experience ─(0.17)──┤          │
                    │  Value & Accessibility ─(0.07)┤          │
                    │  Thrills & Innovation ─(ns)───┤          │
                    │  Family & Kids Focus ──(ns)───┘          │
                    │                                          │
                    └──────────────────────────────────────────┘
```

---

## Marketing Funnel Path Coefficients

| Path | Standardized β | p-value | Significance |
|------|----------------|---------|--------------|
| Familiarity → Consideration | **0.647** | < 0.001 | *** |
| Familiarity → Likelihood (direct) | 0.106 | < 0.001 | *** |
| Consideration → Likelihood | **0.617** | < 0.001 | *** |
| Opinion → Consideration | 0.038 | 0.105 | ns |
| Opinion → Likelihood | 0.027 | 0.119 | ns |

**Key Funnel Finding**: Familiarity has a very strong direct effect on Consideration (β = 0.647), and Consideration is the strongest predictor of Likelihood (β = 0.617).

---

## Full Model: Funnel + Benefit Factors → Likelihood

| Predictor | Standardized β | p-value | Significance |
|-----------|----------------|---------|--------------|
| **Consideration** | **0.617** | < 0.001 | *** |
| **Core TDL Experience** | **0.167** | < 0.001 | *** |
| Familiarity | 0.106 | < 0.001 | *** |
| **Value & Accessibility** | **0.069** | < 0.001 | *** |
| Opinion | 0.027 | 0.119 | ns |
| Thrills & Innovation | 0.025 | 0.152 | ns |
| Family & Kids Focus | 0.017 | 0.314 | ns |

---

## Model Fit & Comparison

| Metric | Funnel Only | Full Model |
|--------|-------------|------------|
| **R²** | 0.659 | **0.677** |
| **Adjusted R²** | 0.658 | **0.675** |
| **AIC** | 2039.2 | **1987.4** |
| **BIC** | 2059.2 | **2027.5** |

- **R² Improvement**: +0.018 (1.8 percentage points)
- **F-test**: F(4, 1093) = 15.24, **p < 0.001**
- **Conclusion**: Benefit factors significantly improve model fit

---

## Benefit Factor Details

### Factor 1: Core TDL Experience (β = 0.167***)

**The strongest benefit factor - captures the magical, emotional, memorable TDL experience.**

This factor combines emotional warmth with core experiential benefits. It represents what makes TDL special.

| Attribute | Loading | Type |
|-----------|---------|------|
| **Feel Good** | 0.852 | Emotional |
| **Lifelong Memories** | 0.828 | Functional |
| **Great For Adults** | 0.822 | Functional |
| **Heartwarming** | 0.820 | Emotional |
| **Great For All Family** | 0.815 | Functional |
| **Repeat Experience** | 0.812 | Functional |
| **Premium Feeling** | 0.809 | Emotional |
| **Enjoy Myself** | 0.806 | Functional |
| **Bond Family Friends** | 0.800 | Functional |
| **Longing Aspiring** | 0.799 | Emotional |

**Composition**: 6 functional + 4 emotional attributes
**Interpretation**: This is the "Disney Magic" factor - combining emotional resonance (heartwarming, feel good, premium) with experiential benefits (memories, repeat visits, enjoyment).

---

### Factor 2: Value & Accessibility (β = 0.069***)

**Significant driver - perceptions of affordability and convenience.**

| Attribute | Loading | Type |
|-----------|---------|------|
| **Affordable** | 0.624 | Functional |
| **Not Crowded** | 0.589 | Functional |
| Relaxing | 0.345 | Functional |
| Removed From Reality | 0.316 | Emotional |
| Understands What I Like | 0.293 | Functional |
| Ticket Options | 0.288 | Functional |
| Worth Price | 0.277 | Functional |
| Thrilling | 0.274 | Functional |
| Great For Kids 7-17 | 0.272 | Functional |
| Want Children Experience | 0.271 | Functional |

**Composition**: 9 functional + 1 emotional attributes
**Interpretation**: Despite low absolute ratings on Affordability (2.31/5) and Crowding (2.12/5), improvements in these perceptions do increase visit intent.

---

### Factor 3: Thrills & Innovation (β = 0.025, ns)

**Not significant when controlling for other factors.**

| Attribute | Loading | Type |
|-----------|---------|------|
| Active Adventurous | 0.259 | Functional |
| Soothing Healing | 0.255 | Emotional |
| Heartwarming | 0.242 | Emotional |
| Longing Aspiring | 0.221 | Emotional |
| New Innovative | 0.221 | Functional |
| Feel Good | 0.211 | Emotional |
| Premium Feeling | 0.211 | Emotional |
| Keeping Up With Times | 0.199 | Functional |
| Something New | 0.195 | Functional |
| Feeling Safe | 0.192 | Emotional |

**Composition**: 4 functional + 6 emotional attributes
**Interpretation**: Innovation and thrill-seeking don't independently predict visit intent once Core Experience is accounted for.

---

### Factor 4: Family & Kids Focus (β = 0.017, ns)

**Not significant when controlling for other factors.**

| Attribute | Loading | Type |
|-----------|---------|------|
| Want Children Experience | 0.284 | Functional |
| Great For Kids Under 6 | 0.271 | Functional |
| Relaxing | 0.237 | Functional |
| Affordable | 0.235 | Functional |
| Expand Child Worldview | 0.230 | Functional |
| Active Adventurous | 0.214 | Functional |
| Something New | 0.205 | Functional |
| Great For Kids 7-17 | 0.205 | Functional |
| Not Crowded | 0.197 | Functional |
| New Innovative | 0.177 | Functional |

**Composition**: 10 functional + 0 emotional attributes
**Interpretation**: Kids-specific benefits don't predict visit intent beyond the Core Experience factor (which already includes family bonding).

---

## Segment Analysis

| Segment | n | Model R² | Consideration → Likelihood |
|---------|---|----------|---------------------------|
| E. Adults 35+ (no kids) | 221 | **0.760** | **0.685** |
| D. Couples 18-34 (no kids) | 220 | **0.700** | **0.645** |
| A. Young Families | 220 | 0.690 | 0.613 |
| C. Adults 18-34 (no kids) | 220 | 0.651 | 0.476 |
| B. Older Families | 220 | 0.624 | 0.582 |

**Key Findings**:
- **Adults 35+** has highest R² (0.760) - the model explains their behavior best
- **Adults 18-34 (no kids)** has weakest Consideration → Likelihood path (0.476) - something else is blocking conversion

---

## Key Strategic Insights

### 1. The "Core TDL Experience" is the Primary Driver

The strongest benefit factor (β = 0.167) combines:
- **Emotional warmth**: Feel Good, Heartwarming, Premium Feeling
- **Memory-making**: Lifelong Memories, Bond Family Friends
- **Personal enjoyment**: Enjoy Myself, Great For Adults, Repeat Experience

**Implication**: This IS the "Disney Magic" - messaging should emphasize emotional connection, memory creation, and the premium feel-good experience.

### 2. Consideration Remains the Critical Funnel Stage

With β = 0.617, moving consumers from "aware" to "considering" is the most important conversion point.

### 3. Value Perceptions Help (But Aren't Dealbreakers)

Value & Accessibility (β = 0.069) is significant but smaller:
- Current ratings are low (Affordable: 2.31, Not Crowded: 2.12)
- Improving these perceptions would help, but emotional experience matters more
- People visit despite knowing it's expensive and crowded

### 4. Thrills and Kids-Specific Messaging Don't Move the Needle

Neither Thrills & Innovation nor Family & Kids Focus are significant when the Core Experience is controlled for. This suggests:
- TDL isn't primarily about thrill rides (unlike USJ)
- Kids-specific benefits are captured within the broader "family bonding" experience
- Don't over-index on these in messaging

---

## Recommendations

### For Marketing Communications

| Priority | Message Focus | Rationale |
|----------|---------------|-----------|
| 1 | **Emotional Connection** | Core TDL Experience is strongest driver |
| 2 | **Memory Creation** | "Lifelong Memories" loads highly |
| 3 | **Premium Experience** | "Premium Feeling" resonates |
| 4 | **Adult Enjoyment** | "Great For Adults" often overlooked |

### For Segment Targeting

| Segment | Strategy |
|---------|----------|
| Adults 35+ | High conversion - focus on acquisition |
| Adults 18-34 (no kids) | Weakest conversion - research barriers |
| Couples 18-34 | Strong performers - upsell opportunities |
| Young Families | Core segment - maintain messaging |
| Older Families | Lower conversion - may have scheduling barriers |

---

## Technical Details

### Factor Analysis
- **Method**: Sklearn FactorAnalysis (4 components)
- **KMO**: 0.985 (Excellent)
- **Bartlett's Test**: χ² = 32,895, p < 0.001
- **Why not clustering**: Silhouette score was 0.163 (poor) - Factor Analysis handles correlated attributes better

### Regression Model
- **Method**: OLS with standardized coefficients
- **Sample**: n = 1,101 with complete funnel and benefit data
- **Controls**: Familiarity, Opinion, Consideration

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

*Analysis completed using 6 months of TDL Brand Tracking Survey data (n = 1,101)*
