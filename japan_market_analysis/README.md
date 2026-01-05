# Japan Market Analysis - SEM and Marketing Funnel Study

A comprehensive R-based analytical framework for analyzing Japan market survey data using Structural Equation Modeling (SEM). This project includes data generation, preparation, analysis, and visualization capabilities for understanding marketing funnel dynamics and brand perceptions.

## 📊 Project Overview

### Research Objectives

1. **Marketing Funnel Analysis**: Understand how funnel KPIs (awareness → familiarity → opinion → consideration → likelihood → intent) drive intent to visit/return
2. **Brand Benefits Analysis**: Analyze how functional and emotional brand perceptions influence intent
3. **Segment Comparison**: Compare marketing effectiveness across demographic segments and regions
4. **Mediation Testing**: Test indirect effects within the funnel (e.g., does consideration mediate the effect of awareness on intent?)

### Sample Structure

- **Annual Sample**: n=6,000 (n=500/month × 10 months)
- **Regions**: 
  - Local (Greater Tokyo + 7 major prefectures)
  - Domestic (all other prefectures)
- **Demographic Segments** (100 per group per month):
  - Young Families (child < 6)
  - Matured Families (child 7-17)
  - Young Adults (18-34, single)
  - Young Couples (18-34, partnered, no kids)
  - Matured Adults 35+ (no kids)

## 📁 Project Structure

```
japan_market_analysis/
├── data/
│   ├── raw/                    # Generated survey data files
│   │   ├── japan_market_survey_complete.csv
│   │   ├── survey_M01.csv through survey_M10.csv
│   │   └── data_dictionary.csv
│   └── processed/              # Cleaned and prepared data
│       ├── survey_processed.csv
│       ├── survey_processed.rds
│       └── aggregated files
├── src/
│   ├── 00_config.R             # Configuration and constants
│   ├── 01_generate_data.R      # Simulated data generation
│   ├── 02_data_preparation.R   # Data cleaning and preparation
│   ├── 03_sem_analysis.R       # SEM/CFA analysis (lavaan)
│   ├── 04_visualization.R      # Visualization functions
│   └── 05_main_analysis.R      # Complete analysis workflow
├── output/
│   ├── figures/                # Generated plots and diagrams
│   └── reports/                # Analysis results and tables
├── notebooks/                  # R Markdown notebooks (optional)
├── install_packages.R          # Package installation script
├── DESCRIPTION                 # Project metadata
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- R version 4.0 or higher
- RStudio (recommended)

### Installation

1. **Clone or download the project**

2. **Install required packages**:
   ```r
   source("install_packages.R")
   ```

   Key packages used:
   - `tidyverse` - Data manipulation
   - `lavaan` - Structural equation modeling
   - `semPlot` - SEM path diagrams
   - `psych` - Factor analysis utilities
   - `ggplot2` - Visualization
   - `corrplot` - Correlation matrices

### Running the Analysis

#### Option 1: Complete Workflow
Run the entire analysis pipeline:
```r
source("src/05_main_analysis.R")
```

This will:
1. Generate simulated data (if not exists)
2. Clean and prepare the data
3. Run CFA and SEM analyses
4. Create visualizations
5. Generate summary reports

#### Option 2: Step-by-Step
Run each module individually:

```r
# 1. Load configuration
source("src/00_config.R")

# 2. Generate data
source("src/01_generate_data.R")
full_data <- generate_all_data()
save_data(full_data)

# 3. Prepare data
source("src/02_data_preparation.R")
prep_result <- prepare_data()

# 4. Run SEM analysis
source("src/03_sem_analysis.R")
cfa_results <- run_cfa_analysis(prep_result$data)
sem_results <- run_sem_analysis(prep_result$data)

