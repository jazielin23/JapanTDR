# Japan Market Analysis - TDL Brand Tracking Study

A comprehensive analytical framework for analyzing Japan theme park market survey data using **Structural Equation Modeling (SEM)** and marketing funnel analysis.

---

## 📌 Research Objectives

This study addresses four key research objectives:

| # | Objective | Description |
|---|-----------|-------------|
| **1** | **Marketing Funnel Analysis** | Understand how funnel KPIs (Familiarity → Opinion → Consideration → Likelihood) drive intent to visit/return |
| **2** | **Brand Benefits Analysis** | Analyze how functional and emotional brand perceptions influence visit intent |
| **3** | **Segment Comparison** | Compare marketing effectiveness across demographic segments |
| **4** | **Mediation Testing** | Test indirect effects within the funnel (e.g., does Consideration mediate the Opinion → Likelihood relationship?) |

---

## 📋 Sample Structure

### Overview

- **Total Sample**: n = 541 respondents (177 with complete data for SEM)
- **Focus**: Tokyo Disneyland (TDL) / Tokyo Disney Resort (TDR)
- **Geography**: Local (Greater Tokyo + major prefectures) and Domestic (all other prefectures)

### Demographic Segments

| Segment | Description | Sample n | Mean Age | % of Total |
|---------|-------------|----------|----------|------------|
| A. Young Families | Families with child < 6 years | 109 | 36.0 | 20.1% |
| B. Older Families | Families with child 7-17 years | 117 | 46.3 | 21.6% |
| C. Adults 18-34 | Single adults 18-34, no kids in HH | 102 | 26.5 | 18.9% |
| D. Couples 18-34 | Partnered adults 18-34, no kids in HH | 93 | 29.7 | 17.2% |
| E. Adults 35+ | Adults 35+, no kids in HH | 119 | 57.2 | 22.0% |

---

## 📏 Measurement Definitions

### How Each Metric Relates to Research Objectives

| Measurement | Scale | Objective(s) Used In | Role in Analysis |
|-------------|-------|---------------------|------------------|
| Unaided Awareness | Open-ended text | Descriptive | Top-of-mind brand salience; binary (mentioned/not mentioned) |
| Aided Awareness | Binary (Yes/No) | Descriptive | Brand recognition; binary limits use in SEM path models |
| Familiarity | 1-5 Likert | 1, 2, 3, 4 | Upper funnel predictor; starting point of SEM path model |
| Opinion | 1-5 Likert | 1, 2, 3, 4 | Upper-middle funnel; key driver of consideration |
| Consideration to Visit | 1-5 Likert | 1, 2, 3, 4 | Middle funnel; primary mediator between opinion and likelihood |
| Likelihood to Visit | 1-5 Likert | 1, 2, 3, 4 | Lower funnel; primary outcome variable in all SEM models |
| Future Visitation Intent | Time-based categories | Descriptive | Visit timing indicator; recoded to binary for validation |
| Net Promoter Score (NPS) | 0-10 scale | 3 | Loyalty/advocacy measure; compared across segments |
| Functional Benefits | 1-5 Likert (26 items) | 2 | Rational brand perceptions; tested as predictors of likelihood |
| Emotional Benefits | 1-5 Likert (10 items) | 2 | Affective brand perceptions; tested as predictors of likelihood |

> **Note on Awareness**: This survey measures awareness as binary (Unaided = open-ended recall, Aided = yes/no recognition) rather than a Likert scale. Because nearly all respondents are aware of TDL (a famous Japanese brand), there is minimal variance in awareness. The SEM path model therefore begins at **Familiarity**, which captures the *depth* of brand knowledge on a continuous scale and provides meaningful variance for analysis.

---

### Detailed Measurement Descriptions

#### Marketing Funnel Metrics

**Unaided Awareness**
- **Question**: "What theme parks come to mind?" (open-ended, up to 5 responses)
- **Scale**: Text responses converted to binary (1 = TDL/TDR mentioned, 0 = not mentioned)
- **Limitation**: Not a Likert scale; cannot be used as continuous variable in SEM
- **Use**: Measures spontaneous top-of-mind awareness without prompting

