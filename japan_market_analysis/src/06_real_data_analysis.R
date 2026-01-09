# ============================================================================
# Real Data Analysis Script - TDL Brand Tracking Survey
# Using Relabeled Raw Data with validated Likert scale mappings
# ============================================================================

# ============================================================================
# Setup
# ============================================================================

suppressPackageStartupMessages({
  user_lib <- path.expand("~/R/library")
  if (dir.exists(user_lib)) .libPaths(c(user_lib, .libPaths()))
  
  library(dplyr)
  library(tidyr)
  library(readr)
  library(ggplot2)
  library(lavaan)
  library(psych)
})

message("\n")
message(paste(rep("=", 70), collapse = ""))
message("  TDL REAL DATA ANALYSIS")
message(paste(rep("=", 70), collapse = ""))
message("\n")

# ============================================================================
# Load Data
# ============================================================================

message("Loading TDL survey data...")

# Read the extracted TDL data
data <- read_csv("dbt_project/seeds/survey_responses_tdl.csv", 
                 show_col_types = FALSE)

message(paste("Loaded", nrow(data), "respondents"))

# ============================================================================
# Data Preparation
# ============================================================================

message("\nPreparing data...")

# Clean and prepare analysis dataset
analysis_data <- data %>%
  mutate(
    # Demographics
    segment = audience,
    gender = case_when(
      gender == "1" ~ "Male",
      gender == "2" ~ "Female",
      TRUE ~ NA_character_
    ),
    age = as.numeric(age),
    age_group = case_when(
      age >= 18 & age <= 34 ~ "18-34",
      age >= 35 & age <= 54 ~ "35-54",
      age >= 55 ~ "55+",
      TRUE ~ "Unknown"
    ),
    region = geography,
    
    # Funnel metrics (already 1-5 scale, 5=positive)
    familiarity = as.numeric(familiarity_tdl),
    opinion = as.numeric(opinion_tdl),
    consideration = as.numeric(consideration_tdl),
    likelihood = as.numeric(likelihood_visit_tdl),
    intent_binary = as.numeric(intent_visit_tdl == "Yes"),
    nps = as.numeric(nps_tdl),
    
    # Visit behavior
    been_past_3yr = as.numeric(been_to_tdl_past_3yr == "Yes"),
    disney_fan = as.numeric(disney_fandom == "Yes"),
    
    # Functional attributes (1-5 scale)
    func_relaxing = as.numeric(tdl_func_relaxing),
    func_enjoy = as.numeric(tdl_func_enjoy_myself),
    func_memories = as.numeric(tdl_func_lifelong_memories),
    func_bonding = as.numeric(tdl_func_bond_family_friends),
    func_kids_young = as.numeric(tdl_func_great_for_kids_under_6),
    func_kids_older = as.numeric(tdl_func_great_for_kids_7_17),
    func_adults = as.numeric(tdl_func_great_for_adults),
    func_family = as.numeric(tdl_func_great_for_all_family),
    func_variety = as.numeric(tdl_func_variety_of_things),
    func_unique = as.numeric(tdl_func_unique_experiences),
    func_repeat = as.numeric(tdl_func_repeat_experience),
    func_innovative = as.numeric(tdl_func_new_innovative),
    func_crowded = as.numeric(tdl_func_not_crowded),
    func_worth_price = as.numeric(tdl_func_worth_price),
    func_affordable = as.numeric(tdl_func_affordable),
    
    # Emotional attributes (1-5 scale)
    emot_dreams = as.numeric(tdl_emot_land_of_dreams),
    emot_escape = as.numeric(tdl_emot_removed_from_reality),
    emot_fantasy = as.numeric(tdl_emot_fantastical),
    emot_warm = as.numeric(tdl_emot_heartwarming),
    emot_healing = as.numeric(tdl_emot_soothing_healing),
    emot_safe = as.numeric(tdl_emot_feeling_safe),
    emot_sparkling = as.numeric(tdl_emot_sparkling),
    emot_premium = as.numeric(tdl_emot_premium_feeling),
    emot_feel_good = as.numeric(tdl_emot_feel_good),
    
    # Bipolar comparisons (1=TDR, 7=USJ) - recode so higher = TDR preference
    bipolar_fun_tdr = 8 - as.numeric(bipolar_fun),
    bipolar_special_tdr = 8 - as.numeric(bipolar_feeling_special),
    bipolar_innovative_tdr = 8 - as.numeric(bipolar_innovative),
    bipolar_trending_tdr = 8 - as.numeric(bipolar_trending)
  ) %>%
  # Filter to valid responses
  filter(!is.na(familiarity) & !is.na(likelihood))

