# ============================================================================
# Data Preparation and Cleaning Module
# Prepares survey data for SEM analysis
# ============================================================================

# Set library path FIRST
user_lib <- path.expand("~/R/library")
if (dir.exists(user_lib)) .libPaths(c(user_lib, .libPaths()))

# Load individual tidyverse packages
library(dplyr)
library(tidyr)
library(readr)
library(purrr)
library(psych)

# Load configuration (relative to working directory)
source("src/00_config.R")

# ============================================================================
# Data Loading Functions
# ============================================================================

#' Load complete survey dataset
load_complete_data <- function() {
  file_path <- file.path(DATA_RAW_DIR, "japan_market_survey_complete.csv")
  
  if (!file.exists(file_path)) {
    stop("Data file not found. Please run 01_generate_data.R first.")
  }
  
  data <- read_csv(file_path, show_col_types = FALSE)
  message(paste("Loaded", nrow(data), "records from complete dataset"))
  return(data)
}

#' Load monthly data files
load_monthly_data <- function(months = NULL) {
  if (is.null(months)) {
    months <- paste0("M", sprintf("%02d", 1:N_MONTHS))
  }
  
  all_data <- list()
  for (month in months) {
    file_path <- file.path(DATA_RAW_DIR, paste0("survey_", month, ".csv"))
    if (file.exists(file_path)) {
      all_data[[month]] <- read_csv(file_path, show_col_types = FALSE)
      message(paste("Loaded", month, ":", nrow(all_data[[month]]), "records"))
    } else {
      warning(paste("File not found:", file_path))
    }
  }
  
  combined <- bind_rows(all_data)
  message(paste("Total records loaded:", nrow(combined)))
  return(combined)
}

# ============================================================================
# Data Cleaning Functions
# ============================================================================

#' Clean and validate survey data
clean_survey_data <- function(data) {
  
  message("Cleaning survey data...")
  
  # Store original count
  n_original <- nrow(data)
  
  # Convert factors
  data <- data %>%
    mutate(
      region = factor(region, levels = REGIONS),
      segment = factor(segment, levels = DEMOGRAPHIC_SEGMENTS),
      month = factor(month, levels = paste0("M", sprintf("%02d", 1:N_MONTHS))),
      gender = factor(gender),
      relationship_status = factor(relationship_status),
      income_bracket = factor(income_bracket, levels = c(
        "Under 3M", "3-5M", "5-7M", "7-10M", "Over 10M"
      ))
    )
  
  # Validate Likert scale ranges
  likert_vars <- c(FUNNEL_STAGES[FUNNEL_STAGES != "nps"], ALL_BENEFITS)
  
  for (var in likert_vars) {
    if (var %in% names(data)) {
      out_of_range <- data[[var]] < LIKERT_MIN | data[[var]] > LIKERT_MAX
      if (any(out_of_range, na.rm = TRUE)) {
        warning(paste("Found", sum(out_of_range, na.rm = TRUE), 
                     "out-of-range values in", var))
        data[[var]] <- pmax(pmin(data[[var]], LIKERT_MAX), LIKERT_MIN)
      }
    }
  }
  
  # Validate NPS range
  if ("nps" %in% names(data)) {
    out_of_range <- data$nps < NPS_MIN | data$nps > NPS_MAX
    if (any(out_of_range, na.rm = TRUE)) {
      warning(paste("Found", sum(out_of_range, na.rm = TRUE), 
                   "out-of-range NPS values"))
      data$nps <- pmax(pmin(data$nps, NPS_MAX), NPS_MIN)
    }
  }
  
  # Remove duplicates based on respondent_id
  n_before_dedup <- nrow(data)
  data <- data %>% distinct(respondent_id, .keep_all = TRUE)
  n_duplicates <- n_before_dedup - nrow(data)
  
  if (n_duplicates > 0) {
    message(paste("Removed", n_duplicates, "duplicate records"))
  }
  
  # Handle missing values
  n_missing <- sum(is.na(data))
  if (n_missing > 0) {
    message(paste("Found", n_missing, "missing values"))
  }
  
  message(paste("Cleaned data:", nrow(data), "records (removed", 
                n_original - nrow(data), "records)"))
  
  return(data)
}

# ============================================================================
# Variable Creation Functions
# ============================================================================

