# ============================================================================
# Data Generation Script for Japan Market Analysis
# Generates simulated survey data for 10 months (n=1000/month, n=10000 total)
# ============================================================================

# Set library path for user-installed packages FIRST
user_lib <- path.expand("~/R/library")
if (dir.exists(user_lib)) .libPaths(c(user_lib, .libPaths()))

# Load individual tidyverse packages
library(dplyr)
library(tidyr)
library(readr)
library(purrr)

# Load configuration (relative to working directory)
source("src/00_config.R")

set.seed(RANDOM_SEED)

# ============================================================================
# Helper Functions
# ============================================================================

#' Generate correlated Likert scale responses
#' @param n Number of responses
#' @param mean_val Mean value (1-7 scale)
#' @param sd_val Standard deviation
#' @param min_val Minimum value
#' @param max_val Maximum value
generate_likert <- function(n, mean_val, sd_val = 1.2, min_val = 1, max_val = 7) {
  responses <- round(rnorm(n, mean = mean_val, sd = sd_val))
  responses <- pmax(pmin(responses, max_val), min_val)
  return(responses)
}

#' Generate NPS score (0-10 scale)
generate_nps <- function(n, mean_val, sd_val = 2.0) {
  responses <- round(rnorm(n, mean = mean_val, sd = sd_val))
  responses <- pmax(pmin(responses, NPS_MAX), NPS_MIN)
  return(responses)
}

#' Generate funnel metrics with logical progression
#' Creates realistic correlations suitable for SEM (r = 0.3-0.6 range)
generate_funnel_metrics <- function(n, segment, region, month) {
  
  # Base means vary by segment and region
  segment_effects <- c(
    "Young Families" = 0.4,
    "Matured Families" = 0.3,
    "Young Adults" = 0.0,
    "Young Couples" = 0.2,
    "Matured Adults 35+" = -0.1
  )
  
  region_effects <- c(
    "Local" = 0.5,
    "Domestic" = 0.0
  )
  
  # Seasonal effect (summer months higher)
  month_num <- as.numeric(gsub("M", "", month))
  seasonal_effect <- 0.3 * sin((month_num - 3) * pi / 6)
  
  base_effect <- segment_effects[segment] + region_effects[region] + seasonal_effect
  
  # Generate with moderate correlations (not too high to avoid multicollinearity)
  # Using a factor-based approach for more realistic SEM data
  
  # Common latent factors
  upper_factor <- rnorm(n, 0, 1)  # Upper funnel latent
  middle_factor <- rnorm(n, 0, 1) # Middle funnel latent
  lower_factor <- rnorm(n, 0, 1)  # Lower funnel latent
  
  # Cross-factor correlations (moderate)
  middle_factor <- 0.4 * upper_factor + sqrt(1 - 0.4^2) * middle_factor
  lower_factor <- 0.3 * upper_factor + 0.4 * middle_factor + sqrt(1 - 0.3^2 - 0.4^2) * lower_factor
  
  # Generate observed variables with factor loadings + unique variance
  awareness_mean <- 4.5 + base_effect
  awareness <- round(awareness_mean + 0.7 * upper_factor + rnorm(n, 0, 0.8))
  awareness <- pmax(pmin(awareness, LIKERT_MAX), LIKERT_MIN)
  
  familiarity <- round(4.0 + base_effect * 0.8 + 0.7 * upper_factor + rnorm(n, 0, 0.9))
  familiarity <- pmax(pmin(familiarity, LIKERT_MAX), LIKERT_MIN)
  
  opinion <- round(4.0 + base_effect * 0.7 + 0.65 * middle_factor + rnorm(n, 0, 0.9))
  opinion <- pmax(pmin(opinion, LIKERT_MAX), LIKERT_MIN)
  
  consideration <- round(3.8 + base_effect * 0.6 + 0.7 * middle_factor + rnorm(n, 0, 0.85))
  consideration <- pmax(pmin(consideration, LIKERT_MAX), LIKERT_MIN)
  
  likelihood <- round(3.5 + base_effect * 0.5 + 0.75 * lower_factor + rnorm(n, 0, 0.8))
  likelihood <- pmax(pmin(likelihood, LIKERT_MAX), LIKERT_MIN)
  
  intent <- round(3.3 + base_effect * 0.5 + 0.7 * lower_factor + rnorm(n, 0, 0.85))
  intent <- pmax(pmin(intent, LIKERT_MAX), LIKERT_MIN)
  
  # NPS with its own variance
  nps <- round(5.0 + base_effect * 1.2 + 0.5 * lower_factor + 0.3 * middle_factor + rnorm(n, 0, 1.5))
  nps <- pmax(pmin(nps, NPS_MAX), NPS_MIN)
  
  return(data.frame(
    awareness = awareness,
    familiarity = familiarity,
    opinion = opinion,
    consideration = consideration,
    likelihood = likelihood,
    intent = intent,
    nps = nps
  ))
}

