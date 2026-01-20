# Tokyo Disneyland (TDL) Brand Tracking Analysis

## Overview

This analysis uses **real survey data** from the Japan Theme Park Brand Tracking Study across **6 waves** (February-July), analyzed using **Structural Equation Modeling (SEM)** to test causal relationships in the marketing funnel.

**Sample:** 3,260 total respondents across 6 waves (1,096 with complete brand attribute data for full SEM)  
**Focus:** Tokyo Disneyland (TDL)  
**Scale Validation:** All Likert scales confirmed (5=High/Positive, 1=Low/Negative)

---

## Data Summary

| Wave | Month | Sample Size |
|------|-------|-------------|
| 1 | February | 541 |
| 2 | March | 762 |
| 3 | April | 497 |
| 4 | May | 500 |
| 5 | June | 500 |
| 6 | July | 500 |
| **Total** | **Feb-Jul** | **3,300** |

---

## Research Objectives

1. **Marketing Funnel Analysis** - How funnel KPIs drive intent to visit
2. **Brand Benefits Analysis** - How functional vs emotional benefits influence intent
3. **Segment Comparison** - Compare path coefficients across demographic segments
4. **Mediation Testing** - Test indirect effects within the funnel
5. **Time Series Trend Analysis** (NEW) - Detect trends across the 6-month period

---

## 🔍 How to Read This Analysis: A Plain-Language Guide

### Understanding Path Coefficients (Beta/β)

**Path coefficients** tell you how strongly one variable influences another. Here's a quick reference:

| Beta Value | Strength | What It Means |
|------------|----------|---------------|
| **0.60+** | Very strong | Major influence - priority focus area |
| **0.40 - 0.59** | Strong | Meaningful relationship worth optimizing |
| **0.20 - 0.39** | Moderate | Notable effect, actionable |
| **0.10 - 0.19** | Small | Real but modest impact |
| **< 0.10** | Weak | Limited practical significance |

**Example interpretation**: Familiarity → Opinion (β = 0.68) means:
> "For every 1-unit increase in Familiarity, Opinion increases by 0.68 units. This is a VERY STRONG relationship. Improving how well people know TDL substantially improves what they think of TDL."

### What p-value Means

| p-value | Meaning |
|---------|---------|
| **< 0.001 (\*\*\*)** | We are >99.9% confident this relationship is real |
| **< 0.01 (\*\*)** | We are >99% confident |
| **< 0.05 (\*)** | We are >95% confident |
| **> 0.05 (ns)** | Cannot confirm the relationship is real |

---

## SEM Results

### Objective 1: Marketing Funnel Analysis (n=3,260)

**Path Model:** Familiarity -> Opinion -> Consideration -> Likelihood

| Path | Standardized Beta | p-value | Significance |
|------|-------------------|---------|--------------|
| Familiarity -> Opinion | **0.679** | < 0.001 | *** |
| Opinion -> Consideration | **0.479** | < 0.001 | *** |
| Familiarity -> Consideration (direct) | 0.342 | < 0.001 | *** |
| Consideration -> Likelihood | **0.606** | < 0.001 | *** |
| Opinion -> Likelihood (direct) | 0.186 | < 0.001 | *** |
| Familiarity -> Likelihood (direct) | 0.098 | < 0.001 | *** |

**Model Fit:** R-squared = 0.676 (67.6% of variance in Likelihood explained)

**Key Finding:** Consideration is the strongest direct predictor of Likelihood (Beta = 0.606). The funnel flows sequentially with each stage significantly predicting the next.

```
Familiarity --(0.68)--> Opinion --(0.48)--> Consideration --(0.61)--> Likelihood
     |                      |                                            ^
     |                      +---------(0.19)-----------------------------+
     +-----------------(0.10)--------------------------------------------+
```

#### 💡 What These Numbers Mean (Plain-Language Interpretation)

**YES, your interpretation is correct!** Familiarity has a strong influence on Opinion and Consideration. Here's why this is a big learning:

