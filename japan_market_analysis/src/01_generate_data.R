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
#' Higher awareness leads to higher familiarity, etc.
generate_funnel_metrics <- function(n, segment, region, month) {
  
  # Base means vary by segment and region
  segment_effects <- c(
    "Young Families" = 0.3,
    "Matured Families" = 0.2,
    "Young Adults" = 0.0,
    "Young Couples" = 0.1,
    "Matured Adults 35+" = -0.1
  )
  
  region_effects <- c(
    "Local" = 0.4,
    "Domestic" = 0.0
  )
  
  # Seasonal effect (summer months higher)
  month_num <- as.numeric(gsub("M", "", month))
  seasonal_effect <- 0.2 * sin((month_num - 3) * pi / 6)
  
  base_effect <- segment_effects[segment] + region_effects[region] + seasonal_effect
  
  # Generate awareness first (base of funnel)
  awareness_mean <- 4.5 + base_effect + rnorm(1, 0, 0.1)
  awareness <- generate_likert(n, awareness_mean)
  
  # Familiarity depends on awareness
  familiarity_mean <- 0.7 * awareness + rnorm(n, 0.5, 0.3)
  familiarity <- pmax(pmin(round(familiarity_mean), LIKERT_MAX), LIKERT_MIN)
  
  # Opinion depends on familiarity
  opinion_mean <- 0.6 * familiarity + 0.2 * awareness + rnorm(n, 0.3, 0.3)
  opinion <- pmax(pmin(round(opinion_mean), LIKERT_MAX), LIKERT_MIN)
  
  # Consideration depends on opinion and familiarity
  consideration_mean <- 0.5 * opinion + 0.3 * familiarity + rnorm(n, 0.2, 0.3)
  consideration <- pmax(pmin(round(consideration_mean), LIKERT_MAX), LIKERT_MIN)
  
  # Likelihood depends on consideration
  likelihood_mean <- 0.7 * consideration + 0.1 * opinion + rnorm(n, 0.2, 0.3)
  likelihood <- pmax(pmin(round(likelihood_mean), LIKERT_MAX), LIKERT_MIN)
  
  # Intent depends on likelihood and consideration
  intent_mean <- 0.6 * likelihood + 0.2 * consideration + rnorm(n, 0.2, 0.3)
  intent <- pmax(pmin(round(intent_mean), LIKERT_MAX), LIKERT_MIN)
  
  # NPS is related to overall experience (intent + opinion)
  nps_mean <- (intent + opinion) * 0.7 + rnorm(n, 0, 0.5)
  nps <- pmax(pmin(round(nps_mean), NPS_MAX), NPS_MIN)
  
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
  
  region_effect <- ifelse(region == "Local", 0.2, 0.0)
  
  # Base means from opinion (people with good opinion rate benefits higher)
  base_mean <- 3.5 + 0.3 * (funnel_data$opinion - 4) + region_effect
  
  func_prefs <- segment_func_pref[[segment]]
  emot_prefs <- segment_emot_pref[[segment]]
  
  # Generate functional benefits
  func_convenience <- generate_likert(n, base_mean + func_prefs["convenience"])
  func_value <- generate_likert(n, base_mean + func_prefs["value"])
  func_quality <- generate_likert(n, base_mean + func_prefs["quality"])
  func_variety <- generate_likert(n, base_mean + func_prefs["variety"])
  func_reliability <- generate_likert(n, base_mean + func_prefs["reliability"])
  
  # Generate emotional benefits
  emot_excitement <- generate_likert(n, base_mean + emot_prefs["excitement"])
  emot_relaxation <- generate_likert(n, base_mean + emot_prefs["relaxation"])
  emot_connection <- generate_likert(n, base_mean + emot_prefs["connection"])
  emot_authenticity <- generate_likert(n, base_mean + emot_prefs["authenticity"])
  emot_memorable <- generate_likert(n, base_mean + emot_prefs["memorable"])
  
  return(data.frame(
    func_convenience = func_convenience,
    func_value = func_value,
    func_quality = func_quality,
    func_variety = func_variety,
    func_reliability = func_reliability,
    emot_excitement = emot_excitement,
    emot_relaxation = emot_relaxation,
    emot_connection = emot_connection,
    emot_authenticity = emot_authenticity,
    emot_memorable = emot_memorable
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
