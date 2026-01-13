# TDL Survey Data Model

## Overview

This data model is built from the **Relabeled Raw Data.csv** which contains the official variable definitions from the brand tracking survey.

## Validated Scale Mappings

All scales have been verified against the source data definitions:

### 5-Point Likert Scales (HIGHER = BETTER)

| Score | Label |
|-------|-------|
| 5 | Very Positive (Excellent, Very Familiar, Definitely Would) |
| 4 | Positive (Good, Familiar, Would) |
| 3 | Neutral (Can't say either way, Might or might not) |
| 2 | Negative (Bad, Not familiar, Would not) |
| 1 | Very Negative (Very bad, Not at all familiar, Definitely would not) |

**Applies to:**
- Familiarity (TDL, TDS, USJ)
- Opinion (TDL, TDS, USJ)
- Consideration (TDL, TDS, USJ)
- Likelihood to Visit (TDL, TDS, USJ)
- All Functional Attributes (26 items per park)
- All Emotional Attributes (10 items per park)

### Bipolar Scales (TDR vs USJ)

| Score | Label |
|-------|-------|
| 1 | Definitely TDR |
| 2-3 | Lean TDR |
| 4 | Neutral |
| 5-6 | Lean USJ |
| 7 | Definitely USJ |

**For TDL/TDR analysis:** Lower scores = BETTER for Disney

### NPS Scale

| Score | Category |
|-------|----------|
| 9-10 | Promoter |
| 7-8 | Passive |
| 0-6 | Detractor |

### Visit Recency

| Code | Meaning |
|------|---------|
| 1 | Within last month |
| 2 | 2-3 months ago |
| 3 | 4-6 months ago |
| 4 | 7-12 months ago |
| 5 | 2 years ago |
| 6 | 3 years ago |
| 7 | 4-5 years ago |
| 8 | More than 6 years ago |
| 9 | Never visited |

---

## Model Architecture

```
seeds/
├── survey_responses_tdl.csv    # Extracted TDL-focused data (541 respondents)
└── data_dictionary.csv          # Column metadata and scale definitions

models/staging/
└── stg_survey_responses.sql     # Cleaned, typed, labeled survey data

models/marts/marketing/
├── fct_tdl_brand_funnel.sql         # Marketing funnel metrics
├── fct_tdl_attribute_perceptions.sql # 36 attribute ratings + composites
└── fct_tdr_vs_usj_comparison.sql    # Bipolar competitive analysis
```

---

## Key Columns by Category

### Demographics
- `segment_name`: A. Young Families, B. Older Families, C. Young Singles/Couples, D. Older Singles/Couples, E. Seniors
- `age_group`: 18-24, 25-34, 35-44, 45-54, 55-64, 65+
- `gender`: Male, Female
- `geography`: Local, Domestic

### Funnel Metrics (all 1-5 where 5=best)
- `familiarity_tdl`
- `opinion_tdl`
- `consideration_tdl`
- `likelihood_visit_tdl`
- `intent_visit_tdl_12mo` (binary)

### TDL Functional Attributes (26 items, 1-5)
Grouped into:
- **Experience Quality**: relaxing, enjoy_myself, lifelong_memories, bond_family_friends
- **Family Suitability**: great_for_kids_under_6, great_for_kids_7_17, great_for_adults, want_children_experience, expand_child_worldview, great_for_all_family
- **Innovation**: keeping_up_with_times, variety_of_things, unique_experiences, new_innovative, something_new
- **Excitement**: active_adventurous, thrilling, repeat_experience
- **Value**: worth_price, affordable, ticket_options
- **Other**: not_crowded, character_interaction, worth_short_vacation

### TDL Emotional Attributes (10 items, 1-5)
- land_of_dreams, removed_from_reality, fantastical, heartwarming, soothing_healing, feeling_safe, longing_aspiring, sparkling, premium_feeling, feel_good

### Bipolar Comparisons (19 items, 1-7)
- fun, feeling_special, anticipation, excitement, playful_mind, relaxed_content, only_one, oshi, return_childhood, trending, realism, innovative, unpredictability, refreshing_look, edgy, feel_refreshed, heart_throbbing, be_merry, suspenseful

---

## Composite Scores

The `fct_tdl_attribute_perceptions` model includes pre-calculated composite scores:

| Score | Description | Items |
|-------|-------------|-------|
| experience_quality_score | Core experience | 4 items |
| family_suitability_score | Family appeal | 6 items |
| innovation_score | Innovation perception | 4 items |
| excitement_score | Thrill/excitement | 3 items |
| value_perception_score | Value for money | 3 items |
| emotional_score | Emotional connection | 10 items |

---

## Sample Analysis Queries

### Funnel Conversion by Segment
```sql
select 
    segment_name,
    avg(familiarity_tdl) as avg_familiarity,
    avg(opinion_tdl) as avg_opinion,
    avg(consideration_tdl) as avg_consideration,
    avg(likelihood_visit_tdl) as avg_likelihood,
    avg(intent_visit_tdl_12mo) as intent_rate
from fct_tdl_brand_funnel
group by segment_name
order by avg_likelihood desc
```

### TDL vs USJ Preference by Age
```sql
select
    age_group,
    avg(avg_bipolar_score) as avg_preference,
    sum(case when overall_preference = 'TDR Loyalist' then 1 else 0 end) as tdr_loyalists,
    sum(case when overall_preference = 'USJ Loyalist' then 1 else 0 end) as usj_loyalists
from fct_tdr_vs_usj_comparison
group by age_group
```

### Top/Bottom Attributes
```sql
select
    'tdl_func_relaxing' as attribute,
    avg(tdl_func_relaxing) as avg_score
from fct_tdl_attribute_perceptions
union all
select 'tdl_func_not_crowded', avg(tdl_func_not_crowded)
from fct_tdl_attribute_perceptions
-- ... add other attributes
order by avg_score desc
```

---

## Data Quality Notes

1. **Missing Values**: Some respondents have nulls for attributes (99 code in source = missing)
2. **Sample Size**: 541 respondents total
3. **Validation**: Data extraction verified against source with 100% match on test fields