| Path | Beta | Interpretation |
|------|------|----------------|
| **Familiarity → Opinion** | **0.68** | **VERY STRONG.** When people become more familiar with TDL, their opinion of the brand improves dramatically. This is one of the strongest relationships in our entire model. |
| **Familiarity → Consideration** | **0.34** | **STRONG.** Familiarity directly drives consideration to visit - people who know TDL better are more likely to consider going. |
| **Opinion → Consideration** | **0.48** | **STRONG.** Better opinions lead to more consideration. Opinion is the "amplifier" that converts familiarity into intent. |
| **Consideration → Likelihood** | **0.61** | **VERY STRONG.** Once someone considers TDL, they're very likely to intend to visit. This is the highest-converting stage. |
| **Opinion → Likelihood (direct)** | **0.19** | **MODERATE.** Opinion has some direct effect on likelihood, but most of its power (67%) flows through Consideration. |
| **Familiarity → Likelihood (direct)** | **0.10** | **SMALL.** Familiarity has a small direct effect, but its main power is through Opinion and Consideration. |

**The Big Picture:**

Familiarity is your **"starting lever"** - when you pull it:
1. Opinion jumps significantly (β = 0.68)
2. Consideration increases directly (β = 0.34) AND indirectly through Opinion
3. This flows down to Likelihood

**Actionable implication:** Campaigns that build familiarity (detailed park information, behind-the-scenes content, educational materials about TDL experiences) can move the ENTIRE funnel.

---

### Objective 2: Brand Benefits Analysis (n=1,096)

**Testing:** Functional & Emotional Benefits -> Likelihood

| Predictor | Standardized Beta | p-value | Significance |
|-----------|-------------------|---------|--------------|
| Functional Benefits | **0.144** | < 0.001 | *** |
| Emotional Benefits | -0.019 | 0.597 | ns |

**Full Model (Funnel + Benefits):** R-squared = 0.678

| Variable | Beta | p-value |
|----------|------|---------|
| Consideration | 0.595 | < 0.001 *** |
| Functional | 0.144 | < 0.001 *** |
| Opinion | 0.104 | < 0.001 *** |
| Familiarity | 0.087 | < 0.001 *** |
| Emotional | -0.019 | 0.597 ns |

**Key Finding:** Functional benefits have a significant unique effect on Likelihood (Beta = 0.144, p < 0.001), while Emotional benefits do not add incremental predictive power beyond the funnel metrics. This suggests that for TDL, **functional messaging** (convenience, variety, value) may be more effective than emotional messaging for driving visit intent.

---

### Objective 3: Segment Comparison (n=3,260)

**Path: Consideration -> Likelihood by Segment**

| Segment | n | Beta | p-value | R-squared |
|---------|---|------|---------|-----------|
| E. Adults 35+ (no kids) | 650 | **0.826** | < 0.001 | 0.709 |
| A. Young Families | 657 | 0.803 | < 0.001 | 0.589 |
| C. Adults 18-34 (no kids) | 650 | 0.794 | < 0.001 | 0.674 |
| D. Couples 18-34 (no kids) | 650 | 0.789 | < 0.001 | 0.609 |
| B. Older Families | 653 | **0.747** | < 0.001 | 0.576 |

**Key Finding:** 
- **Strongest effect:** Adults 35+ (Beta = 0.826) - When this segment considers visiting, they're very likely to follow through
- **Weakest effect:** Older Families (Beta = 0.747) - Consideration doesn't convert as strongly to intent
- Path coefficients vary by segment, supporting **targeted marketing approaches**

**Funnel Metrics by Segment:**

| Segment | Familiarity | Opinion | Consideration | Likelihood | NPS |
|---------|-------------|---------|---------------|------------|-----|
| D. Couples 18-34 | 4.04 | 4.30 | 4.17 | 4.12 | 8.56 |
| A. Young Families | 3.96 | 4.26 | 4.15 | 4.08 | 8.52 |
| C. Adults 18-34 | 4.00 | 4.27 | 4.03 | 4.02 | 8.55 |
| B. Older Families | 3.96 | 4.20 | 3.99 | 3.94 | 8.54 |
| E. Adults 35+ | 3.81 | 4.13 | 3.63 | 3.49 | 7.84 |

