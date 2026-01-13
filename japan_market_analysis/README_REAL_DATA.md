# Japan Market Analysis - Real Data Results

## Overview

This analysis applies the SEM (Structural Equation Modeling) framework developed with synthetic data to the **actual Brand Tracking Survey 2025 Wave 11 data** (n=500).

## Data Processing

### Raw Data → Analysis Format Mapping

| Raw Data Column | Mapped Variable | Description |
|-----------------|-----------------|-------------|
| Quota | segment | Demographic segment (Young Families, Matured Families, etc.) |
| SC3 | region | Local (Tokyo + 7 prefectures) vs. Domestic |
| SC1 | gender | Male/Female |
| SC2 | age | Age in years |
| Q1-1 | awareness | Brand awareness for TDR (1-7 scale) |
| Q2-1 | familiarity | Brand familiarity for TDR (1-7 scale) |
| Q3-1 | opinion | Favorable opinion for TDR (1-7 scale) |
| Q4-1 | consideration | Consideration for visit (1-7 scale) |
| Q5-1 | likelihood | Likelihood to visit (1-7 scale) |
| Q7/Q8 1-38 | func_*/emot_* | Brand attribute items → Functional/Emotional benefits |

### Brand Attribute Mapping

The 38 brand attribute items (Q7/Q8/Q9) were mapped to functional and emotional benefit constructs:

**Functional Benefits:**
- `func_convenience`: Crowding, flexibility, customization
- `func_value`: Worth the price, affordability, price points
- `func_quality`: Unique experiences, vacation-worthy
- `func_variety`: Variety of things to do
- `func_reliability`: Feeling safe

**Emotional Benefits:**
- `emot_excitement`: Active/adventurous, thrilling, innovative experiences
- `emot_relaxation`: Escape from everyday, relaxing, soothing
- `emot_connection`: Welcoming, bonding, comfortable, heart warming
- `emot_authenticity`: Land of dreams, fantastical, removed from reality
- `emot_memorable`: Lifelong special memories

---

## Key Findings from Real Data

### 1. Sample Characteristics

- **Total Sample**: n=500 (Wave 11)
- **Segment Distribution**: 100 per segment (Young Families, Matured Families, Young Adults, Young Couples, Matured Adults 35+)
- **Regional Distribution**: 65% Local, 35% Domestic

### 2. Scale Reliability (Cronbach's Alpha)

| Scale | Alpha | Interpretation |
|-------|-------|----------------|
| Marketing Funnel | α = 0.707 | Acceptable |
| Functional Benefits | α = 0.856 | Good |
| Emotional Benefits | α = 0.905 | Excellent |

### 3. Funnel Performance

| Stage | Mean | SD |
|-------|------|-----|
| Awareness | 5.35 | 1.55 |
| Familiarity | 5.86 | 1.27 |
| Opinion | 5.54 | 1.44 |
| Consideration | 5.32 | 1.61 |
| Likelihood | 6.84 | 1.84 |
| Intent | 6.08 | 1.04 |

**Key Insight**: High familiarity (5.86) and likelihood (6.84) scores indicate strong brand recognition and interest, but consideration (5.32) is relatively lower, suggesting a gap between interest and active planning.

### 4. Path Analysis Results

**Funnel Progression (Upper → Middle → Lower):**

| Path | β | p-value | Interpretation |
|------|---|---------|----------------|
| Upper → Middle Funnel | 0.784 | < 0.001 | Very strong relationship |
| Middle → Lower Funnel | 0.094 | 0.191 | Not significant |
| Upper → Lower Funnel | -0.137 | 0.058 | Marginally negative |

**Full Model - Drivers of Intent:**

| Predictor | β | p-value | Significance |
|-----------|---|---------|--------------|
| Consideration | 0.609 | < 0.001 | *** |
| Awareness | -0.145 | 0.021 | * |
| Functional Benefits | 0.089 | 0.391 | ns |
| Emotional Benefits | 0.035 | 0.730 | ns |
| Familiarity | -0.026 | 0.734 | ns |

**Model Fit**: R² = 0.377 (37.7% variance in intent explained)

### 5. Mediation Analysis

Testing: Does **consideration** mediate the relationship between **awareness** and **intent**?

| Effect | Value |
|--------|-------|
| Total effect (c) | 0.257 |
| Direct effect (c') | -0.149 |
| Indirect effect (a×b) | 0.406 |
| Proportion mediated | >100% |

**Interpretation**: Full mediation with suppression effect detected. Awareness has a **positive indirect effect** through consideration (people who are aware are more likely to consider, and consideration drives intent), but a **negative direct effect** when controlling for consideration. This suggests:

1. Awareness alone is not enough - it must translate into active consideration
2. Among those who are aware but NOT considering, higher awareness may indicate past negative experiences or barriers

### 6. Strategic Implications

Based on the real data analysis:

1. **Consideration is the Critical Driver**: With β = 0.609, consideration is by far the strongest predictor of intent. Marketing efforts should focus on converting awareness into active consideration.

2. **Benefits Have Limited Direct Effect**: Unlike the synthetic data, functional and emotional benefits do not show significant direct effects on intent in this sample. This may indicate:
   - Benefits influence earlier funnel stages (awareness → familiarity)
   - Benefits are "table stakes" - expected rather than differentiating
   - The sample already has high baseline benefit perceptions

3. **The "Awareness Trap"**: The negative direct effect of awareness on intent (when controlling for consideration) suggests that high awareness without consideration may indicate barriers to visit. Focus on converting aware non-considerers.

4. **Regional Focus**: Local region (65% of sample) has higher scores across all metrics - consider tailored strategies for the Domestic market.

---

## Files Generated

### Scripts
- `src/process_raw_data.py` - Transforms raw Excel to analysis format
- `src/sem_analysis.py` - Python-based path/mediation analysis

### Output
- `output/figures/readme_*.png` - Visualizations
- `output/reports/*.csv` - Statistical results
- `data/processed/survey_processed.csv` - Processed dataset

---

## Running the Analysis

```bash
# Step 1: Process raw data
cd japan_market_analysis
python3 src/process_raw_data.py

# Step 2: Run SEM/Path analysis
python3 src/sem_analysis.py
```

---

## Comparison: Synthetic vs. Real Data

| Aspect | Synthetic Data | Real Data |
|--------|---------------|-----------|
| Sample Size | 10,000 | 500 |
| Primary Driver of Intent | Consideration (β=0.17) | Consideration (β=0.61) |
| Benefits Effect | Significant | Not significant |
| Awareness Direct Effect | Positive | Negative (suppression) |
| Mediation | Partial | Full with suppression |

The real data shows a **stronger but more complex** relationship structure, with consideration playing an even more dominant role than in the synthetic data.