# 5. Create visualizations
source("src/04_visualization.R")
save_all_plots(prep_result$data, sem_results$full)
```

## 📐 Measurement Model

### Marketing Funnel Constructs

| Latent Variable | Indicators | Scale |
|-----------------|------------|-------|
| Upper Funnel | awareness, familiarity | 1-7 Likert |
| Middle Funnel | opinion, consideration | 1-7 Likert |
| Lower Funnel | likelihood, intent | 1-7 Likert |
| NPS | nps | 0-10 |

### Brand Benefits Constructs

| Latent Variable | Indicators |
|-----------------|------------|
| Functional | convenience, value, quality, variety, reliability |
| Emotional | excitement, relaxation, connection, authenticity, memorable |

## 📈 SEM Models

### 1. Funnel-Only Model
Tests the progression through marketing funnel stages:
```
upper_funnel → middle_funnel → lower_funnel
```

### 2. Full SEM Model
Includes both funnel progression and brand benefits:
```
upper_funnel → middle_funnel → lower_funnel
functional → middle_funnel, lower_funnel
emotional → middle_funnel, lower_funnel
```

### 3. Direct Intent Model
All predictors directly affecting intent:
```
intent ~ awareness + familiarity + opinion + consideration + likelihood + functional + emotional
```

### 4. Mediation Model
Tests if consideration mediates awareness → intent relationship.

## 📊 Output Files

### Figures (`output/figures/`)
- `01_funnel_overall.png` - Marketing funnel performance
- `02_funnel_by_region.png` - Funnel comparison by region
- `03_funnel_conversion.png` - Stage conversion rates
- `04_benefits_overall.png` - Brand benefit perceptions
- `05_benefits_heatmap.png` - Benefits by segment heatmap
- `06_time_trends.png` - Metrics over time
- `12_path_coefficients.png` - SEM path coefficients
- `15_sem_path_diagram.png` - Visual SEM diagram
- `16_executive_dashboard.png` - Summary dashboard

### Reports (`output/reports/`)
- `fit_indices_*.csv` - Model fit statistics
- `path_coefficients_*.csv` - Standardized regression coefficients
- `factor_loadings_*.csv` - CFA factor loadings
- `r_squared_*.csv` - Variance explained
- `summary_*.csv` - Aggregated summary tables

## 🔍 Interpreting Results

### Model Fit Criteria
| Index | Excellent | Acceptable |
|-------|-----------|------------|
| CFI | ≥ 0.95 | ≥ 0.90 |
| TLI | ≥ 0.95 | ≥ 0.90 |
| RMSEA | ≤ 0.06 | ≤ 0.08 |
| SRMR | ≤ 0.08 | ≤ 0.10 |

### Path Coefficient Interpretation
- **β > 0.5**: Large effect
- **0.3 < β < 0.5**: Medium effect
- **0.1 < β < 0.3**: Small effect
- **β < 0.1**: Negligible effect

## 🔧 Customization

### Modify Data Generation Parameters
Edit `src/00_config.R`:
```r
MONTHLY_SAMPLE_SIZE <- 500  # Change sample size
N_MONTHS <- 10              # Change number of months
SEGMENT_SIZE_PER_MONTH <- 100  # Change per-segment quota
```

### Add New Variables
1. Add to configuration in `00_config.R`
2. Update data generation in `01_generate_data.R`
3. Include in preparation in `02_data_preparation.R`
4. Modify SEM models in `03_sem_analysis.R`

### Custom SEM Models
Add new model specifications in `03_sem_analysis.R`:
```r
get_custom_model <- function() {
  '
  # Your custom model specification
  latent =~ indicator1 + indicator2
  outcome ~ predictor1 + predictor2
  '
}
```

## 📝 Notes

- The simulated data includes realistic correlations and segment effects
- All random generation uses a fixed seed (42) for reproducibility
- Missing data is handled using Full Information Maximum Likelihood (FIML)
- Multi-group analysis tests for measurement invariance between regions

## 📚 References

- Rosseel, Y. (2012). lavaan: An R Package for Structural Equation Modeling. Journal of Statistical Software, 48(2), 1-36.
- Kline, R. B. (2016). Principles and Practice of Structural Equation Modeling (4th ed.). Guilford Press.

## 📄 License

MIT License - See DESCRIPTION file for details.

---

*Generated for Japan Market Analysis Project*
