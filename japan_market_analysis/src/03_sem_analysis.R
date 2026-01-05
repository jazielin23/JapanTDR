# ============================================================================
# Structural Equation Modeling (SEM) Analysis Module
# Uses lavaan for CFA and SEM analyses
# ============================================================================

# Set library path FIRST
user_lib <- path.expand("~/R/library")
if (dir.exists(user_lib)) .libPaths(c(user_lib, .libPaths()))

# Load individual tidyverse packages
library(dplyr)
library(tidyr)
library(readr)
library(purrr)
library(lavaan)
library(psych)

# Try to load semPlot if available
has_semPlot <- requireNamespace("semPlot", quietly = TRUE)
if (has_semPlot) library(semPlot)

# Load configuration (relative to working directory)
source("src/00_config.R")

# ============================================================================
# Model Specifications
# ============================================================================

#' Define the measurement model (CFA) for funnel stages
get_funnel_cfa_model <- function() {
  '
  # Measurement model for marketing funnel
  # Upper funnel: Awareness and Familiarity
  upper_funnel =~ awareness + familiarity
  
  # Middle funnel: Opinion and Consideration
  middle_funnel =~ opinion + consideration
  
  # Lower funnel: Likelihood and Intent
  lower_funnel =~ likelihood + intent
  '
}

#' Define the measurement model for brand benefits
get_benefits_cfa_model <- function() {
  '
  # Functional benefits latent construct
  functional =~ func_convenience + func_value + func_quality + 
                func_variety + func_reliability
  
  # Emotional benefits latent construct
  emotional =~ emot_excitement + emot_relaxation + emot_connection + 
               emot_authenticity + emot_memorable
  '
}

#' Define the complete CFA model
get_complete_cfa_model <- function() {
  '
  # Marketing Funnel Constructs
  upper_funnel =~ awareness + familiarity
  middle_funnel =~ opinion + consideration
  lower_funnel =~ likelihood + intent
  
  # Brand Benefits Constructs
  functional =~ func_convenience + func_value + func_quality + 
                func_variety + func_reliability
  emotional =~ emot_excitement + emot_relaxation + emot_connection + 
               emot_authenticity + emot_memorable
  '
}

#' Define the structural model: Funnel driving Intent
get_funnel_sem_model <- function() {
  '
  # Measurement Model
  upper_funnel =~ awareness + familiarity
  middle_funnel =~ opinion + consideration
  lower_funnel =~ likelihood + intent
  
  # Structural Model: Funnel Progression
  middle_funnel ~ upper_funnel
  lower_funnel ~ middle_funnel + upper_funnel
  
  # Intent as ultimate outcome (part of lower funnel)
  '
}

#' Define the full SEM model: Funnel + Benefits driving Intent
get_full_sem_model <- function() {
  '
  # === MEASUREMENT MODEL ===
  
  # Marketing Funnel Constructs
  upper_funnel =~ awareness + familiarity
  middle_funnel =~ opinion + consideration
  lower_funnel =~ likelihood + intent
  
  # Brand Benefits Constructs
  functional =~ func_convenience + func_value + func_quality + 
                func_variety + func_reliability
  emotional =~ emot_excitement + emot_relaxation + emot_connection + 
               emot_authenticity + emot_memorable
  
  # === STRUCTURAL MODEL ===
  
  # Funnel progression
  middle_funnel ~ a1*upper_funnel
  lower_funnel ~ b1*middle_funnel + b2*upper_funnel
  
  # Benefits influence on lower funnel (intent)
  lower_funnel ~ d1*functional + d2*emotional
  
  # === INDIRECT EFFECTS ===
  
  # Indirect effect of upper funnel on lower funnel via middle
  indirect_upper := a1 * b1
  
  # Total effect of upper funnel on lower funnel
  total_upper := b2 + (a1 * b1)
  '
}