#' Generate brand benefit perceptions
#' Creates correlated benefits within functional/emotional dimensions for valid CFA
generate_brand_benefits <- function(n, segment, region, funnel_data) {
  
  # Segment preferences for different benefits
  segment_func_pref <- list(
    "Young Families" = c(convenience = 0.5, value = 0.4, quality = 0.2, variety = 0.3, reliability = 0.4),
    "Matured Families" = c(convenience = 0.3, value = 0.3, quality = 0.4, variety = 0.4, reliability = 0.3),
    "Young Adults" = c(convenience = 0.2, value = 0.5, quality = 0.1, variety = 0.5, reliability = 0.0),
    "Young Couples" = c(convenience = 0.3, value = 0.3, quality = 0.3, variety = 0.4, reliability = 0.2),
    "Matured Adults 35+" = c(convenience = 0.4, value = 0.2, quality = 0.5, variety = 0.2, reliability = 0.5)
  )
  
  segment_emot_pref <- list(
    "Young Families" = c(excitement = 0.4, relaxation = 0.3, connection = 0.5, authenticity = 0.2, memorable = 0.5),
    "Matured Families" = c(excitement = 0.3, relaxation = 0.4, connection = 0.4, authenticity = 0.3, memorable = 0.4),
    "Young Adults" = c(excitement = 0.6, relaxation = 0.1, connection = 0.2, authenticity = 0.4, memorable = 0.5),
    "Young Couples" = c(excitement = 0.5, relaxation = 0.3, connection = 0.4, authenticity = 0.3, memorable = 0.5),
    "Matured Adults 35+" = c(excitement = 0.2, relaxation = 0.5, connection = 0.3, authenticity = 0.5, memorable = 0.3)
  )
  
  region_effect <- ifelse(region == "Local", 0.3, 0.0)
  
  func_prefs <- segment_func_pref[[segment]]
  emot_prefs <- segment_emot_pref[[segment]]
  
  # Create latent factors for benefits (for proper CFA structure)
  functional_factor <- rnorm(n, 0, 1)
  emotional_factor <- rnorm(n, 0, 1)
  
  # Correlate factors with funnel (benefits drive intent)
  # Get mean opinion for this batch
  opinion_centered <- funnel_data$opinion - mean(funnel_data$opinion)
  functional_factor <- functional_factor + 0.2 * opinion_centered / sd(funnel_data$opinion + 0.01)
  emotional_factor <- emotional_factor + 0.25 * opinion_centered / sd(funnel_data$opinion + 0.01)
  
  # Moderate correlation between functional and emotional
  emotional_factor <- 0.4 * functional_factor + sqrt(1 - 0.4^2) * emotional_factor
  
  base_mean <- 4.0 + region_effect
  
  # Generate functional benefits with shared factor + unique variance
  func_convenience <- round(base_mean + func_prefs["convenience"] + 0.65 * functional_factor + rnorm(n, 0, 0.9))
  func_value <- round(base_mean + func_prefs["value"] + 0.7 * functional_factor + rnorm(n, 0, 0.85))
  func_quality <- round(base_mean + func_prefs["quality"] + 0.7 * functional_factor + rnorm(n, 0, 0.85))
  func_variety <- round(base_mean + func_prefs["variety"] + 0.6 * functional_factor + rnorm(n, 0, 0.95))
  func_reliability <- round(base_mean + func_prefs["reliability"] + 0.65 * functional_factor + rnorm(n, 0, 0.9))
  
  # Generate emotional benefits with shared factor + unique variance
  emot_excitement <- round(base_mean + emot_prefs["excitement"] + 0.7 * emotional_factor + rnorm(n, 0, 0.85))
  emot_relaxation <- round(base_mean + emot_prefs["relaxation"] + 0.6 * emotional_factor + rnorm(n, 0, 0.95))
  emot_connection <- round(base_mean + emot_prefs["connection"] + 0.7 * emotional_factor + rnorm(n, 0, 0.85))
  emot_authenticity <- round(base_mean + emot_prefs["authenticity"] + 0.65 * emotional_factor + rnorm(n, 0, 0.9))
  emot_memorable <- round(base_mean + emot_prefs["memorable"] + 0.7 * emotional_factor + rnorm(n, 0, 0.85))
  
  # Clamp to valid range
  clamp <- function(x) pmax(pmin(x, LIKERT_MAX), LIKERT_MIN)
  
  return(data.frame(
    func_convenience = clamp(func_convenience),
    func_value = clamp(func_value),
    func_quality = clamp(func_quality),
    func_variety = clamp(func_variety),
    func_reliability = clamp(func_reliability),
    emot_excitement = clamp(emot_excitement),
    emot_relaxation = clamp(emot_relaxation),
    emot_connection = clamp(emot_connection),
    emot_authenticity = clamp(emot_authenticity),
    emot_memorable = clamp(emot_memorable)
  ))
}

