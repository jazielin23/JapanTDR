#!/usr/bin/env python3
"""
Extract and properly format Tokyo Disneyland (TDL) focused survey data.
Creates clean CSV files for dbt modeling.

Likert Scale Mappings (all confirmed from Relabeled Raw Data):
- 5-point scales: 5=High/Positive, 1=Low/Negative
- Bipolar scales: 1=Definitely TDR, 4=Neutral, 7=Definitely USJ
"""

import csv
import os

def main():
    input_file = "/workspace/japan_market_analysis/Relabeled Raw Data.csv"
    output_dir = "/workspace/japan_market_analysis/dbt_project/seeds"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Column mappings based on analysis
    COLUMNS = {
        # Demographics (0-indexed)
        'segment_code': 0,
        'audience': 1,
        'gender': 2,
        'age': 3,
        'prefecture_code': 4,
        'geography': 5,
        'marital_status': 6,
        
        # Household composition
        'living_alone': 7,
        'living_with_spouse': 8,
        'living_with_significant_other': 9,
        'living_with_children': 10,
        'living_with_parents': 11,
        'living_with_siblings': 12,
        'living_with_friend': 13,
        'living_with_other': 14,
        
        # Children flags
        'has_children_separate': 15,
        'boys_under_17_in_hh': 25,
        'boys_in_hh': 26,
        'girls_under_17_in_hh': 38,
        'girls_in_hh': 39,
        'has_grandchildren': 42,
        
        # Visit recency (1=within month ... 9=never)
        'recent_visit_tdl': 66,
        'been_to_tdl_past_3yr': 67,
        'recent_visit_tds': 68,
        'been_to_tds_past_3yr': 69,
        'recent_visit_usj': 70,
        
        # Visit frequency (1=1 time ... 10=31+)
        'visit_count_tdl': 71,
        'visit_count_tds': 72,
        'visit_count_usj': 73,
        
        # Decision maker
        'decision_maker': 74,
        'non_park_rejector': 75,
        
        # Aided awareness (0/1)
        'aided_awareness_tdl': 76,
        'aided_awareness_tds': 77,
        'aided_awareness_usj': 78,
        
        # Funnel metrics (5=high, 1=low)
        'familiarity_tdl': 86,
        'familiarity_tds': 87,
        'familiarity_usj': 88,
        
        'opinion_tdl': 94,
        'opinion_tds': 95,
        'opinion_usj': 96,
        
        'consideration_tdl': 102,
        'consideration_tds': 103,
        'consideration_usj': 104,
        
        'likelihood_visit_tdl': 110,
        'likelihood_visit_tds': 111,
        'likelihood_visit_usj': 112,
        
        # Visit timing
        'when_visit_tdl': 118,
        'intent_visit_tdl_code': 119,
        'intent_visit_tdl': 120,
        'when_visit_tds': 121,
        'intent_visit_tds_code': 122,
        'intent_visit_tds_or_tdl': 123,
        'intent_visit_tds': 124,
        
        # NPS
        'nps_tdl': 137,
        'nps_tds': 138,
        'nps_usj': 139,
        
        # Disney fandom
        'funderful_disney_member': 272,
        'disney_plus_subscriber': 273,
        'disney_card_club_member': 274,
        'disney_store_card_member': 275,
        'disney_vacation_club_member': 276,
        'no_disney_fandom': 277,
        'disney_fandom': 278,
        
        # Income
        'annual_personal_income': 279,
        'annual_household_income': 280,
    }
    
    # TDL Functional Attributes (F) - columns 145-170
    TDL_FUNCTIONAL_ATTRS = {
        'relaxing': 145,
        'enjoy_myself': 146,
        'lifelong_memories': 147,
        'bond_family_friends': 148,
        'great_for_kids_under_6': 149,
        'great_for_kids_7_17': 150,
        'great_for_adults': 151,
        'want_children_experience': 152,
        'expand_child_worldview': 153,
        'great_for_all_family': 154,
        'understands_what_i_like': 155,
        'feel_comfortable': 156,
        'keeping_up_with_times': 157,
        'variety_of_things': 158,
        'unique_experiences': 159,
        'repeat_experience': 160,
        'active_adventurous': 161,
        'thrilling': 162,
        'new_innovative': 163,
        'something_new': 164,
        'not_crowded': 165,
        'character_interaction': 166,
        'worth_short_vacation': 167,
        'worth_price': 168,
        'affordable': 169,
        'ticket_options': 170,
    }
    
    # TDL Emotional Attributes (E) - columns 171-180
    TDL_EMOTIONAL_ATTRS = {
        'land_of_dreams': 171,
        'removed_from_reality': 172,
        'fantastical': 173,
        'heartwarming': 174,
        'soothing_healing': 175,
        'feeling_safe': 176,
        'longing_aspiring': 177,
        'sparkling': 178,
        'premium_feeling': 179,
        'feel_good': 180,
    }
    
    # Bipolar scales (1=TDR, 7=USJ)
    BIPOLAR_ATTRS = {
        'bipolar_fun': 253,
        'bipolar_feeling_special': 254,
        'bipolar_anticipation': 255,
        'bipolar_excitement': 256,
        'bipolar_playful_mind': 257,
        'bipolar_relaxed_content': 258,
        'bipolar_only_one': 259,
        'bipolar_oshi': 260,
        'bipolar_return_childhood': 261,
        'bipolar_trending': 262,
        'bipolar_realism': 263,
        'bipolar_innovative': 264,
        'bipolar_unpredictability': 265,
        'bipolar_refreshing_look': 266,
        'bipolar_edgy': 267,
        'bipolar_feel_refreshed': 268,
        'bipolar_heart_throbbing': 269,
        'bipolar_be_merry': 270,
        'bipolar_suspenseful': 271,
    }
    
    with open(input_file, 'r', encoding='cp1252') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        # Create output files
        respondent_rows = []
        attr_rows = []
        
        respondent_id = 0
        for row in reader:
            respondent_id += 1
            
            # Extract respondent data
            resp = {'respondent_id': respondent_id}
            
            for col_name, col_idx in COLUMNS.items():
                val = row[col_idx] if col_idx < len(row) else ''
                resp[col_name] = val
            
            # Extract TDL functional attributes
            for attr_name, col_idx in TDL_FUNCTIONAL_ATTRS.items():
                val = row[col_idx] if col_idx < len(row) else ''
                resp[f'tdl_func_{attr_name}'] = val
            
            # Extract TDL emotional attributes
            for attr_name, col_idx in TDL_EMOTIONAL_ATTRS.items():
                val = row[col_idx] if col_idx < len(row) else ''
                resp[f'tdl_emot_{attr_name}'] = val
            
            # Extract bipolar attributes
            for attr_name, col_idx in BIPOLAR_ATTRS.items():
                val = row[col_idx] if col_idx < len(row) else ''
                resp[attr_name] = val
            
            respondent_rows.append(resp)
    
    # Write respondent data
    output_file = os.path.join(output_dir, 'survey_responses_tdl.csv')
    if respondent_rows:
        fieldnames = list(respondent_rows[0].keys())
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(respondent_rows)
        print(f"Written {len(respondent_rows)} respondents to {output_file}")
    
    # Create data dictionary
    dict_rows = []
    
    # Add column metadata
    scale_info = {
        'familiarity': '5=very familiar, 4=familiar, 3=neutral, 2=not familiar, 1=not familiar at all',
        'opinion': '5=excellent, 4=good, 3=neutral, 2=bad, 1=very bad',
        'consideration': '5=would definitely, 4=would, 3=might/might not, 2=would not, 1=would not at all',
        'likelihood': '5=definitely likely, 4=likely, 3=might/might not, 2=not likely, 1=definitely not',
        'functional_attr': '5=strongly agree, 4=agree, 3=neutral, 2=disagree, 1=strongly disagree',
        'emotional_attr': '5=strongly agree, 4=agree, 3=neutral, 2=disagree, 1=strongly disagree',
        'bipolar': '1=Definitely TDR, 2-3=Lean TDR, 4=Neutral, 5-6=Lean USJ, 7=Definitely USJ',
        'recent_visit': '1=last month, 2=2-3mo, 3=4-6mo, 4=7-12mo, 5=2yr, 6=3yr, 7=4-5yr, 8=6+yr, 9=never',
        'visit_count': '1=1x, 2=2x, 3=3x, 4=4x, 5=5x, 6=6-9x, 7=10x, 8=11-20x, 9=21-30x, 10=31+',
    }
    
    for col, idx in COLUMNS.items():
        scale_type = ''
        if 'familiarity' in col:
            scale_type = scale_info['familiarity']
        elif 'opinion' in col:
            scale_type = scale_info['opinion']
        elif 'consideration' in col:
            scale_type = scale_info['consideration']
        elif 'likelihood' in col:
            scale_type = scale_info['likelihood']
        elif 'recent_visit' in col:
            scale_type = scale_info['recent_visit']
        elif 'visit_count' in col:
            scale_type = scale_info['visit_count']
        
        dict_rows.append({
            'column_name': col,
            'original_column_index': idx,
            'category': 'demographics' if idx < 43 else 'behavior' if idx < 100 else 'perception',
            'scale_description': scale_type,
            'park': 'TDL' if 'tdl' in col else 'TDS' if 'tds' in col else 'USJ' if 'usj' in col else 'all'
        })
    
    for col, idx in TDL_FUNCTIONAL_ATTRS.items():
        dict_rows.append({
            'column_name': f'tdl_func_{col}',
            'original_column_index': idx,
            'category': 'functional_attribute',
            'scale_description': scale_info['functional_attr'],
            'park': 'TDL'
        })
    
    for col, idx in TDL_EMOTIONAL_ATTRS.items():
        dict_rows.append({
            'column_name': f'tdl_emot_{col}',
            'original_column_index': idx,
            'category': 'emotional_attribute',
            'scale_description': scale_info['emotional_attr'],
            'park': 'TDL'
        })
    
    for col, idx in BIPOLAR_ATTRS.items():
        dict_rows.append({
            'column_name': col,
            'original_column_index': idx,
            'category': 'bipolar_comparison',
            'scale_description': scale_info['bipolar'],
            'park': 'TDR_vs_USJ'
        })
    
    dict_file = os.path.join(output_dir, 'data_dictionary.csv')
    with open(dict_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['column_name', 'original_column_index', 'category', 'scale_description', 'park'])
        writer.writeheader()
        writer.writerows(dict_rows)
    print(f"Written data dictionary to {dict_file}")

if __name__ == '__main__':
    main()