#' Define a simpler SEM model for robust estimation
get_simple_sem_model <- function() {
  '
  # === MEASUREMENT MODEL ===
  
  # Brand Benefits Constructs only
  functional =~ func_convenience + func_value + func_quality + 
                func_variety + func_reliability
  emotional =~ emot_excitement + emot_relaxation + emot_connection + 
               emot_authenticity + emot_memorable
  
  # === STRUCTURAL MODEL ===
  
  # Direct effects on intent (observed variable)
  intent ~ awareness + familiarity + consideration + functional + emotional
  
  # Covariances
  awareness ~~ familiarity
  awareness ~~ consideration
  familiarity ~~ consideration
  '
}

#' Alternative model: Direct paths to intent
get_direct_intent_model <- function() {
  '
  # === MEASUREMENT MODEL ===
  
  # Use single indicators for funnel stages
  # (treating them as observed variables)
  
  # Brand Benefits Constructs
  functional =~ func_convenience + func_value + func_quality + 
                func_variety + func_reliability
  emotional =~ emot_excitement + emot_relaxation + emot_connection + 
               emot_authenticity + emot_memorable
  
  # === STRUCTURAL MODEL ===
  
  # All predictors directly affecting intent
  intent ~ awareness + familiarity + opinion + consideration + likelihood
  intent ~ functional + emotional
  
  # Funnel progression (correlations between stages)
  awareness ~~ familiarity
  familiarity ~~ opinion
  opinion ~~ consideration
  consideration ~~ likelihood
  
  # Benefits influence earlier stages
  opinion ~ functional + emotional
  consideration ~ functional + emotional
  '
}

#' Mediation model: Testing if consideration mediates awareness->intent
get_mediation_model <- function() {
  '
  # Mediation: Awareness -> Consideration -> Intent
  
  # Direct effect
  intent ~ c*awareness
  
  # Mediation path
  consideration ~ a*awareness
  intent ~ b*consideration
  
  # Control for other variables
  intent ~ familiarity + opinion + likelihood
  consideration ~ familiarity + opinion
  
  # Indirect and total effects
  indirect := a * b
  total := c + (a * b)
  '
}

# ============================================================================
# Model Fitting Functions
# ============================================================================

#' Fit a CFA model
fit_cfa <- function(data, model_syntax, model_name = "CFA Model") {
  
  message(paste("\nFitting", model_name, "..."))
  
  fit <- cfa(
    model = model_syntax,
    data = data,
    estimator = "MLR",  # Robust ML for non-normal data
    std.lv = TRUE,      # Standardize latent variables
    missing = "fiml"    # Full information ML for missing data
  )
  
  message("Model fitted successfully")
  
  return(fit)
}

#' Fit a SEM model
fit_sem <- function(data, model_syntax, model_name = "SEM Model") {
  
  message(paste("\nFitting", model_name, "..."))
  
  fit <- sem(
    model = model_syntax,
    data = data,
    estimator = "MLR",
    std.lv = TRUE,
    missing = "fiml"
  )
  
  message("Model fitted successfully")
  
  return(fit)
}

#' Fit multi-group SEM (for comparing regions or segments)
fit_multigroup_sem <- function(data, model_syntax, group_var, model_name = "Multi-group SEM") {
  
  message(paste("\nFitting", model_name, "by", group_var, "..."))
  
  # Configural invariance (same structure, different parameters)
  fit_config <- sem(
    model = model_syntax,
    data = data,
    group = group_var,
    estimator = "MLR",
    std.lv = TRUE
  )
  
  # Metric invariance (equal factor loadings)
  fit_metric <- sem(
    model = model_syntax,
    data = data,
    group = group_var,
    group.equal = c("loadings"),
    estimator = "MLR",
    std.lv = TRUE
  )
  
  # Scalar invariance (equal loadings and intercepts)
  fit_scalar <- sem(
    model = model_syntax,
    data = data,
    group = group_var,
    group.equal = c("loadings", "intercepts"),
    estimator = "MLR",
    std.lv = TRUE
  )
  
  message("Multi-group models fitted")
  
  return(list(
    configural = fit_config,
    metric = fit_metric,
    scalar = fit_scalar
  ))
}