**Aided Awareness**
- **Question**: "Are you aware of the following theme parks?" (checklist including TDL, TDS, USJ, Fuji-Q Highland, Ghibli Park, LEGOLAND, Nagashima Spaland)
- **Scale**: Binary (1 = Yes aware, 0 = Not aware)
- **Limitation**: Binary variable limits use in path models; for TDL, near-ceiling effect (most respondents aware)
- **Use**: Measures recognition when brand name is provided; used as filter/descriptive

**Familiarity**
- **Question**: "How familiar are you with [TDL]?"
- **Scale**: 5-point Likert
  - 5 = Very familiar
  - 4 = Familiar
  - 3 = Can't say either way
  - 2 = Not familiar
  - 1 = Not familiar at all
- **Use**: Upper funnel metric; measures depth of brand knowledge

**Opinion**
- **Question**: "What is your overall opinion of [TDL]?"
- **Scale**: 5-point Likert
  - 5 = Excellent
  - 4 = Good
  - 3 = Neutral
  - 2 = Bad
  - 1 = Very bad
- **Use**: Upper-middle funnel metric; measures overall brand sentiment

**Consideration to Visit**
- **Question**: "Would you consider visiting [TDL]?"
- **Scale**: 5-point Likert
  - 5 = Would definitely consider
  - 4 = Would consider
  - 3 = Might or might not consider
  - 2 = Would not consider
  - 1 = Would not consider at all
- **Use**: Middle funnel metric; key mediator between opinion and likelihood

**Likelihood to Visit**
- **Question**: "How likely are you to visit [TDL]?"
- **Scale**: 5-point Likert
  - 5 = Definitely likely to go
  - 4 = Likely to go
  - 3 = Might or might not go
  - 2 = Not likely to go
  - 1 = Definitely not likely to go
- **Use**: Lower funnel metric; primary outcome variable in SEM models

**Future Visitation Intent**
- **Question**: "When are you most likely to go to [TDL]?"
- **Scale**: Time-based categories
  - 1 = Within 1 month
  - 2 = Within 2 months
  - 3 = Within 3 months
  - 4 = Within 4-6 months
  - 5 = Within 7-9 months
  - 6 = Within 10-12 months
  - 7 = Not in the next 12 months
  - 8 = Have not decided yet
- **Calculation**: Recoded to binary (1-6 = Yes intent within 12 months, 7-8 = No intent)
- **Use**: Behavioral intent indicator

**Net Promoter Score (NPS)**
- **Question**: "How likely are you to recommend [TDL] to a friend or colleague?"
- **Scale**: 0-10 scale
- **Calculation**: 
  - Promoters (9-10): Loyal enthusiasts
  - Passives (7-8): Satisfied but unenthusiastic
  - Detractors (0-6): Unhappy customers
  - NPS = % Promoters - % Detractors
- **Use**: Loyalty and advocacy metric

---

#### Brand Benefits Metrics

**Functional Benefits of a Brand**
- **Question**: "To what extent do the following describe [TDL]?" (26 functional attributes)
- **Scale**: 5-point Likert (5 = High/Strongly Agree, 1 = Low/Strongly Disagree)
- **Attributes include**:
  - Relaxing
  - Is a place where I can enjoy myself
  - Builds lifelong special memories
  - Allows me to bond with family and/or friends
  - Is a great experience for younger kids under 6 years old
  - Is a great experience for older kids between 7 and 17 years old
  - Is a great experience for adults
  - Is something I want my children/grandchildren to experience
  - Is going to expand my child's/grandchild's worldview
  - Is a great experience for all family or party members
  - Understands the kind of things that I like
  - Makes me feel comfortable, as if I am with friends
  - Keeping up with the times
  - Offers a variety of things to do
  - Offers experiences not available anywhere else
  - Is an experience I like to do over and over again
  - Offers active and adventurous experiences
  - Offers thrilling experiences
  - Offers new, innovative experiences
  - Always has something new to see and do
  - Is not overly crowded
  - Is a place where we can interact with our favorite movie or story characters
  - Is a place worth visiting for a short vacation of 1-2 nights
  - Worth the price to go
  - Is affordable (is within a price range that I can afford)
  - Offers multiple types of tickets that meet specific needs
