# ============================================================================
# Visualization Module for Japan Market Analysis
# Creates publication-ready figures for SEM results and marketing insights
# ============================================================================

# Set library path FIRST
.libPaths(c("~/R/library", .libPaths()))

# Load individual tidyverse packages
library(dplyr)
library(tidyr)
library(readr)
library(purrr)
library(ggplot2)
library(scales)
library(corrplot)
library(lavaan)
library(here)

# Try to load optional packages
has_semPlot <- requireNamespace("semPlot", quietly = TRUE)
if (has_semPlot) library(semPlot)
has_patchwork <- requireNamespace("patchwork", quietly = TRUE)
if (has_patchwork) library(patchwork)

# Load configuration
source(here("src", "00_config.R"))

# ============================================================================
# Theme Setup
# ============================================================================

#' Custom theme for all plots
theme_japan_market <- function(base_size = 12) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title = element_text(face = "bold", size = base_size * 1.3, hjust = 0),
      plot.subtitle = element_text(color = "gray40", size = base_size * 0.9),
      plot.caption = element_text(color = "gray50", size = base_size * 0.7, hjust = 1),
      axis.title = element_text(size = base_size * 0.9),
      axis.text = element_text(size = base_size * 0.8),
      legend.title = element_text(face = "bold", size = base_size * 0.9),
      legend.text = element_text(size = base_size * 0.8),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(color = "gray90"),
      strip.text = element_text(face = "bold", size = base_size * 0.9),
      plot.margin = margin(15, 15, 15, 15)
    )
}

# Set as default theme
theme_set(theme_japan_market())

# ============================================================================
# Funnel Visualization Functions
# ============================================================================

#' Create marketing funnel chart
plot_funnel_chart <- function(data, by_group = NULL, title = "Marketing Funnel") {
  
  # Calculate means for each funnel stage
  if (is.null(by_group)) {
    funnel_means <- data %>%
      summarise(across(all_of(FUNNEL_STAGES[FUNNEL_STAGES != "nps"]), 
                       ~mean(., na.rm = TRUE))) %>%
      pivot_longer(everything(), names_to = "stage", values_to = "mean") %>%
      mutate(stage = factor(stage, levels = FUNNEL_STAGES[FUNNEL_STAGES != "nps"]))
  } else {
    funnel_means <- data %>%
      group_by(across(all_of(by_group))) %>%
      summarise(across(all_of(FUNNEL_STAGES[FUNNEL_STAGES != "nps"]), 
                       ~mean(., na.rm = TRUE)), .groups = "drop") %>%
      pivot_longer(cols = all_of(FUNNEL_STAGES[FUNNEL_STAGES != "nps"]),
                   names_to = "stage", values_to = "mean") %>%
      mutate(stage = factor(stage, levels = FUNNEL_STAGES[FUNNEL_STAGES != "nps"]))
  }
  
  # Calculate conversion rates (percentage of max score)
  funnel_means <- funnel_means %>%
    mutate(pct_of_max = mean / LIKERT_MAX * 100)
  
  # Create funnel plot
  if (is.null(by_group)) {
    p <- ggplot(funnel_means, aes(x = stage, y = pct_of_max, fill = stage)) +
      geom_col(width = 0.7) +
      geom_text(aes(label = sprintf("%.1f", mean)), 
                vjust = -0.5, size = 4, fontface = "bold") +
      scale_fill_manual(values = FUNNEL_COLORS, guide = "none") +
      scale_y_continuous(limits = c(0, 100), labels = function(x) paste0(x, "%")) +
      labs(
        title = title,
        subtitle = "Average scores as percentage of maximum (7-point scale)",
        x = "Funnel Stage",
        y = "% of Maximum Score",
        caption = "Higher values indicate stronger performance"
      )
  } else {
    p <- ggplot(funnel_means, aes(x = stage, y = pct_of_max, 
                                   fill = .data[[by_group]])) +
      geom_col(position = position_dodge(width = 0.8), width = 0.7) +
      scale_y_continuous(limits = c(0, 100), labels = function(x) paste0(x, "%")) +
      labs(
        title = title,
        subtitle = paste("Comparison by", by_group),
        x = "Funnel Stage",
        y = "% of Maximum Score",
        fill = by_group
      ) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
    if (by_group == "region") {
      p <- p + scale_fill_manual(values = REGION_COLORS)
    } else if (by_group == "segment") {
      p <- p + scale_fill_manual(values = SEGMENT_COLORS)
    }
  }
  
  return(p)
}

