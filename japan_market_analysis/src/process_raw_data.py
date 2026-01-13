#!/usr/bin/env python3
"""
Process Raw Survey Data for SEM Analysis
=========================================

This script transforms the raw Brand Tracking Survey data into the format 
expected by the SEM analysis R scripts, matching the synthetic data structure.

Key mappings:
- Demographics: SC1 (gender), SC2 (age), SC3 (prefecture), SC4 (marital status)
- Funnel Variables: Q1-Q6 for theme parks (columns 1=TDL, 2=TDS)
- Brand Attributes: Q7 (TDL), Q8 (TDS), Q9 (USJ) - 38 items each
- Segments derived from Quota variable

Author: Data Analysis Team
Date: 2025
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Create output directory if it doesn't exist
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Configuration: Variable Mappings
# =============================================================================

# Brand attribute mapping (Q7/Q8/Q9 item index -> synthetic variable category)
# Based on the questionnaire structure in the Word document

BRAND_ATTRIBUTE_MAPPING = {
    # Emotional benefits (map to emot_* variables)
    1: ('emot_relaxation', 'Offers an escape from everyday'),
    2: ('emot_relaxation', 'Is relaxing'),
    3: ('emot_connection', 'Is a place where I feel welcomed'),
    5: ('emot_memorable', 'Builds lifelong special memories'),
    6: ('emot_connection', 'Allows me to bond with family and/or friends'),
    14: ('emot_connection', 'Makes me feel comfortable, as if I am with friends'),
    33: ('emot_authenticity', 'Land of dreams'),
    34: ('emot_authenticity', 'Removed from reality'),
    35: ('emot_authenticity', 'Fantastical'),
    36: ('emot_connection', 'Heart warming'),
    37: ('emot_relaxation', 'Soothing/healing'),
    
    # Excitement/thrilling
    19: ('emot_excitement', 'Offers active and adventurous experiences'),
    20: ('emot_excitement', 'Offers thrilling experiences'),
    21: ('emot_excitement', 'Offers new, innovative experiences'),
    22: ('emot_excitement', 'Always has something new to see and do'),
    
    # Functional benefits (map to func_* variables)
    16: ('func_variety', 'Offers a variety of things to do'),
    17: ('func_quality', 'Offers experiences not available anywhere else'),
    23: ('func_convenience', 'Is not overly crowded'),
    25: ('func_quality', 'Is a place worth visiting for a short vacation'),
    27: ('func_convenience', 'Offers flexibility so I can change my plans'),
    28: ('func_convenience', 'Offers customization'),
    29: ('func_value', 'Worth the price to go'),
    30: ('func_value', 'Is affordable'),
    31: ('func_value', 'Offers multiple price points'),
    32: ('func_value', 'Is something I feel good about spending my money on'),
    38: ('func_reliability', 'Feeling safe'),
}

# Prefecture to Region mapping (Local = Greater Tokyo + major prefectures)
# SC3 codes based on Japanese prefecture numbering
LOCAL_PREFECTURE_CODES = [
    11, 12, 13, 14,  # Greater Tokyo: Saitama, Chiba, Tokyo, Kanagawa
    23, 27, 40, 1    # Major: Aichi, Osaka, Fukuoka, Hokkaido
]

# Segment mapping from Quota patterns
SEGMENT_PATTERNS = {
    'A': 'Young Families',
    'B': 'Matured Families', 
    'C': 'Young Adults',
    'D': 'Young Couples',
    'E': 'Matured Adults 35+'
}


def load_raw_data(excel_path: str) -> pd.DataFrame:
    """Load raw survey data from Excel file."""
    print(f"Loading data from: {excel_path}")
    xlsx = pd.ExcelFile(excel_path)
    df = pd.read_excel(xlsx, sheet_name='Rawdata w11')
    print(f"Loaded {len(df)} respondents with {len(df.columns)} columns")
    return df


def extract_segment(quota_str: str) -> str:
    """Extract demographic segment from Quota string."""
    if pd.isna(quota_str):
        return 'Unknown'
    # Pattern: "XXX．X【地域】性別　ブランド"
    # Extract the letter after "．" 
    for pattern, segment in SEGMENT_PATTERNS.items():
        if f'．{pattern}【' in str(quota_str):
            return segment
    return 'Unknown'


def extract_region(prefecture_code: int) -> str:
    """Map prefecture code to region (Local/Domestic)."""
    if pd.isna(prefecture_code):
        return 'Unknown'
    return 'Local' if int(prefecture_code) in LOCAL_PREFECTURE_CODES else 'Domestic'


def extract_gender(gender_code: int) -> str:
    """Map gender code to string."""
    if pd.isna(gender_code):
        return 'Unknown'
    return {1: 'Male', 2: 'Female'}.get(int(gender_code), 'Other')


def recode_funnel_variable(value, var_type='likert'):
    """
    Recode funnel variables to 1-7 scale (matching synthetic data).
    Raw data uses various scales that need harmonization.
    """
    if pd.isna(value) or value == 99:  # 99 is often "Don't know"
        return np.nan
    
    value = float(value)
    
    # Most variables use 1-5 scale, convert to 1-7
    if var_type == 'likert':
        if value <= 5:
            # Map 1-5 to 1-7: (x-1) * 1.5 + 1
            return (value - 1) * 1.5 + 1
    
    return value


def compute_benefit_scores(df: pd.DataFrame, brand_prefix: str) -> dict:
    """
    Compute aggregated benefit scores from brand attribute items.
    
    Args:
        df: DataFrame with raw data
        brand_prefix: 'Q7-' for TDL, 'Q8-' for TDS, 'Q9-' for USJ
    
    Returns:
        Dictionary of computed benefit variables
    """
    results = {
        'func_convenience': [],
        'func_value': [],
        'func_quality': [],
        'func_variety': [],
        'func_reliability': [],
        'emot_excitement': [],
        'emot_relaxation': [],
        'emot_connection': [],
        'emot_authenticity': [],
        'emot_memorable': []
    }
    
    # Group attribute items by benefit category
    category_items = {}
    for item_num, (category, desc) in BRAND_ATTRIBUTE_MAPPING.items():
        if category not in category_items:
            category_items[category] = []
        category_items[category].append(item_num)
    
    for idx in range(len(df)):
        row = df.iloc[idx]
        for category, items in category_items.items():
            values = []
            for item_num in items:
                col_name = f'{brand_prefix}{item_num}'
                if col_name in df.columns:
                    val = row[col_name]
                    if not pd.isna(val) and val != 99:
                        # Convert 1-5 to 1-7 scale
                        converted = (float(val) - 1) * 1.5 + 1
                        values.append(converted)
            
            # Compute mean if we have values
            if values:
                results[category].append(np.mean(values))
            else:
                results[category].append(np.nan)
    
    return results


def process_raw_data(input_path: str, output_dir: str) -> pd.DataFrame:
    """
    Main processing function to transform raw data to analysis format.
    
    Focus on TDR (Tokyo Disney Resort) - combines TDL and TDS data.
    """
    
    # Load raw data
    raw_df = load_raw_data(input_path)
    
    # Initialize processed dataframe
    n_resp = len(raw_df)
    processed = pd.DataFrame()
    
    # ==========================================================================
    # 1. Generate respondent ID and metadata
    # ==========================================================================
    processed['respondent_id'] = [f'R{i+1:05d}' for i in range(n_resp)]
    processed['month'] = 'M11'  # Wave 11 data
    
    # ==========================================================================
    # 2. Demographics
    # ==========================================================================
    print("Processing demographics...")
    processed['segment'] = raw_df['Quota'].apply(extract_segment)
    processed['region'] = raw_df['SC3'].apply(extract_region)
    processed['prefecture'] = raw_df['SC3'].astype(str)
    processed['gender'] = raw_df['SC1'].apply(extract_gender)
    processed['age'] = raw_df['SC2']
    
    # Household composition (simplified)
    processed['household_size'] = 2  # Default, would need more processing
    
    # Has children (derived from segment)
    processed['has_children'] = processed['segment'].isin(['Young Families', 'Matured Families'])
    
    # Relationship status (from SC4 if available)
    processed['relationship_status'] = 'Unknown'
    
    # Income bracket (would need SC14 processing)
    processed['income_bracket'] = 'Unknown'
    
    # ==========================================================================
    # 3. Marketing Funnel Variables (for TDR - use TDL column '-1')
    # ==========================================================================
    print("Processing funnel variables...")
    
    # Q1: Awareness (1-5 scale in raw, convert to 1-7)
    processed['awareness'] = raw_df['Q1-1'].apply(lambda x: recode_funnel_variable(x))
    
    # Q2: Familiarity (1-5 scale)
    processed['familiarity'] = raw_df['Q2-1'].apply(lambda x: recode_funnel_variable(x))
    
    # Q3: Opinion (1-5 scale)
    processed['opinion'] = raw_df['Q3-1'].apply(lambda x: recode_funnel_variable(x))
    
    # Q4: Consideration (1-5 scale)
    processed['consideration'] = raw_df['Q4-1'].apply(lambda x: recode_funnel_variable(x))
    
    # Q5: Likelihood (1-8 scale in some cases)
    processed['likelihood'] = raw_df['Q5-1'].apply(lambda x: recode_funnel_variable(x))
    
    # Intent: Use average of consideration and likelihood as proxy
    processed['intent'] = (processed['consideration'] + processed['likelihood']) / 2
    
    # ==========================================================================
    # 4. NPS (Q6 appears to be visit timing, not NPS in this data)
    # Use Q10-1 which has 0-10 scale for overall brand metrics
    # ==========================================================================
    # For now, create a synthetic NPS from opinion and likelihood
    processed['nps'] = ((processed['opinion'] + processed['likelihood']) / 2 - 1) * (10/6)
    
    # ==========================================================================
    # 5. Brand Benefits from Q7 (TDL), Q8 (TDS), Q9 (USJ)
    # ==========================================================================
    print("Processing brand benefit attributes...")
    
    # Determine which brand attributes each respondent answered
    # Q7 = TDL, Q8 = TDS, Q9 = USJ
    # Prioritize TDL (Q7), then TDS (Q8)
    
    # Initialize benefit columns
    benefit_cols = [
        'func_convenience', 'func_value', 'func_quality', 'func_variety', 'func_reliability',
        'emot_excitement', 'emot_relaxation', 'emot_connection', 'emot_authenticity', 'emot_memorable'
    ]
    
    for col in benefit_cols:
        processed[col] = np.nan
    
    # Process Q7 (TDL) benefits
    q7_benefits = compute_benefit_scores(raw_df, 'Q7-')
    for col in benefit_cols:
        processed[col] = q7_benefits[col]
    
    # Fill missing with Q8 (TDS) benefits
    q8_benefits = compute_benefit_scores(raw_df, 'Q8-')
    for col in benefit_cols:
        mask = processed[col].isna()
        for i, val in enumerate(q8_benefits[col]):
            if mask.iloc[i] and not pd.isna(val):
                processed.loc[processed.index[i], col] = val
    
    # ==========================================================================
    # 6. Data Quality and Cleaning
    # ==========================================================================
    print("Cleaning data...")
    
    # Remove respondents with too many missing values
    key_vars = ['awareness', 'familiarity', 'opinion', 'consideration', 'likelihood']
    missing_pct = processed[key_vars].isna().sum(axis=1) / len(key_vars)
    processed = processed[missing_pct < 0.5].reset_index(drop=True)
    
    print(f"Final dataset: {len(processed)} respondents")
    
    # ==========================================================================
    # 7. Save processed data
    # ==========================================================================
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save as CSV
    csv_path = output_path / 'survey_processed.csv'
    processed.to_csv(csv_path, index=False)
    print(f"Saved processed data to: {csv_path}")
    
    # Also create data dictionary
    data_dict = pd.DataFrame({
        'variable': processed.columns,
        'description': [
            'Unique respondent identifier',
            'Survey month (M01-M12)',
            'Demographic segment',
            'Region: Local or Domestic',
            'Prefecture code',
            'Gender',
            'Age in years',
            'Number of people in household',
            'Has children (TRUE/FALSE)',
            'Relationship status',
            'Annual household income bracket',
            'Brand awareness (1-7 scale)',
            'Brand familiarity (1-7 scale)',
            'Favorable opinion (1-7 scale)',
            'Consideration for visit (1-7 scale)',
            'Likelihood to visit (1-7 scale)',
            'Intent to visit/return (1-7 scale)',
            'Net Promoter Score (0-10 scale)',
            'Convenience perception (1-7 scale)',
            'Value for money perception (1-7 scale)',
            'Quality experience perception (1-7 scale)',
            'Variety of options perception (1-7 scale)',
            'Reliability perception (1-7 scale)',
            'Excitement perception (1-7 scale)',
            'Relaxation perception (1-7 scale)',
            'Connection perception (1-7 scale)',
            'Authenticity perception (1-7 scale)',
            'Memorable experience perception (1-7 scale)'
        ][:len(processed.columns)],
        'type': [str(processed[col].dtype) for col in processed.columns]
    })
    
    dict_path = output_path / 'data_dictionary_raw.csv'
    data_dict.to_csv(dict_path, index=False)
    print(f"Saved data dictionary to: {dict_path}")
    
    return processed


def main():
    """Main entry point."""
    # Find the Excel file
    excel_file = PROJECT_ROOT / "240122_Brand Tracking Survey 2025wave11_table by segment_20251229.xlsx"
    
    if not excel_file.exists():
        print(f"Error: Excel file not found at {excel_file}")
        return None
    
    # Process the data
    processed_df = process_raw_data(
        str(excel_file),
        str(DATA_PROCESSED_DIR)
    )
    
    # Print summary statistics
    print("\n" + "="*60)
    print("PROCESSED DATA SUMMARY")
    print("="*60)
    print(f"\nTotal respondents: {len(processed_df)}")
    print(f"\nSegment distribution:")
    print(processed_df['segment'].value_counts())
    print(f"\nRegion distribution:")
    print(processed_df['region'].value_counts())
    
    print(f"\nFunnel variable means:")
    funnel_vars = ['awareness', 'familiarity', 'opinion', 'consideration', 'likelihood', 'intent']
    for var in funnel_vars:
        print(f"  {var}: {processed_df[var].mean():.2f}")
    
    print(f"\nBenefit variable means:")
    benefit_vars = ['func_convenience', 'func_value', 'func_quality', 'func_variety', 
                    'func_reliability', 'emot_excitement', 'emot_relaxation', 
                    'emot_connection', 'emot_authenticity', 'emot_memorable']
    for var in benefit_vars:
        if var in processed_df.columns:
            print(f"  {var}: {processed_df[var].mean():.2f}")
    
    return processed_df


if __name__ == "__main__":
    main()
