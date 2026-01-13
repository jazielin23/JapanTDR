# Handling Competitor Data in Theme Park Survey

## Current Focus: Tokyo Disneyland (TDL)

The survey collects data on multiple theme parks:
- **TDL** - Tokyo Disneyland (primary focus)
- **TDS** - Tokyo DisneySea (sister park)
- **USJ** - Universal Studios Japan (main competitor)
- **Fuji-Q Highland** (competitor)
- **Ghibli Park** (competitor)
- **LEGOLAND Japan** (competitor)
- **Nagashima Spaland** (competitor)

Currently, the data model focuses on TDL with comparative references to TDS and USJ.

---

## Options for Competitor Analysis

### Option A: Current Approach (Recommended for TDL Focus)
**Status: Implemented**

Extract TDL-specific columns with USJ and TDS as comparison points.

**Pros:**
- Simpler data model
- Clear TDL-centric analysis
- Efficient for TDL stakeholders

**Cons:**
- Cannot do full competitive benchmarking
- Missing analysis on Fuji-Q, Ghibli, etc.

---

### Option B: Multi-Park Comparative Model

Create parallel models for each park with identical structure.

```
fct_park_brand_funnel (with park_id dimension)
├── TDL metrics
├── TDS metrics  
├── USJ metrics
├── Fuji-Q metrics
└── etc.
```

**Implementation:**
1. Modify extraction script to pull all parks
2. Create long-format table with `park_id` as dimension
3. Enable side-by-side comparisons

**Pros:**
- Full competitive analysis capability
- Easy to add new parks
- Consistent metrics across all parks

**Cons:**
- More complex data model
- Larger data volume
- May be overkill if TDL is only focus

---

### Option C: Competitor Summary View

Keep TDL as primary but add a summary view for competitors.

```sql
-- Example: dim_competitor_summary
select
    'USJ' as park,
    avg(familiarity_usj) as avg_familiarity,
    avg(opinion_usj) as avg_opinion,
    avg(consideration_usj) as avg_consideration
union all
select 'Fuji-Q', ...
```

**Pros:**
- Lightweight addition
- Maintains TDL focus
- Provides competitive context

**Cons:**
- Limited to summary stats
- No individual-level analysis

---

## Column Positions for All Parks (Reference)

Based on Relabeled Raw Data.csv:

| Metric | TDL | TDS | USJ | Fuji-Q | Ghibli | LEGOLAND | Nagashima |
|--------|-----|-----|-----|--------|--------|----------|-----------|
| Familiarity | 86 | 87 | 88 | 89 | 90 | 91 | 92 |
| Opinion | 94 | 95 | 96 | 97 | 98 | 99 | 100 |
| Consideration | 102 | 103 | 104 | 105 | 106 | 107 | 108 |
| Likelihood | 110 | 111 | 112 | 113 | 114 | 115 | 116 |
| NPS | 137 | 138 | 139 | 140 | 141 | 142 | 143 |

Attribute ratings only collected for TDL, TDS, and USJ (columns 145-252).

---

## Recommendation

For initial analysis: **Continue with Option A (TDL Focus)**

The current model includes:
- Direct TDL metrics
- TDL vs USJ comparisons via bipolar scales
- TDL vs USJ/TDS gap analysis on funnel metrics

If broader competitive analysis is needed later, Option B can be implemented by:
1. Extending the extraction script
2. Creating a `dim_parks` dimension table
3. Unpivoting metrics into long format

---

## Bipolar Scale Interpretation

The bipolar scales directly compare TDR (Tokyo Disney Resort = TDL + TDS) against USJ:

| Score | Interpretation |
|-------|----------------|
| 1 | Definitely TDR |
| 2 | Strongly TDR |
| 3 | Slightly TDR |
| 4 | Neutral |
| 5 | Slightly USJ |
| 6 | Strongly USJ |
| 7 | Definitely USJ |

**For TDR/TDL analysis:** Lower scores = Better for Disney