#' Create funnel conversion visualization
plot_funnel_conversion <- function(data) {
  
  # Calculate stage-to-stage conversion
  stage_order <- FUNNEL_STAGES[FUNNEL_STAGES != "nps"]
  
  conversion_data <- data.frame(
    from_stage = stage_order[-length(stage_order)],
    to_stage = stage_order[-1]
  )
  
  # Calculate conversion rates
  for (i in 1:nrow(conversion_data)) {
    from <- conversion_data$from_stage[i]
    to <- conversion_data$to_stage[i]
    
    # Conversion = % of people with high score in 'from' who also have high score in 'to'
    high_from <- data[[from]] >= 5
    high_to <- data[[to]] >= 5
    
    conversion_data$conversion_rate[i] <- sum(high_from & high_to) / sum(high_from) * 100
  }
  
  conversion_data$transition <- paste(conversion_data$from_stage, "→", conversion_data$to_stage)
  conversion_data$transition <- factor(conversion_data$transition, 
                                        levels = conversion_data$transition)
  
  p <- ggplot(conversion_data, aes(x = transition, y = conversion_rate)) +
    geom_col(fill = "#2E86AB", width = 0.6) +
    geom_text(aes(label = sprintf("%.1f%%", conversion_rate)), 
              vjust = -0.5, size = 4, fontface = "bold") +
    scale_y_continuous(limits = c(0, 100), labels = function(x) paste0(x, "%")) +
    labs(
      title = "Funnel Stage Conversion Rates",
      subtitle = "Percentage of respondents with high scores (≥5) progressing to next stage",
      x = "Stage Transition",
      y = "Conversion Rate"
    ) +
    theme(axis.text.x = element_text(angle = 30, hjust = 1))
  
  return(p)
}

# ============================================================================
# Brand Benefits Visualization
# ============================================================================

#' Create brand benefits radar/spider chart
plot_benefits_radar <- function(data, by_group = NULL) {
  
  if (is.null(by_group)) {
    benefits_means <- data %>%
      summarise(across(all_of(ALL_BENEFITS), ~mean(., na.rm = TRUE))) %>%
      pivot_longer(everything(), names_to = "benefit", values_to = "mean")
  } else {
    benefits_means <- data %>%
      group_by(across(all_of(by_group))) %>%
      summarise(across(all_of(ALL_BENEFITS), ~mean(., na.rm = TRUE)), .groups = "drop") %>%
      pivot_longer(cols = all_of(ALL_BENEFITS), names_to = "benefit", values_to = "mean")
  }
  
  # Add benefit type
  benefits_means <- benefits_means %>%
    mutate(
      benefit_type = ifelse(benefit %in% FUNCTIONAL_BENEFITS, "Functional", "Emotional"),
      benefit_label = case_when(
        benefit == "func_convenience" ~ "Convenience",
        benefit == "func_value" ~ "Value",
        benefit == "func_quality" ~ "Quality",
        benefit == "func_variety" ~ "Variety",
        benefit == "func_reliability" ~ "Reliability",
        benefit == "emot_excitement" ~ "Excitement",
        benefit == "emot_relaxation" ~ "Relaxation",
        benefit == "emot_connection" ~ "Connection",
        benefit == "emot_authenticity" ~ "Authenticity",
        benefit == "emot_memorable" ~ "Memorable",
        TRUE ~ benefit
      )
    )
  
  if (is.null(by_group)) {
    p <- ggplot(benefits_means, aes(x = reorder(benefit_label, -mean), y = mean, 
                                     fill = benefit_type)) +
      geom_col(width = 0.7) +
      geom_text(aes(label = sprintf("%.2f", mean)), vjust = -0.5, size = 3.5) +
      scale_fill_manual(values = c("Functional" = "#2E86AB", "Emotional" = "#A23B72")) +
      scale_y_continuous(limits = c(0, 7)) +
      labs(
        title = "Brand Benefit Perceptions",
        subtitle = "Mean ratings on 7-point scale",
        x = "Benefit",
        y = "Mean Rating",
        fill = "Benefit Type"
      ) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
  } else {
    p <- ggplot(benefits_means, aes(x = benefit_label, y = mean, 
                                     fill = .data[[by_group]])) +
      geom_col(position = position_dodge(width = 0.8), width = 0.7) +
      facet_wrap(~benefit_type, scales = "free_x") +
      scale_y_continuous(limits = c(0, 7)) +
      labs(
        title = "Brand Benefit Perceptions by Group",
        x = "Benefit",
        y = "Mean Rating",
        fill = by_group
      ) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
    if (by_group == "region") {
      p <- p + scale_fill_manual(values = REGION_COLORS)
    } else if (by_group == "segment") {
      p <- p + scale_fill_manual(values = SEGMENT_COLORS)
    }
  }
  
  return(p)
}

