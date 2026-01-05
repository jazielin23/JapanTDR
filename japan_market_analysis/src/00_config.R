# ============================================================================
# Configuration File for Japan Market Analysis
# ============================================================================

# Set library path for user-installed packages
.libPaths(c("~/R/library", .libPaths()))

# --- Project Paths ---
PROJECT_ROOT <- here::here()
DATA_RAW_DIR <- file.path(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED_DIR <- file.path(PROJECT_ROOT, "data", "processed")
OUTPUT_DIR <- file.path(PROJECT_ROOT, "output")
FIGURES_DIR <- file.path(OUTPUT_DIR, "figures")
REPORTS_DIR <- file.path(OUTPUT_DIR, "reports")

# Create directories if they don't exist
dir.create(DATA_RAW_DIR, recursive = TRUE, showWarnings = FALSE)
dir.create(DATA_PROCESSED_DIR, recursive = TRUE, showWarnings = FALSE)
dir.create(FIGURES_DIR, recursive = TRUE, showWarnings = FALSE)
dir.create(REPORTS_DIR, recursive = TRUE, showWarnings = FALSE)

# --- Survey Configuration ---

# Sample sizes
MONTHLY_SAMPLE_SIZE <- 500
ANNUAL_SAMPLE_SIZE <- 6000
N_MONTHS <- 10

# Segments per group per month
SEGMENT_SIZE_PER_MONTH <- 100

# Region definitions
REGIONS <- c("Local", "Domestic")

REGION_LABELS <- c(
  "Local" = "Nationwide Local (Greater Tokyo + 7 Prefectures)",
  "Domestic" = "Domestic (All Other Prefectures)"
)

# Prefectures in Local region (Greater Tokyo + 7 major prefectures)
LOCAL_PREFECTURES <- c(
  "Tokyo", "Kanagawa", "Saitama", "Chiba",  # Greater Tokyo

"Osaka", "Aichi", "Fukuoka", "Hokkaido"  # 4 additional major prefectures
)

# Demographic segments
DEMOGRAPHIC_SEGMENTS <- c(
  "Young Families",      # Child < 6
  "Matured Families",    # Child 7-17
  "Young Adults",        # 18-34, single
  "Young Couples",       # 18-34, partnered, no kids
  "Matured Adults 35+"   # 35+, no kids
)

SEGMENT_DESCRIPTIONS <- c(
  "Young Families" = "Households with children under 6 years old",
  "Matured Families" = "Households with children aged 7-17",
  "Young Adults" = "Single adults aged 18-34",
  "Young Couples" = "Partnered adults aged 18-34 without children",
  "Matured Adults 35+" = "Adults aged 35+ without children"
)

# --- Marketing Funnel Variables ---

FUNNEL_STAGES <- c(
  "awareness",      # Brand awareness
  "familiarity",    # Brand familiarity
  "opinion",        # Favorable opinion
  "consideration",  # Consideration set
  "likelihood",     # Likelihood to visit
  "intent",         # Intent to visit/return
  "nps"             # Net Promoter Score
)

FUNNEL_LABELS <- c(
  "awareness" = "Brand Awareness",
  "familiarity" = "Brand Familiarity",
  "opinion" = "Favorable Opinion",
  "consideration" = "Consideration",
  "likelihood" = "Likelihood to Visit",
  "intent" = "Intent to Visit/Return",
  "nps" = "Net Promoter Score"
)

# --- Brand Benefit Variables ---

# Functional benefits
FUNCTIONAL_BENEFITS <- c(
  "func_convenience",    # Convenient location/access
  "func_value",          # Good value for money
  "func_quality",        # High quality experience
  "func_variety",        # Variety of options
  "func_reliability"     # Reliable/consistent experience
)

FUNCTIONAL_LABELS <- c(
  "func_convenience" = "Convenience",
  "func_value" = "Value for Money",
  "func_quality" = "Quality Experience",
  "func_variety" = "Variety of Options",
  "func_reliability" = "Reliability"
)

# Emotional benefits
EMOTIONAL_BENEFITS <- c(
  "emot_excitement",     # Exciting/thrilling
  "emot_relaxation",     # Relaxing/peaceful
  "emot_connection",     # Sense of connection
  "emot_authenticity",   # Authentic experience
  "emot_memorable"       # Memorable moments
)

EMOTIONAL_LABELS <- c(
  "emot_excitement" = "Excitement",
  "emot_relaxation" = "Relaxation",
  "emot_connection" = "Connection",
  "emot_authenticity" = "Authenticity",
  "emot_memorable" = "Memorable"
)

ALL_BENEFITS <- c(FUNCTIONAL_BENEFITS, EMOTIONAL_BENEFITS)

# --- Scale Definitions ---

# Most items use 1-7 Likert scale
LIKERT_MIN <- 1
LIKERT_MAX <- 7

# NPS uses 0-10 scale
NPS_MIN <- 0
NPS_MAX <- 10

# --- Visualization Settings ---

# Color palettes
REGION_COLORS <- c("Local" = "#2E86AB", "Domestic" = "#A23B72")

SEGMENT_COLORS <- c(
  "Young Families" = "#E8573F",
  "Matured Families" = "#F4A261",
  "Young Adults" = "#2A9D8F",
  "Young Couples" = "#264653",
  "Matured Adults 35+" = "#9B5DE5"
)

FUNNEL_COLORS <- c(
  "awareness" = "#003F5C",
  "familiarity" = "#2F4B7C",
  "opinion" = "#665191",
  "consideration" = "#A05195",
  "likelihood" = "#D45087",
  "intent" = "#F95D6A",
  "nps" = "#FF7C43"
)

# Theme settings
THEME_FONT_FAMILY <- "sans"
THEME_BASE_SIZE <- 12

# --- Random Seed for Reproducibility ---
RANDOM_SEED <- 42

message("Configuration loaded successfully.")