# ============================================================================
# Model Evaluation Functions
# ============================================================================

#' Get comprehensive fit indices
get_fit_indices <- function(fit) {
  
  fit_measures <- fitmeasures(fit, c(
    "chisq", "df", "pvalue",
    "cfi", "tli", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper",
    "srmr", "aic", "bic"
  ))
  
  # Create summary data frame
  fit_df <- data.frame(
    Measure = c(
      "Chi-square", "df", "p-value",
      "CFI", "TLI", "RMSEA", "RMSEA 90% CI Lower", "RMSEA 90% CI Upper",
      "SRMR", "AIC", "BIC"
    ),
    Value = as.numeric(fit_measures),
    Threshold = c(
      "Lower is better", "-", "> 0.05",
      "> 0.95", "> 0.95", "< 0.06", "-", "-",
      "< 0.08", "Lower is better", "Lower is better"
    )
  )
  
  return(fit_df)
}

#' Evaluate model fit quality
evaluate_fit <- function(fit) {
  
  fits <- fitmeasures(fit, c("cfi", "tli", "rmsea", "srmr"))
  
  evaluation <- list(
    cfi_good = fits["cfi"] >= 0.95,
    cfi_acceptable = fits["cfi"] >= 0.90,
    tli_good = fits["tli"] >= 0.95,
    tli_acceptable = fits["tli"] >= 0.90,
    rmsea_good = fits["rmsea"] <= 0.06,
    rmsea_acceptable = fits["rmsea"] <= 0.08,
    srmr_good = fits["srmr"] <= 0.08
  )
  
  overall <- ifelse(
    all(evaluation$cfi_good, evaluation$rmsea_good, evaluation$srmr_good),
    "Excellent",
    ifelse(
      all(evaluation$cfi_acceptable, evaluation$rmsea_acceptable, evaluation$srmr_good),
      "Acceptable",
      "Poor"
    )
  )
  
  return(list(
    indices = fits,
    evaluation = evaluation,
    overall = overall
  ))
}

#' Print model summary with interpretation
print_model_summary <- function(fit, model_name = "Model") {
  
  message("\n" %>% paste0(rep("=", 70), collapse = ""))
  message(paste(model_name, "RESULTS"))
  message("=" %>% rep(70) %>% paste(collapse = ""))
  
  # Fit indices
  message("\n--- Model Fit Indices ---")
  fit_df <- get_fit_indices(fit)
  print(fit_df, row.names = FALSE)
  
  # Evaluate fit
  eval_result <- evaluate_fit(fit)
  message(paste("\nOverall Model Fit:", eval_result$overall))
  
  # Parameter estimates
  message("\n--- Standardized Parameter Estimates ---")
  params <- standardizedSolution(fit)
  
  # Latent variable definitions (factor loadings)
  loadings <- params %>%
    filter(op == "=~") %>%
    select(lhs, rhs, est.std, se, pvalue) %>%
    mutate(
      sig = case_when(
        pvalue < 0.001 ~ "***",
        pvalue < 0.01 ~ "**",
        pvalue < 0.05 ~ "*",
        TRUE ~ ""
      )
    )
  
  message("\nFactor Loadings:")
  print(loadings, row.names = FALSE)
  
  # Structural paths (regressions)
  regressions <- params %>%
    filter(op == "~") %>%
    select(lhs, rhs, est.std, se, pvalue) %>%
    mutate(
      sig = case_when(
        pvalue < 0.001 ~ "***",
        pvalue < 0.01 ~ "**",
        pvalue < 0.05 ~ "*",
        TRUE ~ ""
      )
    )
  
  if (nrow(regressions) > 0) {
    message("\nStructural Paths (Regressions):")
    print(regressions, row.names = FALSE)
  }
  
  # Defined parameters (indirect effects)
  defined <- params %>%
    filter(op == ":=") %>%
    select(lhs, est.std, se, pvalue) %>%
    mutate(
      sig = case_when(
        pvalue < 0.001 ~ "***",
        pvalue < 0.01 ~ "**",
        pvalue < 0.05 ~ "*",
        TRUE ~ ""
      )
    )
  
  if (nrow(defined) > 0) {
    message("\nIndirect/Defined Effects:")
    print(defined, row.names = FALSE)
  }
  
  # R-squared values
  message("\n--- Variance Explained (R²) ---")
  r2 <- lavInspect(fit, "r2")
  print(round(r2, 3))
  
  message("\n" %>% paste0(rep("=", 70), collapse = ""))
  
  return(invisible(NULL))
}