#' Create benefits heatmap by segment
plot_benefits_heatmap <- function(data) {
  
  # Calculate means by segment
  benefits_by_segment <- data %>%
    group_by(segment) %>%
    summarise(across(all_of(ALL_BENEFITS), ~mean(., na.rm = TRUE)), .groups = "drop") %>%
    pivot_longer(cols = all_of(ALL_BENEFITS), names_to = "benefit", values_to = "mean")
  
  # Create nice labels
  benefits_by_segment <- benefits_by_segment %>%
    mutate(
      benefit_label = case_when(
        benefit == "func_convenience" ~ "Convenience",
        benefit == "func_value" ~ "Value for Money",
        benefit == "func_quality" ~ "Quality",
        benefit == "func_variety" ~ "Variety",
        benefit == "func_reliability" ~ "Reliability",
        benefit == "emot_excitement" ~ "Excitement",
        benefit == "emot_relaxation" ~ "Relaxation",
        benefit == "emot_connection" ~ "Connection",
        benefit == "emot_authenticity" ~ "Authenticity",
        benefit == "emot_memorable" ~ "Memorable",
        TRUE ~ benefit
      ),
      benefit_type = ifelse(benefit %in% FUNCTIONAL_BENEFITS, "Functional", "Emotional")
    )
  
  p <- ggplot(benefits_by_segment, aes(x = segment, y = benefit_label, fill = mean)) +
    geom_tile(color = "white", size = 0.5) +
    geom_text(aes(label = sprintf("%.2f", mean)), size = 3, color = "white") +
    scale_fill_gradient2(low = "#E8573F", mid = "#F4A261", high = "#2A9D8F",
                         midpoint = mean(benefits_by_segment$mean),
                         limits = c(1, 7)) +
    facet_grid(benefit_type ~ ., scales = "free_y", space = "free_y") +
    labs(
      title = "Brand Benefit Perceptions by Demographic Segment",
      subtitle = "Mean ratings on 7-point scale",
      x = "Demographic Segment",
      y = "Benefit",
      fill = "Mean\nRating"
    ) +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      panel.grid = element_blank()
    )
  
  return(p)
}

# ============================================================================
# SEM Path Diagram Functions
# ============================================================================

#' Create SEM path diagram using semPlot (if available)
plot_sem_diagram <- function(fit, title = "SEM Path Diagram", 
                              layout = "tree2", what = "std") {
  
  if (!has_semPlot) {
    message("semPlot package not available. Skipping path diagram.")
    return(invisible(NULL))
  }
  
  semPlot::semPaths(
    fit,
    what = what,
    whatLabels = "std",
    layout = layout,
    edge.label.cex = 0.8,
    node.label.cex = 0.8,
    sizeMan = 6,
    sizeLat = 8,
    style = "lisrel",
    nCharNodes = 0,
    nCharEdges = 0,
    edge.color = "black",
    color = list(
      lat = "#2E86AB",
      man = "#F4A261"
    ),
    border.color = "gray30",
    title = TRUE,
    title.cex = 1.2,
    mar = c(2, 2, 3, 2)
  )
  
  title(main = title, line = 2)
}

