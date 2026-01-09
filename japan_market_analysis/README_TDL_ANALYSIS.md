# Tokyo Disneyland (TDL) Brand Tracking Analysis

## 📊 Overview

This analysis uses **real survey data** from the Japan Theme Park Brand Tracking Study. The data has been validated and extracted using the official variable definitions from the **Relabeled Raw Data.csv**.

**Focus:** Tokyo Disneyland (TDL) with competitive benchmarks against TDS and USJ.

---

## 🔬 Scale Mappings (Validated)

All scales confirmed from the official relabeled data:

| Scale Type | Range | Interpretation |
|------------|-------|----------------|
| **Likert 5-point** | 1-5 | 5=High/Positive, 1=Low/Negative |
| **Bipolar TDR vs USJ** | 1-7 | 1=Definitely TDR, 4=Neutral, 7=Definitely USJ |
| **NPS** | 0-10 | 9-10=Promoter, 7-8=Passive, 0-6=Detractor |

---

## 📈 Key Findings

### 1. Sample Overview

| Segment | n | % | Mean Age |
|---------|---|---|----------|
| A. Young Families | 109 | 20.1% | 36.0 |
| B. Older Families | 117 | 21.6% | 46.3 |
| C. Adults 18-34 (no kids) | 102 | 18.9% | 26.5 |
| D. Couples 18-34 (no kids) | 93 | 17.2% | 29.7 |
| E. Adults 35+ (no kids) | 119 | 22.0% | 57.2 |
| **Total** | **541** | **100%** | |

### 2. TDL Marketing Funnel

| Stage | Mean Score | High (4-5) | Medium (3) | Low (1-2) |
|-------|------------|------------|------------|-----------|
| Familiarity | 3.87 | 72.1% | 17.0% | 10.9% |
| Opinion | 4.24 | 86.3% | 8.9% | 4.3% |
| Consideration | 3.97 | 72.8% | 17.9% | 9.2% |
| Likelihood | 3.90 | 67.8% | 21.4% | 10.7% |

**Insight:** Strong Opinion scores (86% positive) but slight drop-off in Consideration and Likelihood conversion.

### 3. Segment Performance

Ranked by Likelihood to Visit:

| Rank | Segment | Likelihood | Consideration | NPS |
|------|---------|------------|---------------|-----|
| 1 | D. Couples 18-34 | **4.22** | 4.22 | 8.82 |
| 2 | C. Adults 18-34 | 4.03 | 4.03 | 8.53 |
| 3 | A. Young Families | 3.99 | 4.17 | 8.81 |
| 4 | B. Older Families | 3.80 | 3.87 | 8.11 |
| 5 | E. Adults 35+ | **3.55** | 3.65 | 7.88 |

**Insight:** Young Couples are the highest-intent segment; Adults 35+ show the lowest intent and NPS.

### 4. Brand Attribute Ratings

**Top Functional Attributes (Scale 1-5):**

| Attribute | Score | Interpretation |
|-----------|-------|----------------|
| Unique experiences | 4.13 | ★★★★☆ |
| Great for kids 7-17 | 4.10 | ★★★★☆ |
| Lifelong memories | 4.09 | ★★★★☆ |
| Character interaction | 4.08 | ★★★★☆ |
| Want children to experience | 4.03 | ★★★★☆ |

**Bottom Functional Attributes (Opportunity Areas):**

| Attribute | Score | Interpretation |
|-----------|-------|----------------|
| Thrilling | 3.54 | ★★★★☆ |
| Ticket options | 3.41 | ★★★☆☆ |
| Relaxing | 3.37 | ★★★☆☆ |
| **Affordable** | **2.12** | ★★☆☆☆ |
| **Not crowded** | **2.01** | ★★☆☆☆ |

**Insight:** Crowding and affordability are significant pain points.

**Top Emotional Attributes:**

| Attribute | Score |
|-----------|-------|
| Land of dreams | 4.41 |
| Removed from reality | 4.39 |
| Sparkling | 4.18 |
| Fantastical | 4.09 |
| Feel good | 4.07 |