# ============================================================================
# Comparison Functions
# ============================================================================

#' Compare nested models using chi-square difference test
compare_models <- function(fit1, fit2, names = c("Model 1", "Model 2")) {
  
  comp <- anova(fit1, fit2)
  
  message("\n--- Model Comparison ---")
  message(paste(names[1], "vs", names[2]))
  print(comp)
  
  return(comp)
}

#' Compare multi-group invariance models
compare_invariance <- function(mg_fits) {
  
  message("\n--- Measurement Invariance Tests ---")
  
  # Check if all models converged
  if (!lavInspect(mg_fits$configural, "converged") ||
      !lavInspect(mg_fits$metric, "converged") ||
      !lavInspect(mg_fits$scalar, "converged")) {
    message("Warning: Not all models converged. Invariance tests may be unreliable.")
  }
  
  # Configural vs Metric
  message("\nConfigural vs Metric (Equal Loadings):")
  comp1 <- tryCatch({
    result <- anova(mg_fits$configural, mg_fits$metric)
    print(result)
    result
  }, error = function(e) {
    message("Could not compare models: ", e$message)
    NULL
  })
  
  # Metric vs Scalar
  message("\nMetric vs Scalar (Equal Loadings + Intercepts):")
  comp2 <- tryCatch({
    result <- anova(mg_fits$metric, mg_fits$scalar)
    print(result)
    result
  }, error = function(e) {
    message("Could not compare models: ", e$message)
    NULL
  })
  
  return(list(
    config_vs_metric = comp1,
    metric_vs_scalar = comp2
  ))
}

# ============================================================================
# Results Extraction Functions
# ============================================================================

#' Extract key path coefficients
extract_path_coefficients <- function(fit) {
  
  params <- standardizedSolution(fit)
  
  paths <- params %>%
    filter(op == "~") %>%
    select(
      outcome = lhs,
      predictor = rhs,
      beta = est.std,
      se = se,
      z = z,
      pvalue = pvalue
    ) %>%
    mutate(
      significance = case_when(
        pvalue < 0.001 ~ "***",
        pvalue < 0.01 ~ "**",
        pvalue < 0.05 ~ "*",
        pvalue < 0.10 ~ ".",
        TRUE ~ ""
      )
    ) %>%
    arrange(outcome, desc(abs(beta)))
  
  return(paths)
}

#' Extract factor loadings
extract_loadings <- function(fit) {
  
  params <- standardizedSolution(fit)
  
  loadings <- params %>%
    filter(op == "=~") %>%
    select(
      factor = lhs,
      indicator = rhs,
      loading = est.std,
      se = se,
      pvalue = pvalue
    ) %>%
    mutate(
      significance = case_when(
        pvalue < 0.001 ~ "***",
        pvalue < 0.01 ~ "**",
        pvalue < 0.05 ~ "*",
        TRUE ~ ""
      )
    )
  
  return(loadings)
}