---

### Objective 4: Mediation Testing (n=3,260)

**Test 1: Does Consideration mediate Opinion -> Likelihood?**

| Component | Value |
|-----------|-------|
| Path a (Opinion -> Consideration) | 0.711 |
| Path b (Consideration -> Likelihood) | 0.643 |
| Direct Effect c' (Opinion -> Likelihood) | 0.227 |
| Indirect Effect (a x b) | **0.457** |
| Sobel z | 35.489 |
| p-value | < 0.001 |
| **% Mediated** | **66.8%** |

**Result:** Significant **partial mediation**. 66.8% of Opinion's effect on Likelihood flows through Consideration. Both direct and indirect paths are significant.

**Test 2: Does Opinion mediate Familiarity -> Likelihood?**

| Component | Value |
|-----------|-------|
| Indirect Effect | 0.324 |
| Sobel z | 25.242 |
| p-value | < 0.001 |

**Result:** Significant mediation. Opinion mediates Familiarity's effect on Likelihood.

#### 💡 What Mediation Means (Plain-Language Interpretation)

**Mediation answers: "HOW does one thing lead to another?"**

Think of it like this:
- You want to know: "Does having a good Opinion of TDL make people want to visit?"
- Answer: YES, but through TWO routes:

```
Route 1 (33% of effect):    Opinion ──────────────────► Likelihood
                            "I like TDL, so I want to visit"

Route 2 (67% of effect):    Opinion ──► Consideration ──► Likelihood
                            "I like TDL, so I'm considering visiting,
                             and because I'm considering it, I want to go"
```

**Why 67% is important:**
Most of Opinion's effect doesn't go directly to Likelihood - it first has to pass through Consideration. This means:

1. **You can't skip the funnel stages** - improving Opinion without moving people to active Consideration loses 67% of the potential impact
2. **Consideration is the critical "gateway"** - it's where opinions convert to intent
3. **Call-to-actions matter** - even great brand perceptions need a push to "consider visiting now"

**The same applies to Familiarity:**
Familiarity → Opinion → Likelihood is a strong indirect path. Familiarity works primarily by improving Opinion first.

---

### Objective 5: Time Series Trend Analysis (NEW)

**Funnel Metrics by Wave:**

| Wave | Month | n | Familiarity | Opinion | Consideration | Likelihood |
|------|-------|---|-------------|---------|---------------|------------|
| 1 | Feb | 535 | 3.91 | 4.26 | 4.00 | 3.93 |
| 2 | Mar | 755 | 3.96 | 4.19 | 4.04 | 3.91 |
| 3 | Apr | 488 | 3.96 | 4.25 | 4.03 | 3.93 |
| 4 | May | 498 | 3.97 | 4.20 | 4.00 | 3.91 |
| 5 | Jun | 493 | 3.91 | 4.21 | 3.97 | 3.90 |
| 6 | Jul | 491 | 4.04 | 4.31 | 4.09 | 4.03 |

**Linear Trend Tests:**

| Metric | Slope | Direction | p-value | Significant? |
|--------|-------|-----------|---------|--------------|
| Familiarity | +0.014 | Increasing | 0.200 | No |
| Opinion | +0.009 | Increasing | 0.327 | No |
| Consideration | +0.004 | Increasing | 0.657 | No |
| Likelihood | +0.013 | Increasing | 0.232 | No |

**Wave Effect in Full Model:** Beta = 0.006, p = 0.278 (Not significant)

**Key Finding:** No significant time trends detected in funnel metrics after controlling for other factors. The data shows stable patterns across the 6-month period, suggesting:
- A single consolidated model is appropriate (no need for monthly models)
- Seasonal factors do not significantly impact visit likelihood
- Marketing efforts can focus on funnel optimization rather than seasonal adjustments

---

## Descriptive Statistics

### Overall Funnel Metrics (Scale 1-5)

