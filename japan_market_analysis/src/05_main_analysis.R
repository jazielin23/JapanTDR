# ============================================================================
# Main Analysis Script for Japan Market Analysis
# Complete workflow: Data Generation → Preparation → SEM → Visualization
# ============================================================================

# ============================================================================
# Setup and Configuration
# ============================================================================

# Load required packages
suppressPackageStartupMessages({
  # Set library path
  .libPaths(c("~/R/library", .libPaths()))
  
  # Individual tidyverse packages
  library(dplyr)
  library(tidyr)
  library(readr)
  library(purrr)
  library(ggplot2)
  
  # SEM packages
  library(lavaan)
  library(psych)
  library(here)
  
  # Optional
  if (requireNamespace("semPlot", quietly = TRUE)) library(semPlot)
})

# Set working directory to project root
setwd(here())

# Load configuration
source(here("src", "00_config.R"))

message("\n")
message("=" %>% rep(70) %>% paste(collapse = ""))
message("  JAPAN MARKET ANALYSIS - COMPLETE WORKFLOW")
message("=" %>% rep(70) %>% paste(collapse = ""))
message("\n")

# ============================================================================
# Step 1: Generate Data (if not exists)
# ============================================================================

message("STEP 1: Data Generation")
message("-" %>% rep(50) %>% paste(collapse = ""))

data_file <- file.path(DATA_RAW_DIR, "japan_market_survey_complete.csv")

if (!file.exists(data_file)) {
  message("Generating simulated survey data...")
  source(here("src", "01_generate_data.R"))
  survey_data <- generate_all_data()
  save_data(survey_data)
} else {
  message("Data file already exists. Skipping generation.")
}

# ============================================================================
# Step 2: Data Preparation
# ============================================================================

message("\n")
message("STEP 2: Data Preparation")
message("-" %>% rep(50) %>% paste(collapse = ""))

source(here("src", "02_data_preparation.R"))

prep_result <- prepare_data()
data <- prep_result$data
reliability <- prep_result$reliability

message(paste("\nTotal records:", nrow(data)))
message(paste("Regions:", paste(levels(data$region), collapse = ", ")))
message(paste("Segments:", paste(levels(data$segment), collapse = ", ")))

# ============================================================================
# Step 3: Confirmatory Factor Analysis (CFA)
# ============================================================================

message("\n")
message("STEP 3: Confirmatory Factor Analysis")
message("-" %>% rep(50) %>% paste(collapse = ""))

source(here("src", "03_sem_analysis.R"))

# Run CFA for measurement model validation
cfa_results <- run_cfa_analysis(data)

# Summary of CFA results
message("\n--- CFA Summary ---")
for (name in names(cfa_results)) {
  fit_eval <- evaluate_fit(cfa_results[[name]])
  message(paste(name, "CFA:", fit_eval$overall, 
                "| CFI:", round(fit_eval$indices["cfi"], 3),
                "| RMSEA:", round(fit_eval$indices["rmsea"], 3)))
}

# ============================================================================
# Step 4: Structural Equation Modeling (SEM)
# ============================================================================

message("\n")
message("STEP 4: Structural Equation Modeling")
message("-" %>% rep(50) %>% paste(collapse = ""))

# Run SEM analysis
sem_results <- run_sem_analysis(data)

# Summary of SEM results
message("\n--- SEM Summary ---")
for (name in names(sem_results)) {
  fit_eval <- evaluate_fit(sem_results[[name]])
  message(paste(name, ":", fit_eval$overall,
                "| CFI:", round(fit_eval$indices["cfi"], 3),
                "| RMSEA:", round(fit_eval$indices["rmsea"], 3)))
}

# Extract key findings from full model
full_model <- sem_results$full
message("\n--- Key Path Coefficients (Full Model) ---")
key_paths <- extract_path_coefficients(full_model) %>%
  filter(pvalue < 0.05) %>%
  head(10)
print(key_paths)