- **Calculation**: Mean score across all functional items per respondent
- **Use**: Tests whether rational/practical brand perceptions drive visit intent

**Emotional Benefits of a Brand**
- **Question**: "To what extent do the following emotional words describe [TDL]?" (10 emotional attributes)
- **Scale**: 5-point Likert (5 = High/Strongly Agree, 1 = Low/Strongly Disagree)
- **Attributes include**:
  - Land of dreams
  - Removed from reality
  - Fantastical
  - Heartwarming
  - Soothing/healing
  - Feeling safe
  - Longing/Aspiring
  - Sparkling
  - Premium feeling
  - Feel good
- **Calculation**: Mean score across all emotional items per respondent
- **Use**: Tests whether affective/experiential brand perceptions drive visit intent

---

## 📊 Results by Objective

### Objective 1: Marketing Funnel Analysis

**Research Question**: How do funnel KPIs drive intent to visit?

**Path Model**: Familiarity → Opinion → Consideration → Likelihood

| Path | Standardized β | p-value | Significance |
|------|---------------|---------|--------------|
| Familiarity → Opinion | **0.658** | < 0.001 | *** |
| Opinion → Consideration | **0.382** | < 0.001 | *** |
| Familiarity → Consideration (direct) | 0.425 | < 0.001 | *** |
| Consideration → Likelihood | **0.573** | < 0.001 | *** |
| Opinion → Likelihood (direct) | 0.239 | < 0.001 | *** |
| Familiarity → Likelihood (direct) | 0.053 | 0.440 | ns |

**Model Fit**: R² = 0.627 (62.7% of variance in Likelihood explained)

**Path Diagram**:
```
Familiarity ──(0.66)──► Opinion ──(0.38)──► Consideration ──(0.57)──► Likelihood
     │                      │                                            ▲
     │                      └─────────(0.24)─────────────────────────────┘
     └────────────────────(ns)────────────────────────────────────────────┘
```

**Key Finding**: Consideration is the strongest direct predictor of Likelihood (β = 0.573). The funnel flows sequentially, with each stage significantly predicting the next. Familiarity's effect on Likelihood is fully mediated through Opinion and Consideration.

---

### Objective 2: Brand Benefits Analysis

**Research Question**: Do functional and emotional brand perceptions influence visit intent?

**Model**: Likelihood ~ Funnel Metrics + Functional Benefits + Emotional Benefits

| Predictor | Standardized β | p-value | Significance |
|-----------|---------------|---------|--------------|
| Consideration | 0.463 | < 0.001 | *** |
| **Functional Benefits** | **0.305** | 0.003 | ** |
| Opinion | 0.113 | 0.122 | ns |
| Familiarity | 0.054 | 0.410 | ns |
| **Emotional Benefits** | -0.022 | 0.817 | ns |

**Full Model Fit**: R² = 0.663 (66.3% of variance in Likelihood explained)

**Key Finding**: **Functional benefits significantly predict Likelihood** (β = 0.305, p = 0.003), while Emotional benefits do not add incremental predictive power beyond the funnel metrics. This suggests that for TDL, **functional messaging** (variety, unique experiences, family suitability) may be more effective than emotional messaging for driving visit intent.

**Top Functional Strengths (Mean Score)**:
| Attribute | Score |
|-----------|-------|
| Unique experiences | 4.13 |
| Great for kids 7-17 | 4.10 |
| Lifelong memories | 4.09 |
| Character interaction | 4.08 |

**Key Weaknesses (Opportunity Areas)**:
| Attribute | Score |
|-----------|-------|
| Affordable | **2.12** |
| Not crowded | **2.01** |

