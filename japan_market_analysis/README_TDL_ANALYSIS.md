# Tokyo Disneyland (TDL) Brand Tracking Analysis

## 📊 Overview

This analysis uses **real survey data** from the Japan Theme Park Brand Tracking Study, analyzed using **Structural Equation Modeling (SEM)** to test causal relationships in the marketing funnel.

**Sample:** 541 total respondents (177 with complete data for SEM)  
**Focus:** Tokyo Disneyland (TDL)  
**Scale Validation:** All Likert scales confirmed (5=High/Positive, 1=Low/Negative)

---

## 🔬 Research Objectives

1. **Marketing Funnel Analysis** - How funnel KPIs drive intent to visit
2. **Brand Benefits Analysis** - How functional vs emotional benefits influence intent
3. **Segment Comparison** - Compare path coefficients across demographic segments
4. **Mediation Testing** - Test indirect effects within the funnel

---

## 📈 SEM Results

### Objective 1: Marketing Funnel Analysis

**Path Model:** Familiarity → Opinion → Consideration → Likelihood

| Path | Standardized β | p-value | Significance |
|------|---------------|---------|--------------|
| Familiarity → Opinion | **0.658** | < 0.001 | *** |
| Opinion → Consideration | **0.382** | < 0.001 | *** |
| Familiarity → Consideration (direct) | 0.425 | < 0.001 | *** |
| Consideration → Likelihood | **0.573** | < 0.001 | *** |
| Opinion → Likelihood (direct) | 0.239 | < 0.001 | *** |
| Familiarity → Likelihood (direct) | 0.053 | 0.440 | ns |

**Model Fit:** R² = 0.627 (62.7% of variance in Likelihood explained)

**Key Finding:** Consideration is the strongest direct predictor of Likelihood (β = 0.573). The funnel flows sequentially with each stage significantly predicting the next.

```
Familiarity ──(0.66)──► Opinion ──(0.38)──► Consideration ──(0.57)──► Likelihood
     │                      │                                            ▲
     │                      └─────────(0.24)─────────────────────────────┘
     └────────────────────(ns)────────────────────────────────────────────┘
```

---

### Objective 2: Brand Benefits Analysis

**Testing:** Functional & Emotional Benefits → Likelihood

| Predictor | Standardized β | p-value | Significance |
|-----------|---------------|---------|--------------|
| Functional Benefits | **0.305** | 0.003 | ** |
| Emotional Benefits | -0.022 | 0.817 | ns |

**Full Model (Funnel + Benefits):** R² = 0.663

| Variable | β | p-value |
|----------|---|---------|
| Consideration | 0.463 | < 0.001 *** |
| Functional | 0.305 | 0.003 ** |
| Opinion | 0.113 | 0.122 |
| Familiarity | 0.054 | 0.410 |
| Emotional | -0.022 | 0.817 |

**Key Finding:** Functional benefits have a significant unique effect on Likelihood (β = 0.305, p = 0.003), while Emotional benefits do not add incremental predictive power beyond the funnel metrics. This suggests that for TDL, **functional messaging** (convenience, variety, value) may be more effective than emotional messaging for driving visit intent.

---

### Objective 3: Segment Comparison

**Path: Consideration → Likelihood by Segment**

| Segment | n | β | p-value | R² |
|---------|---|---|---------|---|
| A. Young Families | 38 | **0.869** | < 0.001 | 0.443 |
| D. Couples 18-34 | 32 | 0.857 | < 0.001 | 0.779 |
| C. Adults 18-34 | 30 | 0.852 | < 0.001 | 0.646 |
| E. Adults 35+ | 37 | 0.792 | < 0.001 | 0.761 |
| B. Older Families | 40 | **0.559** | < 0.001 | 0.304 |

**Key Finding:** 
- **Strongest effect:** Young Families (β = 0.869) - When this segment considers visiting, they're very likely to follow through
- **Weakest effect:** Older Families (β = 0.559) - Consideration doesn't convert as strongly to intent; other barriers may exist
- Path coefficients vary significantly by segment, supporting **targeted marketing approaches**

---

### Objective 4: Mediation Testing

**Test 1: Does Consideration mediate Opinion → Likelihood?**

| Component | Value |
|-----------|-------|
| Path a (Opinion → Consideration) | 0.661 |
| Path b (Consideration → Likelihood) | 0.596 |
| Direct Effect c' (Opinion → Likelihood) | 0.259 |
| Indirect Effect (a × b) | **0.394** |
| Sobel z | 7.431 |
| p-value | < 0.001 |
| **% Mediated** | **60.3%** |