#' Create custom path coefficient plot
plot_path_coefficients <- function(sem_fit, title = "Standardized Path Coefficients") {
  
  # Extract standardized solution
  params <- standardizedSolution(sem_fit)
  
  # Get regression paths
  paths <- params %>%
    filter(op == "~") %>%
    select(outcome = lhs, predictor = rhs, beta = est.std, pvalue = pvalue) %>%
    mutate(
      sig = pvalue < 0.05,
      path_label = paste(predictor, "→", outcome)
    ) %>%
    arrange(desc(abs(beta)))
  
  p <- ggplot(paths, aes(x = reorder(path_label, abs(beta)), y = beta, fill = sig)) +
    geom_col(width = 0.7) +
    geom_text(aes(label = sprintf("%.3f%s", beta, ifelse(pvalue < 0.001, "***",
                                                          ifelse(pvalue < 0.01, "**",
                                                                 ifelse(pvalue < 0.05, "*", ""))))),
              hjust = ifelse(paths$beta > 0, -0.1, 1.1), size = 3.5) +
    geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
    scale_fill_manual(values = c("TRUE" = "#2E86AB", "FALSE" = "gray70"),
                      labels = c("TRUE" = "p < 0.05", "FALSE" = "p ≥ 0.05")) +
    coord_flip() +
    labs(
      title = title,
      subtitle = "Standardized regression coefficients",
      x = "Path",
      y = "Standardized Coefficient (β)",
      fill = "Significance",
      caption = "*** p < 0.001, ** p < 0.01, * p < 0.05"
    ) +
    theme(legend.position = "bottom")
  
  return(p)
}

#' Plot factor loadings
plot_factor_loadings <- function(sem_fit, title = "Factor Loadings") {
  
  params <- standardizedSolution(sem_fit)
  
  loadings <- params %>%
    filter(op == "=~") %>%
    select(factor = lhs, indicator = rhs, loading = est.std) %>%
    mutate(factor = factor(factor))
  
  p <- ggplot(loadings, aes(x = indicator, y = loading, fill = factor)) +
    geom_col(width = 0.7) +
    geom_hline(yintercept = 0.7, linetype = "dashed", color = "red", alpha = 0.7) +
    geom_text(aes(label = sprintf("%.2f", loading)), vjust = -0.5, size = 3) +
    facet_wrap(~factor, scales = "free_x") +
    scale_y_continuous(limits = c(0, 1.1)) +
    labs(
      title = title,
      subtitle = "Standardized factor loadings (dashed line = 0.70 threshold)",
      x = "Indicator",
      y = "Loading",
      fill = "Factor"
    ) +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      legend.position = "none"
    )
  
  return(p)
}

#' Plot R-squared values
plot_r_squared <- function(sem_fit, title = "Variance Explained (R²)") {
  
  r2 <- lavInspect(sem_fit, "r2")
  
  r2_df <- data.frame(
    variable = names(r2),
    r_squared = as.numeric(r2)
  ) %>%
    arrange(desc(r_squared))
  
  p <- ggplot(r2_df, aes(x = reorder(variable, r_squared), y = r_squared)) +
    geom_col(fill = "#2E86AB", width = 0.7) +
    geom_text(aes(label = sprintf("%.1f%%", r_squared * 100)), 
              hjust = -0.1, size = 3.5) +
    coord_flip() +
    scale_y_continuous(limits = c(0, 1), labels = scales::percent) +
    labs(
      title = title,
      subtitle = "Proportion of variance explained by the model",
      x = "Variable",
      y = "R²"
    )
  
  return(p)
}

# ============================================================================
# Time Trend Visualizations
# ============================================================================