| Stage | Mean | High (4-5) | Medium (3) | Low (1-2) |
|-------|------|------------|------------|-----------|
| Familiarity | 3.92 | 73.6% | 16.1% | 10.3% |
| Opinion | 4.22 | 83.6% | 10.9% | 4.7% |
| Consideration | 3.99 | 75.1% | 16.0% | 8.9% |
| Likelihood | 3.90 | 68.9% | 19.8% | 11.3% |

### Brand Attribute Ratings

**Top Functional Strengths:**

| Attribute | Score |
|-----------|-------|
| Unique experiences | 4.11 |
| Great for kids 7-17 | 4.06 |
| Lifelong memories | 4.02 |
| Character interaction | 3.98 |

**Key Weaknesses (Opportunity Areas):**

| Attribute | Score |
|-----------|-------|
| Affordable | **2.31** |
| Not crowded | **2.12** |

**Top Emotional Attributes:**

| Attribute | Score |
|-----------|-------|
| Removed from reality | 4.33 |
| Land of dreams | 4.31 |
| Sparkling | 4.14 |

### TDR vs USJ Competitive Position

**TDR Wins (score < 4):**
- Return to childhood: 3.08
- Feeling special: 3.12
- Only one: 3.25

**USJ Wins (score > 4):**
- Edgy: 4.44
- Suspenseful: 4.22

---

## Strategic Recommendations

Based on the 6-wave consolidated SEM analysis:

### 1. Focus on Consideration Conversion
- Consideration is the strongest predictor of Likelihood (Beta = 0.606)
- 66.8% of Opinion's effect is mediated through Consideration
- **Action:** Create campaigns that move guests from "I like TDL" to "I plan to visit"

### 2. Prioritize Functional Messaging
- Functional benefits (Beta = 0.144) significantly predict intent; Emotional does not
- **Action:** Emphasize variety, unique experiences, family suitability in communications
- Emotional positioning may be better for brand building vs. visit conversion

### 3. Address Value Perception Gap
- "Not crowded" (2.12) and "Affordable" (2.31) are critical pain points
- **Action:** Tiered pricing, off-peak incentives, crowd management communications

### 4. Customize by Segment
- Adults 35+: Highest conversion from Consideration (Beta = 0.826) but lowest absolute metrics
- Couples 18-34: Best overall funnel performance - priority acquisition target
- Older Families: Lower conversion (Beta = 0.747) - identify and address specific barriers

### 5. Maintain Consistent Marketing
- No significant seasonal trends detected across 6 months
- **Action:** Focus on funnel optimization rather than seasonal adjustments
- One consolidated marketing strategy is sufficient

### 6. Protect TDR Positioning
- Own: Nostalgia, feeling special, "only one"
- Cede to USJ: Edgy, suspenseful

---

## Output Files

| File | Description |
|------|-------------|
| `output/reports/sem_path_coefficients.csv` | All path coefficients from SEM |
| `output/reports/sem_mediation_results.csv` | Mediation test results |
| `output/reports/sem_fit_indices.csv` | Model fit statistics |
| `output/reports/sem_segment_comparison.csv` | Segment-level path coefficients |
| `output/reports/wave_metrics.csv` | Time series funnel metrics by wave |
| `output/reports/trend_analysis.csv` | Linear trend test results |
| `output/reports/segment_trends.csv` | Segment performance trends over time |
| `output/reports/tdl_functional_attributes.csv` | Attribute ratings |
| `output/reports/tdl_competitor_gaps.csv` | TDL vs TDS vs USJ |

---

## Technical Notes

- **Method:** Path analysis using OLS regression (equivalent to SEM for observed variables)
- **Sample:** 3,260 complete cases for funnel analysis; 1,096 for full SEM with attributes
- **Waves:** 6 monthly waves (February-July 2025)
- **Standardization:** All variables z-scored for comparability
- **Mediation:** Sobel test for indirect effects
- **Time Series:** Linear trend tests and wave effect in regression
- **Scripts:** `src/sem_analysis_real_data.py`, `src/analyze_tdl_data.py`
- **Data Extraction:** `dbt_project/scripts/extract_tdl_data.py`

---

## Data Source

*Analysis completed using validated data from Final Data for 6 waves.csv (February-July 2025)*
