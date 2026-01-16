#!/usr/bin/env python3
"""
Extract and properly format Tokyo Disneyland (TDL) focused survey data.
Creates clean CSV files for dbt modeling.

Updated: Now reads from 6-wave dataset (February-July, waves 1-6)

Likert Scale Mappings (all confirmed from Relabeled Raw Data):
- 5-point scales: 5=High/Positive, 1=Low/Negative
- Bipolar scales: 1=Definitely TDR, 4=Neutral, 7=Definitely USJ
"""

import csv
import os

# Wave to Month mapping (Wave 1 = February, Wave 6 = July)
WAVE_TO_MONTH = {
    1: 'February',
    2: 'March',
    3: 'April',
    4: 'May',
    5: 'June',
    6: 'July'
}

def main():
    # Updated to use the 6-wave dataset
    input_file = "/workspace/japan_market_analysis/Final Data for 6 waves.csv"
    output_dir = "/workspace/japan_market_analysis/dbt_project/seeds"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Column mappings based on analysis
    # NOTE: All indices shifted by +1 due to Wave column at position 0
    WAVE_COL = 0  # New Wave column
    OFFSET = 1  # Offset to add to all original column indices
    
    COLUMNS = {
        # Demographics (original 0-indexed, now +1)
        'segment_code': 0 + OFFSET,
        'audience': 1 + OFFSET,
        'gender': 2 + OFFSET,
        'age': 3 + OFFSET,
        'prefecture_code': 4 + OFFSET,
        'geography': 5 + OFFSET,
        'marital_status': 6 + OFFSET,
        
        # Household composition
        'living_alone': 7 + OFFSET,
        'living_with_spouse': 8 + OFFSET,
        'living_with_significant_other': 9 + OFFSET,
        'living_with_children': 10 + OFFSET,
        'living_with_parents': 11 + OFFSET,
        'living_with_siblings': 12 + OFFSET,
        'living_with_friend': 13 + OFFSET,
        'living_with_other': 14 + OFFSET,
        
        # Children flags
        'has_children_separate': 15 + OFFSET,
        'boys_under_17_in_hh': 25 + OFFSET,
        'boys_in_hh': 26 + OFFSET,
        'girls_under_17_in_hh': 38 + OFFSET,
        'girls_in_hh': 39 + OFFSET,
        'has_grandchildren': 42 + OFFSET,
        
        # Visit recency (1=within month ... 9=never)
        'recent_visit_tdl': 66 + OFFSET,
        'been_to_tdl_past_3yr': 67 + OFFSET,
        'recent_visit_tds': 68 + OFFSET,
        'been_to_tds_past_3yr': 69 + OFFSET,
        'recent_visit_usj': 70 + OFFSET,
        
        # Visit frequency (1=1 time ... 10=31+)
        'visit_count_tdl': 71 + OFFSET,
        'visit_count_tds': 72 + OFFSET,
        'visit_count_usj': 73 + OFFSET,
        
        # Decision maker
        'decision_maker': 74 + OFFSET,
        'non_park_rejector': 75 + OFFSET,
        
        # Aided awareness (0/1)
        'aided_awareness_tdl': 76 + OFFSET,
        'aided_awareness_tds': 77 + OFFSET,
        'aided_awareness_usj': 78 + OFFSET,
        
        # Funnel metrics (5=high, 1=low)
        'familiarity_tdl': 86 + OFFSET,
        'familiarity_tds': 87 + OFFSET,
        'familiarity_usj': 88 + OFFSET,
        
        'opinion_tdl': 94 + OFFSET,
        'opinion_tds': 95 + OFFSET,
        'opinion_usj': 96 + OFFSET,
        
        'consideration_tdl': 102 + OFFSET,
        'consideration_tds': 103 + OFFSET,
        'consideration_usj': 104 + OFFSET,
        
        'likelihood_visit_tdl': 110 + OFFSET,
        'likelihood_visit_tds': 111 + OFFSET,
        'likelihood_visit_usj': 112 + OFFSET,
        
        # Visit timing
        'when_visit_tdl': 118 + OFFSET,
        'intent_visit_tdl_code': 119 + OFFSET,
        'intent_visit_tdl': 120 + OFFSET,
        'when_visit_tds': 121 + OFFSET,
        'intent_visit_tds_code': 122 + OFFSET,
        'intent_visit_tds_or_tdl': 123 + OFFSET,
        'intent_visit_tds': 124 + OFFSET,
        
        # NPS
        'nps_tdl': 137 + OFFSET,
        'nps_tds': 138 + OFFSET,
        'nps_usj': 139 + OFFSET,
        
        # Disney fandom
        'funderful_disney_member': 272 + OFFSET,
        'disney_plus_subscriber': 273 + OFFSET,
        'disney_card_club_member': 274 + OFFSET,
        'disney_store_card_member': 275 + OFFSET,
        'disney_vacation_club_member': 276 + OFFSET,
        'no_disney_fandom': 277 + OFFSET,
        'disney_fandom': 278 + OFFSET,
        
        # Income
        'annual_personal_income': 279 + OFFSET,
        'annual_household_income': 280 + OFFSET,
    }
    
    # TDL Functional Attributes (F) - columns 145-170, shifted by +1
    TDL_FUNCTIONAL_ATTRS = {
        'relaxing': 145 + OFFSET,
        'enjoy_myself': 146 + OFFSET,
        'lifelong_memories': 147 + OFFSET,
        'bond_family_friends': 148 + OFFSET,
        'great_for_kids_under_6': 149 + OFFSET,
        'great_for_kids_7_17': 150 + OFFSET,
        'great_for_adults': 151 + OFFSET,
        'want_children_experience': 152 + OFFSET,
        'expand_child_worldview': 153 + OFFSET,
        'great_for_all_family': 154 + OFFSET,
        'understands_what_i_like': 155 + OFFSET,
        'feel_comfortable': 156 + OFFSET,
        'keeping_up_with_times': 157 + OFFSET,
        'variety_of_things': 158 + OFFSET,
        'unique_experiences': 159 + OFFSET,
        'repeat_experience': 160 + OFFSET,
        'active_adventurous': 161 + OFFSET,
        'thrilling': 162 + OFFSET,
        'new_innovative': 163 + OFFSET,
        'something_new': 164 + OFFSET,
        'not_crowded': 165 + OFFSET,
        'character_interaction': 166 + OFFSET,
        'worth_short_vacation': 167 + OFFSET,
        'worth_price': 168 + OFFSET,
        'affordable': 169 + OFFSET,
        'ticket_options': 170 + OFFSET,
    }
    
    # TDL Emotional Attributes (E) - columns 171-180, shifted by +1
    TDL_EMOTIONAL_ATTRS = {
        'land_of_dreams': 171 + OFFSET,
        'removed_from_reality': 172 + OFFSET,
        'fantastical': 173 + OFFSET,
        'heartwarming': 174 + OFFSET,
        'soothing_healing': 175 + OFFSET,
        'feeling_safe': 176 + OFFSET,
        'longing_aspiring': 177 + OFFSET,
        'sparkling': 178 + OFFSET,
        'premium_feeling': 179 + OFFSET,
        'feel_good': 180 + OFFSET,
    }
    
    # Bipolar scales (1=TDR, 7=USJ), shifted by +1
    BIPOLAR_ATTRS = {
        'bipolar_fun': 253 + OFFSET,
        'bipolar_feeling_special': 254 + OFFSET,
        'bipolar_anticipation': 255 + OFFSET,
        'bipolar_excitement': 256 + OFFSET,
        'bipolar_playful_mind': 257 + OFFSET,
        'bipolar_relaxed_content': 258 + OFFSET,
        'bipolar_only_one': 259 + OFFSET,
        'bipolar_oshi': 260 + OFFSET,
        'bipolar_return_childhood': 261 + OFFSET,
        'bipolar_trending': 262 + OFFSET,
        'bipolar_realism': 263 + OFFSET,
        'bipolar_innovative': 264 + OFFSET,
        'bipolar_unpredictability': 265 + OFFSET,
        'bipolar_refreshing_look': 266 + OFFSET,
        'bipolar_edgy': 267 + OFFSET,
        'bipolar_feel_refreshed': 268 + OFFSET,
        'bipolar_heart_throbbing': 269 + OFFSET,
        'bipolar_be_merry': 270 + OFFSET,
        'bipolar_suspenseful': 271 + OFFSET,
    }
    
    # Try multiple encodings for Japanese data
    encodings = ['utf-8', 'cp1252', 'shift_jis', 'cp932', 'utf-8-sig']
    f = None
    for enc in encodings:
        try:
            f = open(input_file, 'r', encoding=enc)
            # Try to read first line to verify encoding works
            test_line = f.readline()
            f.seek(0)  # Reset to beginning
            print(f"Successfully opened with encoding: {enc}")
            break
        except (UnicodeDecodeError, UnicodeError):
            if f:
                f.close()
            continue
    
    if f is None:
        raise ValueError(f"Could not decode file with any of: {encodings}")
    
    with f:
        reader = csv.reader(f)
        headers = next(reader)
        
        # Create output files
        respondent_rows = []
        attr_rows = []
        
        respondent_id = 0
        for row in reader:
            respondent_id += 1
            
            # Extract wave number and month
            wave = int(row[WAVE_COL]) if row[WAVE_COL] else 1
            month = WAVE_TO_MONTH.get(wave, 'Unknown')
            
            # Extract respondent data
            resp = {
                'respondent_id': respondent_id,
                'wave': wave,
                'month': month
            }
            
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
    
    # Add wave/month metadata first
    dict_rows.append({
        'column_name': 'wave',
        'original_column_index': 0,
        'category': 'survey_metadata',
        'scale_description': '1=February, 2=March, 3=April, 4=May, 5=June, 6=July',
        'park': 'all'
    })
    dict_rows.append({
        'column_name': 'month',
        'original_column_index': 0,
        'category': 'survey_metadata',
        'scale_description': 'Month name derived from wave',
        'park': 'all'
    })
    
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