#' Plot time trends for funnel metrics
plot_time_trends <- function(data, metrics = NULL) {
  
  if (is.null(metrics)) {
    metrics <- FUNNEL_STAGES[FUNNEL_STAGES != "nps"]
  }
  
  # Aggregate by month
  monthly_data <- data %>%
    group_by(month, month_num) %>%
    summarise(across(all_of(metrics), ~mean(., na.rm = TRUE)), .groups = "drop") %>%
    pivot_longer(cols = all_of(metrics), names_to = "metric", values_to = "mean") %>%
    mutate(metric = factor(metric, levels = metrics))
  
  p <- ggplot(monthly_data, aes(x = month_num, y = mean, color = metric, group = metric)) +
    geom_line(linewidth = 1.2) +
    geom_point(size = 3) +
    scale_color_manual(values = FUNNEL_COLORS[metrics],
                       labels = FUNNEL_LABELS[metrics]) +
    scale_x_continuous(breaks = 1:max(monthly_data$month_num),
                       labels = paste0("M", sprintf("%02d", 1:max(monthly_data$month_num)))) +
    labs(
      title = "Funnel Metrics Over Time",
      subtitle = "Monthly average scores",
      x = "Month",
      y = "Mean Score (1-7 scale)",
      color = "Metric"
    ) +
    theme(legend.position = "right")
  
  return(p)
}

#' Plot time trends by region
plot_time_trends_by_region <- function(data, metric = "intent") {
  
  monthly_data <- data %>%
    group_by(month, month_num, region) %>%
    summarise(mean = mean(.data[[metric]], na.rm = TRUE), .groups = "drop")
  
  p <- ggplot(monthly_data, aes(x = month_num, y = mean, color = region, group = region)) +
    geom_line(linewidth = 1.2) +
    geom_point(size = 3) +
    scale_color_manual(values = REGION_COLORS) +
    scale_x_continuous(breaks = 1:max(monthly_data$month_num),
                       labels = paste0("M", sprintf("%02d", 1:max(monthly_data$month_num)))) +
    labs(
      title = paste(FUNNEL_LABELS[metric], "Over Time by Region"),
      x = "Month",
      y = "Mean Score",
      color = "Region"
    )
  
  return(p)
}

# ============================================================================
# Correlation and Comparison Plots
# ============================================================================

#' Create correlation matrix plot
plot_correlation_matrix <- function(data, variables = NULL, title = "Correlation Matrix") {
  
  if (is.null(variables)) {
    variables <- c(FUNNEL_STAGES, ALL_BENEFITS)
  }
  
  cor_matrix <- data %>%
    select(all_of(variables)) %>%
    cor(use = "pairwise.complete.obs")
  
  # Create plot
  corrplot(
    cor_matrix,
    method = "color",
    type = "upper",
    order = "hclust",
    addCoef.col = "black",
    number.cex = 0.6,
    tl.col = "black",
    tl.srt = 45,
    tl.cex = 0.8,
    col = colorRampPalette(c("#E8573F", "white", "#2A9D8F"))(200),
    title = title,
    mar = c(0, 0, 2, 0)
  )
}