#' Extract indirect effects
extract_indirect_effects <- function(fit) {
  
  params <- standardizedSolution(fit)
  
  indirect <- params %>%
    filter(op == ":=") %>%
    select(
      effect = lhs,
      estimate = est.std,
      se = se,
      pvalue = pvalue
    ) %>%
    mutate(
      significance = case_when(
        pvalue < 0.001 ~ "***",
        pvalue < 0.01 ~ "**",
        pvalue < 0.05 ~ "*",
        TRUE ~ ""
      )
    )
  
  return(indirect)
}

#' Get R-squared values for endogenous variables
extract_r_squared <- function(fit) {
  
  r2 <- lavInspect(fit, "r2")
  
  r2_df <- data.frame(
    variable = names(r2),
    r_squared = as.numeric(r2)
  ) %>%
    arrange(desc(r_squared))
  
  return(r2_df)
}

# ============================================================================
# Main Analysis Functions
# ============================================================================

#' Run complete CFA analysis
run_cfa_analysis <- function(data) {
  
  message("\n" %>% paste0(rep("=", 70), collapse = ""))
  message("CONFIRMATORY FACTOR ANALYSIS")
  message("=" %>% rep(70) %>% paste(collapse = ""))
  
  # Fit funnel CFA
  funnel_cfa <- fit_cfa(data, get_funnel_cfa_model(), "Funnel CFA")
  print_model_summary(funnel_cfa, "Funnel CFA")
  
  # Fit benefits CFA
  benefits_cfa <- fit_cfa(data, get_benefits_cfa_model(), "Benefits CFA")
  print_model_summary(benefits_cfa, "Benefits CFA")
  
  # Fit complete CFA
  complete_cfa <- fit_cfa(data, get_complete_cfa_model(), "Complete CFA")
  print_model_summary(complete_cfa, "Complete CFA")
  
  return(list(
    funnel = funnel_cfa,
    benefits = benefits_cfa,
    complete = complete_cfa
  ))
}

#' Run complete SEM analysis
run_sem_analysis <- function(data) {
  
  message("\n" %>% paste0(rep("=", 70), collapse = ""))
  message("STRUCTURAL EQUATION MODELING ANALYSIS")
  message("=" %>% rep(70) %>% paste(collapse = ""))
  
  # Fit funnel-only SEM
  funnel_sem <- fit_sem(data, get_funnel_sem_model(), "Funnel SEM")
  print_model_summary(funnel_sem, "Funnel-Only SEM")
  
  # Fit full SEM with benefits
  full_sem <- fit_sem(data, get_full_sem_model(), "Full SEM")
  print_model_summary(full_sem, "Full SEM (Funnel + Benefits)")
  
  # Fit direct intent model
  direct_sem <- fit_sem(data, get_direct_intent_model(), "Direct Intent SEM")
  print_model_summary(direct_sem, "Direct Intent SEM")
  
  # Fit mediation model
  mediation_sem <- fit_sem(data, get_mediation_model(), "Mediation SEM")
  print_model_summary(mediation_sem, "Mediation SEM")
  
  return(list(
    funnel_only = funnel_sem,
    full = full_sem,
    direct = direct_sem,
    mediation = mediation_sem
  ))
}