#' Generate demographic details for a segment
generate_demographics <- function(n, segment) {
  
  demographics <- data.frame(
    respondent_id = character(n),
    age = integer(n),
    gender = character(n),
    household_size = integer(n),
    has_children = logical(n),
    youngest_child_age = integer(n),
    relationship_status = character(n),
    income_bracket = character(n),
    stringsAsFactors = FALSE
  )
  
  for (i in 1:n) {
    if (segment == "Young Families") {
      demographics$age[i] <- sample(25:45, 1)
      demographics$has_children[i] <- TRUE
      demographics$youngest_child_age[i] <- sample(0:5, 1)
      demographics$relationship_status[i] <- sample(c("Married", "Partnered"), 1, prob = c(0.8, 0.2))
      demographics$household_size[i] <- sample(3:5, 1, prob = c(0.5, 0.35, 0.15))
      
    } else if (segment == "Matured Families") {
      demographics$age[i] <- sample(35:55, 1)
      demographics$has_children[i] <- TRUE
      demographics$youngest_child_age[i] <- sample(7:17, 1)
      demographics$relationship_status[i] <- sample(c("Married", "Partnered", "Single"), 1, prob = c(0.75, 0.15, 0.10))
      demographics$household_size[i] <- sample(3:5, 1, prob = c(0.4, 0.4, 0.2))
      
    } else if (segment == "Young Adults") {
      demographics$age[i] <- sample(18:34, 1)
      demographics$has_children[i] <- FALSE
      demographics$youngest_child_age[i] <- NA
      demographics$relationship_status[i] <- "Single"
      demographics$household_size[i] <- sample(1:2, 1, prob = c(0.7, 0.3))
      
    } else if (segment == "Young Couples") {
      demographics$age[i] <- sample(18:34, 1)
      demographics$has_children[i] <- FALSE
      demographics$youngest_child_age[i] <- NA
      demographics$relationship_status[i] <- sample(c("Married", "Partnered"), 1, prob = c(0.4, 0.6))
      demographics$household_size[i] <- 2
      
    } else {  # Matured Adults 35+
      demographics$age[i] <- sample(35:70, 1)
      demographics$has_children[i] <- FALSE
      demographics$youngest_child_age[i] <- NA
      demographics$relationship_status[i] <- sample(c("Single", "Married", "Partnered", "Divorced/Widowed"), 1, 
                                                     prob = c(0.3, 0.4, 0.15, 0.15))
      demographics$household_size[i] <- sample(1:3, 1, prob = c(0.4, 0.45, 0.15))
    }
    
    # Gender (roughly balanced)
    demographics$gender[i] <- sample(c("Male", "Female", "Other/Prefer not to say"), 1, 
                                      prob = c(0.48, 0.48, 0.04))
    
    # Income bracket (varies slightly by age)
    if (demographics$age[i] < 30) {
      demographics$income_bracket[i] <- sample(
        c("Under 3M", "3-5M", "5-7M", "7-10M", "Over 10M"), 1,
        prob = c(0.25, 0.35, 0.25, 0.10, 0.05)
      )
    } else if (demographics$age[i] < 50) {
      demographics$income_bracket[i] <- sample(
        c("Under 3M", "3-5M", "5-7M", "7-10M", "Over 10M"), 1,
        prob = c(0.10, 0.25, 0.30, 0.25, 0.10)
      )
    } else {
      demographics$income_bracket[i] <- sample(
        c("Under 3M", "3-5M", "5-7M", "7-10M", "Over 10M"), 1,
        prob = c(0.15, 0.25, 0.25, 0.20, 0.15)
      )
    }
  }
  
  return(demographics)
}