#' Create segment comparison plot for key metrics
plot_segment_comparison <- function(data, metric = "intent") {
  
  segment_data <- data %>%
    group_by(region, segment) %>%
    summarise(
      mean = mean(.data[[metric]], na.rm = TRUE),
      se = sd(.data[[metric]], na.rm = TRUE) / sqrt(n()),
      .groups = "drop"
    )
  
  p <- ggplot(segment_data, aes(x = segment, y = mean, fill = region)) +
    geom_col(position = position_dodge(width = 0.8), width = 0.7) +
    geom_errorbar(aes(ymin = mean - 1.96*se, ymax = mean + 1.96*se),
                  position = position_dodge(width = 0.8), width = 0.25) +
    scale_fill_manual(values = REGION_COLORS) +
    labs(
      title = paste(FUNNEL_LABELS[metric], "by Segment and Region"),
      subtitle = "Mean scores with 95% confidence intervals",
      x = "Demographic Segment",
      y = "Mean Score",
      fill = "Region"
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  return(p)
}

#' Create NPS distribution plot
plot_nps_distribution <- function(data, by_group = NULL) {
  
  if (is.null(by_group)) {
    p <- ggplot(data, aes(x = nps, fill = nps_category)) +
      geom_histogram(binwidth = 1, color = "white") +
      scale_fill_manual(values = c("Detractor" = "#E8573F", 
                                    "Passive" = "#F4A261", 
                                    "Promoter" = "#2A9D8F")) +
      labs(
        title = "NPS Score Distribution",
        x = "NPS Score (0-10)",
        y = "Count",
        fill = "Category"
      )
  } else {
    nps_summary <- data %>%
      group_by(across(all_of(by_group)), nps_category) %>%
      summarise(n = n(), .groups = "drop") %>%
      group_by(across(all_of(by_group))) %>%
      mutate(pct = n / sum(n) * 100)
    
    p <- ggplot(nps_summary, aes(x = .data[[by_group]], y = pct, fill = nps_category)) +
      geom_col(position = "stack", width = 0.7) +
      scale_fill_manual(values = c("Detractor" = "#E8573F", 
                                    "Passive" = "#F4A261", 
                                    "Promoter" = "#2A9D8F")) +
      labs(
        title = paste("NPS Distribution by", by_group),
        x = by_group,
        y = "Percentage",
        fill = "Category"
      ) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
  }
  
  return(p)
}

# ============================================================================
# Dashboard-style Summary Plots
# ============================================================================

#' Create executive summary dashboard
create_executive_dashboard <- function(data, sem_fit = NULL) {
  
  # Funnel chart
  p1 <- plot_funnel_chart(data, title = "Marketing Funnel Performance")
  
  # Benefits by type
  p2 <- plot_benefits_radar(data)
  
  # Segment comparison for intent
  p3 <- plot_segment_comparison(data, "intent")
  
  # Time trends
  p4 <- plot_time_trends(data, c("awareness", "consideration", "intent"))
  
  # Combine plots using patchwork if available, otherwise return list
  if (has_patchwork) {
    dashboard <- (p1 + p2) / (p3 + p4) +
      patchwork::plot_annotation(
        title = "Japan Market Analysis - Executive Summary",
        subtitle = paste("Based on", nrow(data), "survey responses"),
        theme = theme(
          plot.title = element_text(size = 18, face = "bold"),
          plot.subtitle = element_text(size = 12, color = "gray40")
        )
      )
    return(dashboard)
  } else {
    # Return individual plots as a list
    return(list(funnel = p1, benefits = p2, segment = p3, trends = p4))
  }
}

#' Create segment deep-dive dashboard
create_segment_dashboard <- function(data, segment_name) {
  
  segment_data <- data %>% filter(segment == segment_name)
  
  p1 <- plot_funnel_chart(segment_data, by_group = "region",
                          title = paste(segment_name, "- Funnel by Region"))
  
  p2 <- plot_benefits_radar(segment_data, by_group = "region")
  
  p3 <- plot_nps_distribution(segment_data, by_group = "region")
  
  p4 <- plot_time_trends_by_region(segment_data, "intent")
  
  if (has_patchwork) {
    dashboard <- (p1 + p2) / (p3 + p4) +
      patchwork::plot_annotation(
        title = paste("Segment Deep-Dive:", segment_name),
        subtitle = paste("n =", nrow(segment_data), "respondents")
      )
    return(dashboard)
  } else {
    return(list(funnel = p1, benefits = p2, nps = p3, trends = p4))
  }
}

# ============================================================================
# Save Plots Function
# ============================================================================

#' Save all standard plots
save_all_plots <- function(data, sem_fit = NULL, output_dir = FIGURES_DIR) {
  
  message("Saving visualizations...")
  
  # Funnel plots
  ggsave(file.path(output_dir, "01_funnel_overall.png"),
         plot_funnel_chart(data), width = 10, height = 6, dpi = 300)
  
  ggsave(file.path(output_dir, "02_funnel_by_region.png"),
         plot_funnel_chart(data, "region"), width = 12, height = 6, dpi = 300)
  
  ggsave(file.path(output_dir, "03_funnel_conversion.png"),
         plot_funnel_conversion(data), width = 10, height = 6, dpi = 300)
  
  # Benefits plots
  ggsave(file.path(output_dir, "04_benefits_overall.png"),
         plot_benefits_radar(data), width = 12, height = 6, dpi = 300)
  
  ggsave(file.path(output_dir, "05_benefits_heatmap.png"),
         plot_benefits_heatmap(data), width = 14, height = 8, dpi = 300)
  
  # Time trends
  ggsave(file.path(output_dir, "06_time_trends.png"),
         plot_time_trends(data), width = 12, height = 6, dpi = 300)
  
  ggsave(file.path(output_dir, "07_intent_by_region_time.png"),
         plot_time_trends_by_region(data, "intent"), width = 10, height = 6, dpi = 300)
  
  # Segment comparisons
  ggsave(file.path(output_dir, "08_intent_by_segment.png"),
         plot_segment_comparison(data, "intent"), width = 12, height = 6, dpi = 300)
  
  # NPS
  ggsave(file.path(output_dir, "09_nps_distribution.png"),
         plot_nps_distribution(data), width = 10, height = 6, dpi = 300)
  
  ggsave(file.path(output_dir, "10_nps_by_segment.png"),
         plot_nps_distribution(data, "segment"), width = 12, height = 6, dpi = 300)
  
  # Correlation matrix
  png(file.path(output_dir, "11_correlation_matrix.png"), 
      width = 1200, height = 1000, res = 150)
  plot_correlation_matrix(data)
  dev.off()
  
  # SEM plots if model provided
  if (!is.null(sem_fit)) {
    ggsave(file.path(output_dir, "12_path_coefficients.png"),
           plot_path_coefficients(sem_fit), width = 10, height = 8, dpi = 300)
    
    ggsave(file.path(output_dir, "13_factor_loadings.png"),
           plot_factor_loadings(sem_fit), width = 12, height = 6, dpi = 300)
    
    ggsave(file.path(output_dir, "14_r_squared.png"),
           plot_r_squared(sem_fit), width = 8, height = 6, dpi = 300)
    
    # SEM path diagram (if semPlot available)
    if (has_semPlot) {
      png(file.path(output_dir, "15_sem_path_diagram.png"),
          width = 1400, height = 1000, res = 150)
      plot_sem_diagram(sem_fit, "SEM Path Model")
      dev.off()
    }
  }
  
  # Executive dashboard
  dashboard <- create_executive_dashboard(data)
  if (has_patchwork && inherits(dashboard, "patchwork")) {
    ggsave(file.path(output_dir, "16_executive_dashboard.png"),
           dashboard, width = 16, height = 12, dpi = 300)
  } else if (is.list(dashboard)) {
    # Save individual plots if patchwork not available
    ggsave(file.path(output_dir, "16a_dashboard_funnel.png"),
           dashboard$funnel, width = 10, height = 6, dpi = 300)
    ggsave(file.path(output_dir, "16b_dashboard_benefits.png"),
           dashboard$benefits, width = 10, height = 6, dpi = 300)
  }
  
  message(paste("All plots saved to:", output_dir))
}

# ============================================================================
# Run if executed as script
# ============================================================================

if (sys.nframe() == 0) {
  
  # Load processed data
  data_file <- file.path(DATA_PROCESSED_DIR, "survey_processed.rds")
  
  if (!file.exists(data_file)) {
    message("Processed data not found. Please run data preparation first.")
  } else {
    data <- readRDS(data_file)
    
    # Create sample plots
    message("Creating sample visualizations...")
    
    print(plot_funnel_chart(data))
    print(plot_benefits_heatmap(data))
    print(plot_segment_comparison(data, "intent"))
    
    message("Visualization module loaded successfully!")
  }
}