message("\n--- Indirect Effects ---")
indirect_effects <- extract_indirect_effects(full_model)
print(indirect_effects)

message("\n--- Variance Explained (R²) ---")
r2_values <- extract_r_squared(full_model)
print(r2_values)

# ============================================================================
# Step 5: Multi-Group Analysis
# ============================================================================

message("\n")
message("STEP 5: Multi-Group Analysis (Region Comparison)")
message("-" %>% rep(50) %>% paste(collapse = ""))

region_comparison <- run_region_comparison(data)

# ============================================================================
# Step 6: Segment-Level Analysis
# ============================================================================

message("\n")
message("STEP 6: Segment-Level Analysis")
message("-" %>% rep(50) %>% paste(collapse = ""))

segment_results <- list()
for (seg in DEMOGRAPHIC_SEGMENTS) {
  segment_n <- sum(data$segment == seg)
  message(paste("\nAnalyzing", seg, "(n =", segment_n, ")..."))
  
  # Only run SEM if sufficient sample size
  if (segment_n >= 500) {
    segment_results[[seg]] <- run_segment_analysis(data, seg)
  } else {
    message("Sample size too small for SEM. Skipping.")
  }
}

# ============================================================================
# Step 7: Visualization
# ============================================================================

message("\n")
message("STEP 7: Generating Visualizations")
message("-" %>% rep(50) %>% paste(collapse = ""))

source(here("src", "04_visualization.R"))

# Save all plots
save_all_plots(data, sem_results$full)

# ============================================================================
# Step 8: Generate Summary Report
# ============================================================================

message("\n")
message("STEP 8: Generating Summary Report")
message("-" %>% rep(50) %>% paste(collapse = ""))

# Create summary tables
summary_report <- list()

# 1. Sample characteristics
summary_report$sample <- data %>%
  group_by(region, segment) %>%
  summarise(
    n = n(),
    mean_age = mean(age, na.rm = TRUE),
    pct_female = mean(gender == "Female", na.rm = TRUE) * 100,
    .groups = "drop"
  )

# 2. Funnel metrics by segment
summary_report$funnel <- data %>%
  group_by(region, segment) %>%
  summarise(
    across(all_of(FUNNEL_STAGES), ~mean(., na.rm = TRUE)),
    .groups = "drop"
  )

# 3. Brand benefits by segment
summary_report$benefits <- data %>%
  group_by(region, segment) %>%
  summarise(
    functional = mean(functional_mean, na.rm = TRUE),
    emotional = mean(emotional_mean, na.rm = TRUE),
    .groups = "drop"
  )

# 4. Key drivers of intent
intent_drivers <- extract_path_coefficients(sem_results$direct) %>%
  filter(outcome == "intent") %>%
  arrange(desc(abs(beta)))

summary_report$intent_drivers <- intent_drivers

# 5. Conversion rates
summary_report$conversion <- data %>%
  group_by(region, segment) %>%
  summarise(
    high_awareness = mean(awareness >= 5) * 100,
    high_consideration = mean(consideration >= 5) * 100,
    high_intent = mean(intent >= 5) * 100,
    awareness_to_intent = mean(intent >= 5 & awareness >= 5) / mean(awareness >= 5) * 100,
    .groups = "drop"
  )

# Save summary tables
for (name in names(summary_report)) {
  write_csv(summary_report[[name]], 
            file.path(REPORTS_DIR, paste0("summary_", name, ".csv")))
}

# Save SEM results
save_sem_results(sem_results)

# ============================================================================
# Print Executive Summary
# ============================================================================

message("\n")
message("=" %>% rep(70) %>% paste(collapse = ""))
message("  EXECUTIVE SUMMARY")
message("=" %>% rep(70) %>% paste(collapse = ""))

message("\n1. SAMPLE OVERVIEW")
message("   - Total respondents: ", nrow(data))
message("   - Time period: ", N_MONTHS, " months")
message("   - Regions: Local (", sum(data$region == "Local"), 
        ") | Domestic (", sum(data$region == "Domestic"), ")")

