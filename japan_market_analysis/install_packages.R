# ============================================================================
# Install Required R Packages for Japan Market Analysis
# ============================================================================

# List of required packages
required_packages <- c(
  # Data manipulation
  "tidyverse",
  "dplyr",
  "tidyr",
  "readr",
  "purrr",
  "stringr",
  "lubridate",
  

  # SEM and Factor Analysis
  "lavaan",
  "semPlot",
  "psych",
  
  # Visualization
  "ggplot2",
  "scales",
  "corrplot",
  "RColorBrewer",
  "gridExtra",
  "ggrepel",
  "patchwork",
  
  # Reporting
  "knitr",
  "rmarkdown",
  
  # Utilities
  "here",
  "janitor"
)

# Function to install packages if not already installed
install_if_missing <- function(packages) {
  new_packages <- packages[!(packages %in% installed.packages()[, "Package"])]
  if (length(new_packages) > 0) {
    message("Installing: ", paste(new_packages, collapse = ", "))
    install.packages(new_packages, repos = "https://cran.rstudio.com/")
  } else {
    message("All packages are already installed.")
  }
}

# Install missing packages
install_if_missing(required_packages)

# Load and verify all packages
message("\nLoading packages to verify installation...")
for (pkg in required_packages) {
  if (require(pkg, character.only = TRUE, quietly = TRUE)) {
    message("✓ ", pkg)
  } else {
    warning("✗ Failed to load: ", pkg)
  }
}

message("\nPackage installation complete!")