#' Run multi-group analysis by region
run_region_comparison <- function(data) {
  
  message(paste(rep("=", 70), collapse = ""))
  message("MULTI-GROUP ANALYSIS BY REGION")
  message(paste(rep("=", 70), collapse = ""))
  
  # Try multi-group analysis with error handling
  result <- tryCatch({
    # Fit multi-group models
    mg_fits <- fit_multigroup_sem(
      data, 
      get_full_sem_model(), 
      "region",
      "Region Comparison"
    )
    
    # Test invariance with error handling
    invariance_tests <- tryCatch({
      compare_invariance(mg_fits)
    }, error = function(e) {
      message("Warning: Invariance tests failed - ", e$message)
      NULL
    })
    
    # Get group-specific parameters
    message("\n--- Local Region Parameters ---")
    local_params <- parameterEstimates(mg_fits$configural) %>%
      filter(group == 1, op %in% c("~", ":="))
    print(head(local_params, 20))
    
    message("\n--- Domestic Region Parameters ---")
    domestic_params <- parameterEstimates(mg_fits$configural) %>%
      filter(group == 2, op %in% c("~", ":="))
    print(head(domestic_params, 20))
    
    list(
      fits = mg_fits,
      invariance = invariance_tests
    )
  }, error = function(e) {
    message("\nMulti-group analysis failed: ", e$message)
    message("This can happen when the model is too complex for the data.")
    message("Proceeding with single-group analysis instead.\n")
    
    # Fall back to comparing separate models
    message("--- Separate Group Analysis ---")
    local_data <- data %>% filter(region == "Local")
    domestic_data <- data %>% filter(region == "Domestic")
    
    local_fit <- tryCatch(
      fit_sem(local_data, get_funnel_sem_model(), "Local SEM"),
      error = function(e) NULL
    )
    domestic_fit <- tryCatch(
      fit_sem(domestic_data, get_funnel_sem_model(), "Domestic SEM"),
      error = function(e) NULL
    )
    
    list(
      fits = list(local = local_fit, domestic = domestic_fit),
      invariance = NULL,
      note = "Multi-group failed; separate models fitted instead"
    )
  })
  
  return(result)
}

#' Run segment-specific analysis
run_segment_analysis <- function(data, segment_name) {
  
  message("\n" %>% paste0(rep("=", 70), collapse = ""))
  message(paste("SEGMENT ANALYSIS:", segment_name))
  message("=" %>% rep(70) %>% paste(collapse = ""))
  
  # Filter to segment
  segment_data <- data %>% filter(segment == segment_name)
  message(paste("Sample size:", nrow(segment_data)))
  
  # Fit full SEM
  segment_sem <- fit_sem(segment_data, get_full_sem_model(), 
                         paste(segment_name, "SEM"))
  print_model_summary(segment_sem, paste(segment_name, "SEM"))
  
  return(segment_sem)
}

# ============================================================================
# Save Results Functions
# ============================================================================

#' Save SEM results to files
save_sem_results <- function(sem_fits, output_dir = REPORTS_DIR) {
  
  message("\nSaving SEM results...")
  
  # Save fit indices
  for (name in names(sem_fits)) {
    if (!is.null(sem_fits[[name]])) {
      # Fit indices
      fit_df <- get_fit_indices(sem_fits[[name]])
      write_csv(fit_df, file.path(output_dir, paste0("fit_indices_", name, ".csv")))
      
      # Path coefficients
      paths <- extract_path_coefficients(sem_fits[[name]])
      write_csv(paths, file.path(output_dir, paste0("path_coefficients_", name, ".csv")))
      
      # Factor loadings
      loadings <- extract_loadings(sem_fits[[name]])
      write_csv(loadings, file.path(output_dir, paste0("factor_loadings_", name, ".csv")))
      
      # R-squared
      r2 <- extract_r_squared(sem_fits[[name]])
      write_csv(r2, file.path(output_dir, paste0("r_squared_", name, ".csv")))
    }
  }
  
  message("Results saved to:", output_dir)
}

# ============================================================================
# Run if executed as script
# ============================================================================

if (sys.nframe() == 0) {
  
  # Load processed data
  data_file <- file.path(DATA_PROCESSED_DIR, "survey_processed.rds")
  
  if (!file.exists(data_file)) {
    message("Processed data not found. Running data preparation...")
    source("src/02_data_preparation.R")
    prep_result <- prepare_data()
    data <- prep_result$data
  } else {
    data <- readRDS(data_file)
  }
  
  # Run CFA
  cfa_results <- run_cfa_analysis(data)
  
  # Run SEM
  sem_results <- run_sem_analysis(data)
  
  # Run region comparison
  region_results <- run_region_comparison(data)
  
  # Save results
  save_sem_results(sem_results)
  
  message("\n\nAnalysis complete!")
}