message("\n2. KEY FUNNEL METRICS (Overall)")
funnel_overall <- data %>%
  summarise(across(all_of(FUNNEL_STAGES), ~mean(., na.rm = TRUE)))
for (stage in FUNNEL_STAGES) {
  message("   - ", FUNNEL_LABELS[stage], ": ", round(funnel_overall[[stage]], 2))
}

message("\n3. TOP DRIVERS OF INTENT TO VISIT")
top_drivers <- intent_drivers %>% head(5)
for (i in 1:nrow(top_drivers)) {
  message("   ", i, ". ", top_drivers$predictor[i], 
          " (β = ", round(top_drivers$beta[i], 3), 
          ", p ", ifelse(top_drivers$pvalue[i] < 0.001, "< 0.001", 
                         paste("=", round(top_drivers$pvalue[i], 3))), ")")
}

message("\n4. REGION COMPARISON")
region_means <- data %>%
  group_by(region) %>%
  summarise(
    intent = mean(intent, na.rm = TRUE),
    nps = mean(nps, na.rm = TRUE)
  )
message("   Intent to Visit: Local (", round(region_means$intent[region_means$region == "Local"], 2),
        ") vs Domestic (", round(region_means$intent[region_means$region == "Domestic"], 2), ")")
message("   NPS: Local (", round(region_means$nps[region_means$region == "Local"], 2),
        ") vs Domestic (", round(region_means$nps[region_means$region == "Domestic"], 2), ")")

message("\n5. SEGMENT INSIGHTS")
segment_intent <- data %>%
  group_by(segment) %>%
  summarise(
    intent = mean(intent, na.rm = TRUE),
    high_intent_pct = mean(high_intent) * 100
  ) %>%
  arrange(desc(intent))
message("   Highest intent: ", segment_intent$segment[1], 
        " (", round(segment_intent$intent[1], 2), ")")
message("   Lowest intent: ", segment_intent$segment[5], 
        " (", round(segment_intent$intent[5], 2), ")")

message("\n6. MODEL FIT")
full_eval <- evaluate_fit(sem_results$full)
message("   Full SEM Model: ", full_eval$overall)
message("   CFI = ", round(full_eval$indices["cfi"], 3))
message("   RMSEA = ", round(full_eval$indices["rmsea"], 3))
message("   SRMR = ", round(full_eval$indices["srmr"], 3))

message("\n7. RECOMMENDATIONS")
message("   Based on the SEM results:")

# Get top functional and emotional drivers
func_effect <- extract_path_coefficients(sem_results$full) %>%
  filter(predictor == "functional") %>%
  pull(beta) %>%
  mean(na.rm = TRUE)
emot_effect <- extract_path_coefficients(sem_results$full) %>%
  filter(predictor == "emotional") %>%
  pull(beta) %>%
  mean(na.rm = TRUE)

if (func_effect > emot_effect) {
  message("   - Prioritize functional benefits in marketing messaging")
} else {
  message("   - Prioritize emotional benefits in marketing messaging")
}
message("   - Focus on building awareness → consideration pipeline")
message("   - Tailor messaging by segment for maximum impact")

message("\n")
message("=" %>% rep(70) %>% paste(collapse = ""))
message("  ANALYSIS COMPLETE")
message("=" %>% rep(70) %>% paste(collapse = ""))
message("\nOutput files saved to:")
message("  - Figures: ", FIGURES_DIR)
message("  - Reports: ", REPORTS_DIR)
message("\n")

# ============================================================================
# Return results for further use
# ============================================================================

analysis_results <- list(
  data = data,
  reliability = reliability,
  cfa = cfa_results,
  sem = sem_results,
  region_comparison = region_comparison,
  segment_results = segment_results,
  summary = summary_report
)

message("Results stored in 'analysis_results' object.")