#' Create derived variables for analysis
create_derived_variables <- function(data) {
  
  message("Creating derived variables...")
  
  data <- data %>%
    mutate(
      # Month number for time trends
      month_num = as.numeric(gsub("M", "", month)),
      
      # Age groups
      age_group = cut(age, 
                      breaks = c(0, 24, 34, 44, 54, 100),
                      labels = c("18-24", "25-34", "35-44", "45-54", "55+"),
                      include.lowest = TRUE),
      
      # NPS categories
      nps_category = case_when(
        nps >= 9 ~ "Promoter",
        nps >= 7 ~ "Passive",
        TRUE ~ "Detractor"
      ),
      nps_category = factor(nps_category, levels = c("Detractor", "Passive", "Promoter")),
      
      # Funnel progression score (mean of all funnel stages)
      funnel_mean = rowMeans(across(all_of(FUNNEL_STAGES[FUNNEL_STAGES != "nps"]))),
      
      # Functional benefits composite
      functional_mean = rowMeans(across(all_of(FUNCTIONAL_BENEFITS))),
      
      # Emotional benefits composite
      emotional_mean = rowMeans(across(all_of(EMOTIONAL_BENEFITS))),
      
      # Overall benefits composite
      benefits_mean = rowMeans(across(all_of(ALL_BENEFITS))),
      
      # High intent indicator (top 2 box: 6 or 7)
      high_intent = intent >= 6,
      
      # High consideration indicator
      high_consideration = consideration >= 6,
      
      # Region-Segment combination
      region_segment = paste(region, segment, sep = " - ")
    )
  
  message("Derived variables created successfully")
  return(data)
}

#' Standardize variables for SEM
standardize_for_sem <- function(data) {
  
  message("Standardizing variables for SEM...")
  
  # Variables to standardize
  vars_to_standardize <- c(FUNNEL_STAGES, ALL_BENEFITS)
  
  for (var in vars_to_standardize) {
    if (var %in% names(data)) {
      new_var <- paste0(var, "_z")
      data[[new_var]] <- scale(data[[var]])[, 1]
    }
  }
  
  message("Standardization complete")
  return(data)
}

# ============================================================================
# Data Quality Checks
# ============================================================================

#' Perform comprehensive data quality checks
check_data_quality <- function(data) {
  
  message(paste(rep("=", 60), collapse = ""))
  message("DATA QUALITY REPORT")
  message(paste(rep("=", 60), collapse = ""))
  
  # Basic info
  message("\n--- Basic Information ---")
  message(paste("Total records:", nrow(data)))
  message(paste("Total variables:", ncol(data)))
  message(paste("Date range:", levels(data$month)[1], "to", levels(data$month)[length(levels(data$month))]))
  
  # Sample distribution
  message("\n--- Sample Distribution by Region x Segment ---")
  print(table(data$region, data$segment))
  
  # Monthly distribution
  message("\n--- Monthly Distribution ---")
  print(table(data$month))
  
  # Missing values
  message("\n--- Missing Values ---")
  missing_summary <- colSums(is.na(data))
  missing_vars <- missing_summary[missing_summary > 0]
  if (length(missing_vars) > 0) {
    print(missing_vars)
  } else {
    message("No missing values found")
  }
  
  # Descriptive statistics for key variables
  message("\n--- Funnel Metrics Summary ---")
  funnel_summary <- data %>%
    select(all_of(FUNNEL_STAGES)) %>%
    psych::describe() %>%
    as.data.frame() %>%
    select(n, mean, sd, min, max, skew, kurtosis)
  print(round(funnel_summary, 2))
  
  message("\n--- Brand Benefits Summary ---")
  benefits_summary <- data %>%
    select(all_of(ALL_BENEFITS)) %>%
    psych::describe() %>%
    as.data.frame() %>%
    select(n, mean, sd, min, max, skew, kurtosis)
  print(round(benefits_summary, 2))
  
  # Correlation check
  message("\n--- Funnel Stage Correlations ---")
  funnel_cors <- data %>%
    select(all_of(FUNNEL_STAGES)) %>%
    cor(use = "pairwise.complete.obs")
  print(round(funnel_cors, 2))
  
  message(paste(rep("=", 60), collapse = ""))
  message("End of Quality Report")
  message(paste(rep("=", 60), collapse = ""))
  
  return(invisible(NULL))
}

#' Check reliability of scales
check_scale_reliability <- function(data) {
  
  message("\n--- Scale Reliability (Cronbach's Alpha) ---")
  
  # Funnel scale reliability
  funnel_items <- data %>% select(all_of(FUNNEL_STAGES[FUNNEL_STAGES != "nps"]))
  funnel_alpha <- psych::alpha(funnel_items, check.keys = TRUE)
  message(paste("Funnel Scale Alpha:", round(funnel_alpha$total$raw_alpha, 3)))
  
  # Functional benefits reliability
  func_items <- data %>% select(all_of(FUNCTIONAL_BENEFITS))
  func_alpha <- psych::alpha(func_items, check.keys = TRUE)
  message(paste("Functional Benefits Alpha:", round(func_alpha$total$raw_alpha, 3)))
  
  # Emotional benefits reliability
  emot_items <- data %>% select(all_of(EMOTIONAL_BENEFITS))
  emot_alpha <- psych::alpha(emot_items, check.keys = TRUE)
  message(paste("Emotional Benefits Alpha:", round(emot_alpha$total$raw_alpha, 3)))
  
  return(list(
    funnel = funnel_alpha,
    functional = func_alpha,
    emotional = emot_alpha
  ))
}