**Top Emotional Attributes (Mean Score)**:
| Attribute | Score |
|-----------|-------|
| Land of dreams | 4.41 |
| Removed from reality | 4.39 |
| Sparkling | 4.18 |

---

### Objective 3: Segment Comparison

**Research Question**: Does the Consideration → Likelihood relationship vary by segment?

**Path Coefficient (Consideration → Likelihood) by Segment**:

| Segment | n | β | p-value | R² |
|---------|---|---|---------|---|
| A. Young Families | 38 | **0.869** | < 0.001 | 0.443 |
| D. Couples 18-34 | 32 | 0.857 | < 0.001 | 0.779 |
| C. Adults 18-34 | 30 | 0.852 | < 0.001 | 0.646 |
| E. Adults 35+ | 37 | 0.792 | < 0.001 | 0.761 |
| B. Older Families | 40 | **0.559** | < 0.001 | 0.304 |

**Funnel Metrics by Segment (Mean Scores)**:

| Segment | Familiarity | Opinion | Consideration | Likelihood | NPS |
|---------|-------------|---------|---------------|------------|-----|
| A. Young Families | 3.92 | 4.29 | 4.17 | 3.99 | 8.81 |
| B. Older Families | 3.69 | 4.13 | 3.87 | 3.80 | 8.11 |
| C. Adults 18-34 | 3.88 | 4.33 | 4.03 | 4.03 | 8.53 |
| D. Couples 18-34 | 4.11 | 4.32 | 4.22 | 4.22 | 8.82 |
| E. Adults 35+ | 3.83 | 4.16 | 3.65 | 3.55 | 7.88 |

**Key Findings**:
- **Strongest effect**: Young Families (β = 0.869) - When this segment considers visiting, they're very likely to follow through
- **Weakest effect**: Older Families (β = 0.559) - Consideration doesn't convert as strongly to intent; other barriers may exist (e.g., scheduling, competing activities for older children)
- **Highest overall intent**: Couples 18-34 (Likelihood = 4.22, NPS = 8.82)
- **Lowest overall intent**: Adults 35+ (Likelihood = 3.55, NPS = 7.88)

---

### Objective 4: Mediation Testing

**Research Question**: Is the effect of funnel stages on Likelihood mediated through Consideration?

#### Test 1: Does Consideration Mediate Opinion → Likelihood?

| Component | Value |
|-----------|-------|
| Path a (Opinion → Consideration) | 0.661 |
| Path b (Consideration → Likelihood) | 0.596 |
| Direct Effect c' (Opinion → Likelihood) | 0.259 |
| Indirect Effect (a × b) | **0.394** |
| Sobel z | 7.431 |
| p-value | < 0.001 |
| **% Mediated** | **60.3%** |

**Result**: Significant **partial mediation**. 60.3% of Opinion's effect on Likelihood flows through Consideration. Both direct and indirect paths are significant.

#### Test 2: Does Opinion Mediate Familiarity → Likelihood?

| Component | Value |
|-----------|-------|
| Indirect Effect (Familiarity → Opinion → Likelihood) | **0.301** |
| Sobel z | 5.523 |
| p-value | < 0.001 |

**Result**: Significant mediation. Opinion mediates Familiarity's effect on Likelihood.

**Mediation Diagram**:
```
                    Opinion
                   ↗       ↘
               (0.66)    (0.26 direct)
              ↗               ↘
Familiarity ────────────────────► Likelihood
                     (ns)              ▲
                                       │
         Consideration ─────(0.60)─────┘
              ▲
              │
    Opinion ──┘ (0.66)
```

**Strategic Implication**: Building favorable **Opinion** is the most effective upper-funnel strategy because it has both direct effects on Likelihood AND substantial indirect effects through Consideration. Marketing efforts should focus on shaping positive brand perceptions, which will naturally move consumers into the consideration set.

---

## 💡 Strategic Recommendations

Based on the SEM analysis:

### 1. Focus on Consideration Conversion
- Consideration is the strongest predictor of Likelihood (β = 0.573)
- 60% of Opinion's effect is mediated through Consideration
- **Action**: Create campaigns that move guests from "I like TDL" to "I plan to visit"