**Insight:** TDL excels at escapism and fantasy - core emotional differentiators.

### 5. Key Drivers of Likelihood

| Driver | Correlation (r) |
|--------|-----------------|
| Consideration | 0.798 |
| NPS | 0.715 |
| Functional Mean | 0.708 |
| Opinion | 0.682 |
| Familiarity | 0.641 |
| Emotional Mean | 0.632 |

**Insight:** Consideration is the strongest predictor - focus on moving guests from Opinion to Consideration.

### 6. TDR vs USJ Comparison

**TDL/TDR Strengths (Score < 4 = TDR preferred):**

| Attribute | Score | Advantage |
|-----------|-------|-----------|
| Return to childhood | 3.17 | Strong TDR |
| Feeling special | 3.20 | Strong TDR |
| Only one | 3.36 | Moderate TDR |
| Relaxed/content | 3.54 | Moderate TDR |
| Fun | 3.56 | Moderate TDR |

**USJ Strengths (Score > 4 = USJ preferred):**

| Attribute | Score | Advantage |
|-----------|-------|-----------|
| Edgy | 4.66 | Strong USJ |
| Suspenseful | 4.45 | Moderate USJ |
| Unpredictability | 4.13 | Slight USJ |
| Feel refreshed | 4.09 | Slight USJ |
| Innovative | 4.00 | Neutral |

**Insight:** TDR owns nostalgia, warmth, and feeling special; USJ owns edgy, suspense, and innovation.

### 7. Competitive Funnel Gaps

| Metric | TDL | TDS | USJ | TDL vs USJ |
|--------|-----|-----|-----|------------|
| Familiarity | 3.87 | 3.77 | 3.50 | **+0.37** |
| Opinion | 4.24 | 4.18 | 4.09 | +0.15 |
| Consideration | 3.97 | 3.93 | 3.81 | +0.16 |
| Likelihood | 3.90 | 3.87 | 3.81 | +0.09 |

**Insight:** TDL leads on all funnel stages, with largest advantage in Familiarity (+0.37).

---

## 📁 Output Files

| File | Description |
|------|-------------|
| `output/reports/tdl_segment_summary.csv` | Sample breakdown by segment |
| `output/reports/tdl_funnel_by_segment.csv` | Funnel metrics by segment |
| `output/reports/tdl_segment_performance.csv` | Full performance comparison |
| `output/reports/tdl_competitor_gaps.csv` | TDL vs TDS vs USJ comparison |
| `output/reports/tdl_functional_attributes.csv` | All functional attribute ratings |
| `output/reports/tdl_emotional_attributes.csv` | All emotional attribute ratings |

---

## 💡 Strategic Recommendations

1. **Address Value Perception Gap**
   - "Not crowded" (2.01) and "Affordable" (2.12) are critical weaknesses
   - Consider tiered pricing, off-peak incentives, or crowd management communications

2. **Leverage Emotional Differentiators**
   - "Land of dreams" (4.41) and "Removed from reality" (4.39) are TDL's strongest assets
   - Double down on escapism and fantasy in marketing messaging

3. **Target High-Intent Segments**
   - Couples 18-34 show highest likelihood (4.22) - ideal for acquisition campaigns
   - Adults 35+ need different approach - address their specific barriers

4. **Protect TDR Positioning**
   - Own: Nostalgia ("Return to childhood"), Emotional warmth ("Feeling special")
   - Cede to USJ: Edgy, suspenseful experiences

5. **Focus on Consideration Conversion**
   - Opinion (86% positive) → Consideration (73% positive) shows 13% drop
   - Address barriers that prevent positive opinion from converting to action

---

## 🔧 Technical Notes

- **Data Source:** `Relabeled Raw Data.csv` (official variable definitions)
- **Missing Values:** 0 and 99 treated as missing
- **Attribute Ratings:** 177 respondents (subset who answered detailed questions)
- **Analysis Script:** `src/analyze_tdl_data.py`

---

*Last Updated: Based on TDL Brand Tracking Survey Analysis*