# ============================================================================
# Aggregation Functions
# ============================================================================

#' Aggregate data by segment and region
aggregate_by_segment <- function(data) {
  
  data %>%
    group_by(region, segment) %>%
    summarise(
      n = n(),
      across(all_of(c(FUNNEL_STAGES, ALL_BENEFITS)), 
             list(mean = ~mean(., na.rm = TRUE),
                  sd = ~sd(., na.rm = TRUE))),
      high_intent_pct = mean(high_intent, na.rm = TRUE) * 100,
      .groups = "drop"
    )
}

#' Aggregate data by month for time trends
aggregate_by_month <- function(data) {
  
  data %>%
    group_by(month, month_num) %>%
    summarise(
      n = n(),
      across(all_of(c(FUNNEL_STAGES, ALL_BENEFITS)), 
             list(mean = ~mean(., na.rm = TRUE),
                  sd = ~sd(., na.rm = TRUE))),
      high_intent_pct = mean(high_intent, na.rm = TRUE) * 100,
      .groups = "drop"
    ) %>%
    arrange(month_num)
}

#' Aggregate data by region, segment, and month
aggregate_full <- function(data) {
  
  data %>%
    group_by(region, segment, month, month_num) %>%
    summarise(
      n = n(),
      across(all_of(c(FUNNEL_STAGES, ALL_BENEFITS)), 
             list(mean = ~mean(., na.rm = TRUE))),
      high_intent_pct = mean(high_intent, na.rm = TRUE) * 100,
      .groups = "drop"
    ) %>%
    arrange(region, segment, month_num)
}

# ============================================================================
# Save Processed Data
# ============================================================================

#' Save processed data for analysis
save_processed_data <- function(data, aggregated_segment = NULL, aggregated_month = NULL) {
  
  # Save main processed file
  main_file <- file.path(DATA_PROCESSED_DIR, "survey_processed.csv")
  write_csv(data, main_file)
  message(paste("Saved processed data:", main_file))
  
  # Save as RDS for faster loading
  rds_file <- file.path(DATA_PROCESSED_DIR, "survey_processed.rds")
  saveRDS(data, rds_file)
  message(paste("Saved RDS file:", rds_file))
  
  # Save aggregated data if provided
  if (!is.null(aggregated_segment)) {
    agg_file <- file.path(DATA_PROCESSED_DIR, "aggregated_by_segment.csv")
    write_csv(aggregated_segment, agg_file)
    message(paste("Saved:", agg_file))
  }
  
  if (!is.null(aggregated_month)) {
    agg_file <- file.path(DATA_PROCESSED_DIR, "aggregated_by_month.csv")
    write_csv(aggregated_month, agg_file)
    message(paste("Saved:", agg_file))
  }
}

# ============================================================================
# Main Preparation Pipeline
# ============================================================================

prepare_data <- function() {
  
  message(paste(rep("=", 60), collapse = ""))
  message("STARTING DATA PREPARATION PIPELINE")
  message(paste(rep("=", 60), collapse = ""))
  
  # Load data
  data <- load_complete_data()
  
  # Clean data
  data <- clean_survey_data(data)
  
  # Create derived variables
  data <- create_derived_variables(data)
  
  # Standardize for SEM
  data <- standardize_for_sem(data)
  
  # Quality checks
  check_data_quality(data)
  
  # Check reliability
  reliability <- check_scale_reliability(data)
  
  # Create aggregations
  agg_segment <- aggregate_by_segment(data)
  agg_month <- aggregate_by_month(data)
  
  # Save processed data
  save_processed_data(data, agg_segment, agg_month)
  
  message(paste(rep("=", 60), collapse = ""))
  message("DATA PREPARATION COMPLETE")
  message(paste(rep("=", 60), collapse = ""))
  
  return(list(
    data = data,
    aggregated_segment = agg_segment,
    aggregated_month = agg_month,
    reliability = reliability
  ))
}

# ============================================================================
# Run if executed as script
# ============================================================================

if (sys.nframe() == 0) {
  result <- prepare_data()
  
  message("\n--- Aggregated by Segment (first 10 rows) ---")
  print(head(result$aggregated_segment, 10))
}