message(paste("Analysis sample:", nrow(analysis_data), "respondents"))

# ============================================================================
# Descriptive Statistics
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("DESCRIPTIVE STATISTICS")
message(paste(rep("-", 50), collapse = ""))

# Sample by segment
segment_summary <- analysis_data %>%
  group_by(segment) %>%
  summarise(
    n = n(),
    pct = round(n() / nrow(analysis_data) * 100, 1),
    mean_age = round(mean(age, na.rm = TRUE), 1),
    pct_female = round(mean(gender == "Female", na.rm = TRUE) * 100, 1),
    .groups = "drop"
  )

message("\nSample by Segment:")
print(segment_summary)

# Funnel metrics by segment
funnel_by_segment <- analysis_data %>%
  group_by(segment) %>%
  summarise(
    familiarity = round(mean(familiarity, na.rm = TRUE), 2),
    opinion = round(mean(opinion, na.rm = TRUE), 2),
    consideration = round(mean(consideration, na.rm = TRUE), 2),
    likelihood = round(mean(likelihood, na.rm = TRUE), 2),
    nps = round(mean(nps, na.rm = TRUE), 1),
    .groups = "drop"
  )

message("\nFunnel Metrics by Segment (Scale 1-5, 5=Best):")
print(funnel_by_segment)

# ============================================================================
# Scale Reliability Analysis
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("SCALE RELIABILITY (Cronbach's Alpha)")
message(paste(rep("-", 50), collapse = ""))

# Functional benefits reliability
func_items <- analysis_data %>%
  select(starts_with("func_")) %>%
  select(where(~sum(!is.na(.)) > 100))

if (ncol(func_items) >= 3) {
  func_alpha <- psych::alpha(func_items, check.keys = TRUE)
  message(paste("\nFunctional Benefits Alpha:", round(func_alpha$total$raw_alpha, 3)))
}

# Emotional benefits reliability
emot_items <- analysis_data %>%
  select(starts_with("emot_")) %>%
  select(where(~sum(!is.na(.)) > 100))

if (ncol(emot_items) >= 3) {
  emot_alpha <- psych::alpha(emot_items, check.keys = TRUE)
  message(paste("Emotional Benefits Alpha:", round(emot_alpha$total$raw_alpha, 3)))
}

# Create composite scores
analysis_data <- analysis_data %>%
  rowwise() %>%
  mutate(
    functional_mean = mean(c_across(starts_with("func_")), na.rm = TRUE),
    emotional_mean = mean(c_across(starts_with("emot_")), na.rm = TRUE)
  ) %>%
  ungroup()

# ============================================================================
# Correlation Analysis
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("KEY CORRELATIONS")
message(paste(rep("-", 50), collapse = ""))

cor_vars <- analysis_data %>%
  select(familiarity, opinion, consideration, likelihood, 
         functional_mean, emotional_mean, nps) %>%
  filter(complete.cases(.))

cor_matrix <- cor(cor_vars, use = "complete.obs")
message("\nCorrelation Matrix:")
print(round(cor_matrix, 2))

# ============================================================================
# Regression Analysis: Drivers of Likelihood
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("REGRESSION: DRIVERS OF LIKELIHOOD TO VISIT")
message(paste(rep("-", 50), collapse = ""))

# Model 1: Funnel only
model_funnel <- lm(likelihood ~ familiarity + opinion + consideration, 
                   data = analysis_data)

message("\nModel 1: Funnel Metrics Only")
message(paste("R-squared:", round(summary(model_funnel)$r.squared, 3)))
print(round(coef(summary(model_funnel)), 3))

# Model 2: Add brand benefits
model_full <- lm(likelihood ~ familiarity + opinion + consideration + 
                   functional_mean + emotional_mean, 
                 data = analysis_data)

message("\nModel 2: Funnel + Brand Benefits")
message(paste("R-squared:", round(summary(model_full)$r.squared, 3)))
print(round(coef(summary(model_full)), 3))

# ============================================================================
# SEM Analysis (if sufficient sample)
# ============================================================================