#' Generate prefecture based on region
generate_prefecture <- function(n, region) {
  if (region == "Local") {
    prefectures <- sample(LOCAL_PREFECTURES, n, replace = TRUE)
  } else {
    # Other prefectures (simplified list)
    other_prefectures <- c(
      "Miyagi", "Niigata", "Ishikawa", "Nagano", "Shizuoka", "Kyoto",
      "Hyogo", "Nara", "Hiroshima", "Okayama", "Kagawa", "Ehime",
      "Kumamoto", "Nagasaki", "Kagoshima", "Okinawa", "Ibaraki",
      "Tochigi", "Gunma", "Yamanashi", "Gifu", "Mie", "Shiga",
      "Wakayama", "Tottori", "Shimane", "Yamaguchi", "Tokushima",
      "Kochi", "Saga", "Oita", "Miyazaki"
    )
    prefectures <- sample(other_prefectures, n, replace = TRUE)
  }
  return(prefectures)
}

# ============================================================================
# Main Data Generation
# ============================================================================

generate_monthly_data <- function(month_label) {
  
  message(paste("Generating data for", month_label, "..."))
  
  all_data <- list()
  respondent_counter <- 0
  
  for (region in REGIONS) {
    for (segment in DEMOGRAPHIC_SEGMENTS) {
      
      n <- SEGMENT_SIZE_PER_MONTH
      
      # Generate funnel metrics
      funnel_data <- generate_funnel_metrics(n, segment, region, month_label)
      
      # Generate brand benefits
      benefits_data <- generate_brand_benefits(n, segment, region, funnel_data)
      
      # Generate demographics
      demo_data <- generate_demographics(n, segment)
      
      # Create respondent IDs
      respondent_ids <- paste0(month_label, "_", sprintf("%04d", (respondent_counter + 1):(respondent_counter + n)))
      respondent_counter <- respondent_counter + n
      
      # Combine all data
      segment_data <- data.frame(
        respondent_id = respondent_ids,
        month = month_label,
        region = region,
        segment = segment,
        prefecture = generate_prefecture(n, region),
        stringsAsFactors = FALSE
      )
      
      # Add demographics
      segment_data <- cbind(
        segment_data,
        demo_data[, c("age", "gender", "household_size", "has_children", 
                      "youngest_child_age", "relationship_status", "income_bracket")]
      )
      
      # Add funnel metrics
      segment_data <- cbind(segment_data, funnel_data)
      
      # Add brand benefits
      segment_data <- cbind(segment_data, benefits_data)
      
      all_data[[paste(region, segment, sep = "_")]] <- segment_data
    }
  }
  
  # Combine all segments
  monthly_data <- bind_rows(all_data)
  
  return(monthly_data)
}

# ============================================================================
# Generate 10 Months of Data
# ============================================================================