### 2. Prioritize Functional Messaging
- Functional benefits (β = 0.305) significantly predict intent; Emotional (β = -0.02) does not
- **Action**: Emphasize variety, unique experiences, family suitability in communications
- Emotional positioning may be better for brand building vs. visit conversion

### 3. Address Value Perception Gap
- "Not crowded" (2.01) and "Affordable" (2.12) are critical pain points
- **Action**: Tiered pricing, off-peak incentives, crowd management communications

### 4. Customize by Segment
- **Young Families**: High conversion from Consideration (β = 0.869) - focus on acquisition
- **Older Families**: Lower conversion (β = 0.559) - identify and address specific barriers

### 5. Build Upper Funnel Through Opinion
- Opinion is the key lever - it directly influences Likelihood AND drives Consideration
- **Action**: Invest in brand-building campaigns that shape positive perceptions

---

## 📁 Project Structure

```
japan_market_analysis/
├── data/
│   ├── raw/                    # Raw survey data files
│   │   ├── japan_market_survey_complete.csv
│   │   ├── survey_M01.csv through survey_M10.csv
│   │   └── data_dictionary.csv
│   └── processed/              # Cleaned and prepared data
│       ├── survey_processed.csv
│       └── aggregated files
├── src/
│   ├── 00_config.R             # Configuration and constants
│   ├── 01_generate_data.R      # Simulated data generation
│   ├── 02_data_preparation.R   # Data cleaning and preparation
│   ├── 03_sem_analysis.R       # SEM/CFA analysis (lavaan)
│   ├── 04_visualization.R      # Visualization functions
│   ├── 05_main_analysis.R      # Complete analysis workflow
│   ├── sem_analysis_real_data.py # SEM with real data
│   └── analyze_tdl_data.py     # Descriptive statistics
├── output/
│   ├── figures/                # Generated plots and diagrams
│   └── reports/                # Analysis results and tables
├── Relabeled Raw Data.csv      # Source survey data
└── README.md                   # This file
```

---

## 🚀 Running the Analysis

### Prerequisites
- Python 3.8+ with pandas, numpy, scipy, statsmodels
- R 4.0+ with lavaan, tidyverse (optional for R-based analysis)

### Quick Start
```bash
cd japan_market_analysis

# Run SEM analysis with real data
python3 src/sem_analysis_real_data.py

# Run descriptive statistics
python3 src/analyze_tdl_data.py
```

---

## 📊 Output Files

### Reports (`output/reports/`)
| File | Description |
|------|-------------|
| `sem_path_coefficients.csv` | All path coefficients from SEM |
| `sem_mediation_results.csv` | Mediation test results |
| `sem_fit_indices.csv` | Model fit statistics |
| `sem_segment_comparison.csv` | Segment-level path coefficients |
| `tdl_funnel_by_segment.csv` | Funnel metrics by segment |
| `tdl_functional_attributes.csv` | Functional attribute ratings |
| `tdl_emotional_attributes.csv` | Emotional attribute ratings |
| `tdl_competitor_gaps.csv` | TDL vs TDS vs USJ comparison |

### Figures (`output/figures/`)
| File | Description |
|------|-------------|
| `readme_funnel.png` | Overall funnel performance |
| `readme_funnel_region.png` | Funnel comparison by region |
| `readme_benefits_heatmap.png` | Benefits by segment heatmap |
| `readme_path_coefficients.png` | SEM path coefficients |
| `readme_segment_intent.png` | Intent by segment |

---

## 📚 References

- Baron, R. M., & Kenny, D. A. (1986). The moderator-mediator variable distinction in social psychological research.
- Sobel, M. E. (1982). Asymptotic confidence intervals for indirect effects in structural equation models.
- Rosseel, Y. (2012). lavaan: An R Package for Structural Equation Modeling. *Journal of Statistical Software*, 48(2), 1-36.

---

*Analysis completed using validated data from Japan Theme Park Brand Tracking Survey*