if (nrow(analysis_data) >= 200) {
  message("\n")
  message(paste(rep("-", 50), collapse = ""))
  message("STRUCTURAL EQUATION MODEL")
  message(paste(rep("-", 50), collapse = ""))
  
  # Prepare SEM data (only complete cases for SEM variables)
  sem_data <- analysis_data %>%
    select(familiarity, opinion, consideration, likelihood,
           func_enjoy, func_memories, func_variety, func_worth_price,
           emot_dreams, emot_fantasy, emot_feel_good) %>%
    filter(complete.cases(.))
  
  message(paste("\nSEM sample size:", nrow(sem_data)))
  
  if (nrow(sem_data) >= 150) {
    # Simple path model
    sem_model <- '
      # Direct effects on likelihood
      likelihood ~ b1*consideration + b2*opinion + b3*familiarity
      
      # Funnel flow
      consideration ~ a1*opinion
      opinion ~ a2*familiarity
      
      # Indirect effect
      indirect := a1 * b1
    '
    
    tryCatch({
      sem_fit <- sem(sem_model, data = sem_data, 
                     estimator = "MLR",
                     missing = "fiml")
      
      # Fit indices
      fit_indices <- fitMeasures(sem_fit, c("cfi", "tli", "rmsea", "srmr"))
      message("\nModel Fit:")
      message(paste("  CFI:", round(fit_indices["cfi"], 3)))
      message(paste("  TLI:", round(fit_indices["tli"], 3)))
      message(paste("  RMSEA:", round(fit_indices["rmsea"], 3)))
      message(paste("  SRMR:", round(fit_indices["srmr"], 3)))
      
      # Path coefficients
      message("\nPath Coefficients:")
      param_est <- parameterEstimates(sem_fit, standardized = TRUE)
      paths <- param_est %>%
        filter(op == "~") %>%
        select(lhs, rhs, est, std.all, pvalue)
      print(paths)
      
      # Indirect effects
      message("\nIndirect Effects:")
      indirect <- param_est %>%
        filter(op == ":=")
      if (nrow(indirect) > 0) print(indirect)
      
    }, error = function(e) {
      message(paste("SEM Error:", e$message))
    })
  }
}

# ============================================================================
# TDR vs USJ Comparison
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("TDR vs USJ BIPOLAR COMPARISON")
message(paste(rep("-", 50), collapse = ""))

# Analyze bipolar scores (after recoding: higher = TDR preference)
bipolar_summary <- analysis_data %>%
  select(starts_with("bipolar_")) %>%
  summarise(across(everything(), ~mean(., na.rm = TRUE)))

message("\nBipolar Scores (7=Strong TDR, 4=Neutral, 1=Strong USJ):")
for (col in names(bipolar_summary)) {
  score <- bipolar_summary[[col]]
  preference <- case_when(
    score > 4.5 ~ "TDR Advantage",
    score < 3.5 ~ "USJ Advantage", 
    TRUE ~ "Neutral"
  )
  message(paste(" ", col, ":", round(score, 2), "-", preference))
}

# ============================================================================
# Segment Comparison
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("SEGMENT PERFORMANCE COMPARISON")
message(paste(rep("-", 50), collapse = ""))

segment_performance <- analysis_data %>%
  group_by(segment) %>%
  summarise(
    n = n(),
    likelihood = round(mean(likelihood, na.rm = TRUE), 2),
    functional = round(mean(functional_mean, na.rm = TRUE), 2),
    emotional = round(mean(emotional_mean, na.rm = TRUE), 2),
    nps = round(mean(nps, na.rm = TRUE), 1),
    been_past_3yr = round(mean(been_past_3yr, na.rm = TRUE) * 100, 1),
    .groups = "drop"
  ) %>%
  arrange(desc(likelihood))

message("\nSegment Performance (ranked by likelihood):")
print(segment_performance)

# ============================================================================
# Generate Visualizations
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("GENERATING VISUALIZATIONS")
message(paste(rep("-", 50), collapse = ""))

output_dir <- "output/figures"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# 1. Funnel by Segment
funnel_long <- analysis_data %>%
  select(segment, familiarity, opinion, consideration, likelihood) %>%
  pivot_longer(cols = c(familiarity, opinion, consideration, likelihood),
               names_to = "stage", values_to = "score") %>%
  mutate(stage = factor(stage, levels = c("familiarity", "opinion", 
                                           "consideration", "likelihood")))

p_funnel <- ggplot(funnel_long, aes(x = stage, y = score, fill = segment)) +
  stat_summary(fun = mean, geom = "bar", position = position_dodge(0.9)) +
  stat_summary(fun.data = mean_se, geom = "errorbar", 
               position = position_dodge(0.9), width = 0.2) +
  scale_y_continuous(limits = c(0, 5), breaks = 1:5) +
  labs(title = "TDL Marketing Funnel by Segment",
       subtitle = "Scale: 1 (Low) to 5 (High)",
       x = "Funnel Stage", y = "Mean Score", fill = "Segment") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave(file.path(output_dir, "tdl_funnel_by_segment.png"), p_funnel, 
       width = 10, height = 6, dpi = 150)
message("Saved: tdl_funnel_by_segment.png")