**Result:** Significant **partial mediation**. 60.3% of Opinion's effect on Likelihood flows through Consideration. Both direct and indirect paths are significant.

**Test 2: Does Opinion mediate Familiarity → Likelihood?**

| Component | Value |
|-----------|-------|
| Indirect Effect | 0.301 |
| Sobel z | 5.523 |
| p-value | < 0.001 |

**Result:** Significant mediation. Opinion mediates Familiarity's effect on Likelihood.

---

## 📊 Descriptive Statistics

### Overall Funnel Metrics (Scale 1-5)

| Stage | Mean | High (4-5) | Medium (3) | Low (1-2) |
|-------|------|------------|------------|-----------|
| Familiarity | 3.87 | 72.1% | 17.0% | 10.9% |
| Opinion | 4.24 | 86.3% | 8.9% | 4.3% |
| Consideration | 3.97 | 72.8% | 17.9% | 9.2% |
| Likelihood | 3.90 | 67.8% | 21.4% | 10.7% |

### Brand Attribute Ratings

**Top Functional Strengths:**
| Attribute | Score |
|-----------|-------|
| Unique experiences | 4.13 |
| Great for kids 7-17 | 4.10 |
| Lifelong memories | 4.09 |
| Character interaction | 4.08 |

**Key Weaknesses (Opportunity Areas):**
| Attribute | Score |
|-----------|-------|
| Affordable | **2.12** |
| Not crowded | **2.01** |

**Top Emotional Attributes:**
| Attribute | Score |
|-----------|-------|
| Land of dreams | 4.41 |
| Removed from reality | 4.39 |
| Sparkling | 4.18 |

### TDR vs USJ Competitive Position

**TDR Wins (score < 4):**
- Return to childhood: 3.17
- Feeling special: 3.20
- Only one: 3.36

**USJ Wins (score > 4):**
- Edgy: 4.66
- Suspenseful: 4.45

---

## 💡 Strategic Recommendations

Based on the SEM analysis:

### 1. Focus on Consideration Conversion
- Consideration is the strongest predictor of Likelihood (β = 0.573)
- 60% of Opinion's effect is mediated through Consideration
- **Action:** Create campaigns that move guests from "I like TDL" to "I plan to visit"

### 2. Prioritize Functional Messaging
- Functional benefits (β = 0.305) significantly predict intent; Emotional (β = -0.02) does not
- **Action:** Emphasize variety, unique experiences, family suitability in communications
- Emotional positioning may be better for brand building vs. visit conversion

### 3. Address Value Perception Gap
- "Not crowded" (2.01) and "Affordable" (2.12) are critical pain points
- **Action:** Tiered pricing, off-peak incentives, crowd management communications

### 4. Customize by Segment
- Young Families: High conversion from Consideration (β = 0.869) - focus on acquisition
- Older Families: Lower conversion (β = 0.559) - identify and address specific barriers

### 5. Protect TDR Positioning
- Own: Nostalgia, feeling special, "only one"
- Cede to USJ: Edgy, suspenseful

---

## 📁 Output Files

| File | Description |
|------|-------------|
| `output/reports/sem_path_coefficients.csv` | All path coefficients from SEM |
| `output/reports/sem_mediation_results.csv` | Mediation test results |
| `output/reports/sem_fit_indices.csv` | Model fit statistics |
| `output/reports/sem_segment_comparison.csv` | Segment-level path coefficients |
| `output/reports/tdl_functional_attributes.csv` | Attribute ratings |
| `output/reports/tdl_competitor_gaps.csv` | TDL vs TDS vs USJ |

---

## 🔧 Technical Notes

- **Method:** Path analysis using OLS regression (equivalent to SEM for observed variables)
- **Sample:** 177 complete cases for SEM (attributes only asked of subset)
- **Standardization:** All variables z-scored for comparability
- **Mediation:** Sobel test for indirect effects
- **Scripts:** `src/sem_analysis_real_data.py`, `src/analyze_tdl_data.py`

---

## 📚 References

- Baron, R. M., & Kenny, D. A. (1986). The moderator-mediator variable distinction.
- Sobel, M. E. (1982). Asymptotic confidence intervals for indirect effects.

---

*Analysis completed using validated data from Relabeled Raw Data.csv*