generate_all_data <- function() {
  
  message(paste(rep("=", 60), collapse = ""))
  message("Starting data generation...")
  message(paste(rep("=", 60), collapse = ""))
  
  # Define months (e.g., M01 through M10)
  months <- paste0("M", sprintf("%02d", 1:N_MONTHS))
  
  all_months_data <- list()
  
  for (month in months) {
    all_months_data[[month]] <- generate_monthly_data(month)
  }
  
  # Combine all months
  full_dataset <- bind_rows(all_months_data)
  
  message(paste(rep("=", 60), collapse = ""))
  message(paste("Generated", nrow(full_dataset), "total responses"))
  message(paste("Unique respondents per month:", nrow(full_dataset) / N_MONTHS))
  message(paste(rep("=", 60), collapse = ""))
  
  return(full_dataset)
}

# ============================================================================
# Save Data Files
# ============================================================================

save_data <- function(data) {
  
  message("Saving data files...")
  
  # Save complete dataset
  complete_file <- file.path(DATA_RAW_DIR, "japan_market_survey_complete.csv")
  write_csv(data, complete_file)
  message(paste("Saved:", complete_file))
  
  # Save monthly files
  months <- unique(data$month)
  for (month in months) {
    monthly_data <- data %>% filter(month == !!month)
    monthly_file <- file.path(DATA_RAW_DIR, paste0("survey_", month, ".csv"))
    write_csv(monthly_data, monthly_file)
    message(paste("Saved:", monthly_file))
  }
  
  # Save data dictionary
  data_dict <- data.frame(
    variable = c(
      "respondent_id", "month", "region", "segment", "prefecture",
      "age", "gender", "household_size", "has_children", "youngest_child_age",
      "relationship_status", "income_bracket",
      FUNNEL_STAGES,
      FUNCTIONAL_BENEFITS,
      EMOTIONAL_BENEFITS
    ),
    description = c(
      "Unique respondent identifier",
      "Survey month (M01-M10)",
      "Region: Local (Greater Tokyo + 7 prefectures) or Domestic",
      "Demographic segment",
      "Prefecture of residence",
      "Age in years",
      "Gender",
      "Number of people in household",
      "Has children (TRUE/FALSE)",
      "Age of youngest child (if applicable)",
      "Relationship status",
      "Annual household income bracket (JPY millions)",
      # Funnel stages
      "Brand awareness (1-7 scale)",
      "Brand familiarity (1-7 scale)",
      "Favorable opinion (1-7 scale)",
      "Consideration for visit (1-7 scale)",
      "Likelihood to visit (1-7 scale)",
      "Intent to visit/return (1-7 scale)",
      "Net Promoter Score (0-10 scale)",
      # Functional benefits
      "Convenience perception (1-7 scale)",
      "Value for money perception (1-7 scale)",
      "Quality experience perception (1-7 scale)",
      "Variety of options perception (1-7 scale)",
      "Reliability perception (1-7 scale)",
      # Emotional benefits
      "Excitement perception (1-7 scale)",
      "Relaxation perception (1-7 scale)",
      "Connection perception (1-7 scale)",
      "Authenticity perception (1-7 scale)",
      "Memorable experience perception (1-7 scale)"
    ),
    type = c(
      rep("character", 5),
      "integer", "character", "integer", "logical", "integer",
      "character", "character",
      rep("integer", length(FUNNEL_STAGES)),
      rep("integer", length(FUNCTIONAL_BENEFITS)),
      rep("integer", length(EMOTIONAL_BENEFITS))
    ),
    stringsAsFactors = FALSE
  )
  
  dict_file <- file.path(DATA_RAW_DIR, "data_dictionary.csv")
  write_csv(data_dict, dict_file)
  message(paste("Saved:", dict_file))
  
  message("Data generation complete!")
}

# ============================================================================
# Run Generation
# ============================================================================

if (sys.nframe() == 0) {
  # Running as main script
  full_data <- generate_all_data()
  save_data(full_data)
  
  # Print summary
  message("\n--- Data Summary ---")
  print(table(full_data$region, full_data$segment))
  message("\n--- Monthly Distribution ---")
  print(table(full_data$month))
}