# 2. Attribute Importance
attr_means <- analysis_data %>%
  summarise(across(starts_with("func_"), ~mean(., na.rm = TRUE))) %>%
  pivot_longer(everything(), names_to = "attribute", values_to = "mean_score") %>%
  mutate(attribute = gsub("func_", "", attribute)) %>%
  arrange(desc(mean_score))

p_attrs <- ggplot(attr_means, aes(x = reorder(attribute, mean_score), y = mean_score)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_hline(yintercept = 3, linetype = "dashed", color = "gray50") +
  coord_flip() +
  scale_y_continuous(limits = c(0, 5)) +
  labs(title = "TDL Functional Attribute Ratings",
       subtitle = "Scale: 1 (Low) to 5 (High), dashed line = neutral",
       x = "", y = "Mean Score") +
  theme_minimal()

ggsave(file.path(output_dir, "tdl_attribute_ratings.png"), p_attrs, 
       width = 8, height = 6, dpi = 150)
message("Saved: tdl_attribute_ratings.png")

# 3. Correlation heatmap
if (nrow(cor_vars) > 50) {
  cor_long <- as.data.frame(as.table(cor_matrix)) %>%
    rename(var1 = Var1, var2 = Var2, correlation = Freq)
  
  p_cor <- ggplot(cor_long, aes(x = var1, y = var2, fill = correlation)) +
    geom_tile() +
    geom_text(aes(label = round(correlation, 2)), size = 3) +
    scale_fill_gradient2(low = "blue", mid = "white", high = "red", 
                         midpoint = 0, limits = c(-1, 1)) +
    labs(title = "TDL Metric Correlations", x = "", y = "") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  ggsave(file.path(output_dir, "tdl_correlation_heatmap.png"), p_cor, 
         width = 8, height = 6, dpi = 150)
  message("Saved: tdl_correlation_heatmap.png")
}

# ============================================================================
# Save Results
# ============================================================================

message("\n")
message(paste(rep("-", 50), collapse = ""))
message("SAVING RESULTS")
message(paste(rep("-", 50), collapse = ""))

reports_dir <- "output/reports"
dir.create(reports_dir, showWarnings = FALSE, recursive = TRUE)

write_csv(segment_summary, file.path(reports_dir, "tdl_segment_summary.csv"))
write_csv(funnel_by_segment, file.path(reports_dir, "tdl_funnel_by_segment.csv"))
write_csv(segment_performance, file.path(reports_dir, "tdl_segment_performance.csv"))

message("Saved summary tables to output/reports/")

# ============================================================================
# Executive Summary
# ============================================================================

message("\n")
message(paste(rep("=", 70), collapse = ""))
message("  TDL ANALYSIS - EXECUTIVE SUMMARY")
message(paste(rep("=", 70), collapse = ""))

message("\n1. SAMPLE OVERVIEW")
message(paste("   Total respondents:", nrow(analysis_data)))
message(paste("   Segments:", paste(unique(analysis_data$segment), collapse = ", ")))

message("\n2. OVERALL FUNNEL METRICS (Scale 1-5)")
overall_funnel <- analysis_data %>%
  summarise(
    Familiarity = round(mean(familiarity, na.rm = TRUE), 2),
    Opinion = round(mean(opinion, na.rm = TRUE), 2),
    Consideration = round(mean(consideration, na.rm = TRUE), 2),
    Likelihood = round(mean(likelihood, na.rm = TRUE), 2)
  )
print(overall_funnel)

message("\n3. KEY DRIVERS OF LIKELIHOOD (Regression)")
message("   Top predictors from regression model:")
coefs <- coef(summary(model_full))
sig_coefs <- coefs[coefs[, "Pr(>|t|)"] < 0.05, ]
for (i in 1:min(5, nrow(sig_coefs))) {
  message(paste("   -", rownames(sig_coefs)[i], 
                ": β =", round(sig_coefs[i, "Estimate"], 3)))
}

message("\n4. STRONGEST SEGMENT")
top_seg <- segment_performance$segment[1]
message(paste("   Highest likelihood:", top_seg))

message("\n5. BRAND PERCEPTION STRENGTHS")
top_attrs <- attr_means %>% head(3)
message("   Top-rated attributes:")
for (i in 1:3) {
  message(paste("   -", top_attrs$attribute[i], ":", round(top_attrs$mean_score[i], 2)))
}

message("\n")
message(paste(rep("=", 70), collapse = ""))
message("  ANALYSIS COMPLETE")
message(paste(rep("=", 70), collapse = ""))
message("\nOutput saved to:")
message("  - Figures: output/figures/")
message("  - Reports: output/reports/")
message("\n")
