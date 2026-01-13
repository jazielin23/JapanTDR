{{
    config(
        materialized='view'
    )
}}

/*
    Staging model for TDL survey responses
    
    IMPORTANT: All Likert scales are correctly oriented:
    - 5-point scales: 5 = High/Positive, 1 = Low/Negative
    - Bipolar scales: 1 = TDR preference, 7 = USJ preference, 4 = Neutral
    
    Source: Relabeled Raw Data.csv (validated column mappings)
*/

with source as (
    select * from {{ ref('survey_responses_tdl') }}
),

cleaned as (
    select
        -- Primary key
        respondent_id,
        
        -- Segment information
        segment_code,
        audience as segment_name,
        
        -- Demographics
        cast(nullif(gender, '') as integer) as gender_code,
        case 
            when gender = '1' then 'Male'
            when gender = '2' then 'Female'
            else null
        end as gender,
        cast(nullif(age, '') as integer) as age,
        case
            when cast(nullif(age, '') as integer) between 18 and 24 then '18-24'
            when cast(nullif(age, '') as integer) between 25 and 34 then '25-34'
            when cast(nullif(age, '') as integer) between 35 and 44 then '35-44'
            when cast(nullif(age, '') as integer) between 45 and 54 then '45-54'
            when cast(nullif(age, '') as integer) between 55 and 64 then '55-64'
            when cast(nullif(age, '') as integer) >= 65 then '65+'
            else 'Unknown'
        end as age_group,
        prefecture_code,
        geography,
        
        -- Marital status
        cast(nullif(marital_status, '') as integer) as marital_status_code,
        case
            when marital_status = '1' then 'Single'
            when marital_status = '2' then 'Married'
            when marital_status = '3' then 'Divorced'
            else null
        end as marital_status,
        
        -- Household composition (binary flags)
        cast(nullif(living_alone, '') as integer) as living_alone,
        cast(nullif(living_with_spouse, '') as integer) as living_with_spouse,
        cast(nullif(living_with_children, '') as integer) as living_with_children,
        cast(nullif(living_with_parents, '') as integer) as living_with_parents,
        
        -- Children in household
        case when boys_in_hh = 'Yes' then 1 else 0 end as has_boys_in_hh,
        case when girls_in_hh = 'Yes' then 1 else 0 end as has_girls_in_hh,
        case when has_grandchildren = '1' then 1 else 0 end as has_grandchildren,
        
        -- ============================================================
        -- VISIT BEHAVIOR (TDL Focus)
        -- ============================================================
        
        -- Recent visit (1=last month...9=never) - lower is more recent
        cast(nullif(recent_visit_tdl, '') as integer) as recent_visit_tdl_code,
        case 
            when recent_visit_tdl = '1' then 'Within 1 month'
            when recent_visit_tdl = '2' then '2-3 months ago'
            when recent_visit_tdl = '3' then '4-6 months ago'
            when recent_visit_tdl = '4' then '7-12 months ago'
            when recent_visit_tdl = '5' then '2 years ago'
            when recent_visit_tdl = '6' then '3 years ago'
            when recent_visit_tdl = '7' then '4-5 years ago'
            when recent_visit_tdl = '8' then 'More than 6 years ago'
            when recent_visit_tdl = '9' then 'Never visited'
            else null
        end as recent_visit_tdl,
        case when been_to_tdl_past_3yr = 'Yes' then 1 else 0 end as been_to_tdl_past_3yr,
        
        -- Visit count
        cast(nullif(visit_count_tdl, '') as integer) as visit_count_tdl_code,
        case
            when visit_count_tdl = '1' then 1
            when visit_count_tdl = '2' then 2
            when visit_count_tdl = '3' then 3
            when visit_count_tdl = '4' then 4
            when visit_count_tdl = '5' then 5
            when visit_count_tdl = '6' then 7  -- midpoint of 6-9
            when visit_count_tdl = '7' then 10
            when visit_count_tdl = '8' then 15 -- midpoint of 11-20
            when visit_count_tdl = '9' then 25 -- midpoint of 21-30
            when visit_count_tdl = '10' then 35 -- representing 31+
            else 0
        end as visit_count_tdl_estimated,
        
        -- TDS & USJ visit for comparison
        cast(nullif(recent_visit_tds, '') as integer) as recent_visit_tds_code,
        case when been_to_tds_past_3yr = 'Yes' then 1 else 0 end as been_to_tds_past_3yr,
        cast(nullif(recent_visit_usj, '') as integer) as recent_visit_usj_code,
        
        -- Decision maker
        cast(nullif(decision_maker, '') as integer) as decision_maker_code,
        cast(nullif(non_park_rejector, '') as integer) as non_park_rejector,
        
        -- ============================================================
        -- FUNNEL METRICS (5 = positive, 1 = negative)
        -- ============================================================
        
        -- Aided awareness (binary)
        cast(nullif(aided_awareness_tdl, '') as integer) as aided_awareness_tdl,
        cast(nullif(aided_awareness_tds, '') as integer) as aided_awareness_tds,
        cast(nullif(aided_awareness_usj, '') as integer) as aided_awareness_usj,
        
        -- Familiarity (5=very familiar, 1=not familiar at all)
        cast(nullif(familiarity_tdl, '') as integer) as familiarity_tdl,
        cast(nullif(familiarity_tds, '') as integer) as familiarity_tds,
        cast(nullif(familiarity_usj, '') as integer) as familiarity_usj,
        
        -- Opinion (5=excellent, 1=very bad)
        cast(nullif(opinion_tdl, '') as integer) as opinion_tdl,
        cast(nullif(opinion_tds, '') as integer) as opinion_tds,
        cast(nullif(opinion_usj, '') as integer) as opinion_usj,
        
        -- Consideration (5=would definitely, 1=would not at all)
        cast(nullif(consideration_tdl, '') as integer) as consideration_tdl,
        cast(nullif(consideration_tds, '') as integer) as consideration_tds,
        cast(nullif(consideration_usj, '') as integer) as consideration_usj,
        
        -- Likelihood to visit (5=definitely likely, 1=definitely not)
        cast(nullif(likelihood_visit_tdl, '') as integer) as likelihood_visit_tdl,
        cast(nullif(likelihood_visit_tds, '') as integer) as likelihood_visit_tds,
        cast(nullif(likelihood_visit_usj, '') as integer) as likelihood_visit_usj,
        
        -- Intent to visit
        case when intent_visit_tdl = 'Yes' then 1 else 0 end as intent_visit_tdl_12mo,
        
        -- NPS scores (0-10 scale)
        cast(nullif(nps_tdl, '') as integer) as nps_tdl,
        cast(nullif(nps_tds, '') as integer) as nps_tds,
        cast(nullif(nps_usj, '') as integer) as nps_usj,
        
        -- ============================================================
        -- TDL FUNCTIONAL ATTRIBUTES (5=strongly agree, 1=strongly disagree)
        -- ============================================================
        
        cast(nullif(tdl_func_relaxing, '') as integer) as tdl_func_relaxing,
        cast(nullif(tdl_func_enjoy_myself, '') as integer) as tdl_func_enjoy_myself,
        cast(nullif(tdl_func_lifelong_memories, '') as integer) as tdl_func_lifelong_memories,
        cast(nullif(tdl_func_bond_family_friends, '') as integer) as tdl_func_bond_family_friends,
        cast(nullif(tdl_func_great_for_kids_under_6, '') as integer) as tdl_func_great_for_kids_under_6,
        cast(nullif(tdl_func_great_for_kids_7_17, '') as integer) as tdl_func_great_for_kids_7_17,
        cast(nullif(tdl_func_great_for_adults, '') as integer) as tdl_func_great_for_adults,
        cast(nullif(tdl_func_want_children_experience, '') as integer) as tdl_func_want_children_experience,
        cast(nullif(tdl_func_expand_child_worldview, '') as integer) as tdl_func_expand_child_worldview,
        cast(nullif(tdl_func_great_for_all_family, '') as integer) as tdl_func_great_for_all_family,
        cast(nullif(tdl_func_understands_what_i_like, '') as integer) as tdl_func_understands_what_i_like,
        cast(nullif(tdl_func_feel_comfortable, '') as integer) as tdl_func_feel_comfortable,
        cast(nullif(tdl_func_keeping_up_with_times, '') as integer) as tdl_func_keeping_up_with_times,
        cast(nullif(tdl_func_variety_of_things, '') as integer) as tdl_func_variety_of_things,
        cast(nullif(tdl_func_unique_experiences, '') as integer) as tdl_func_unique_experiences,
        cast(nullif(tdl_func_repeat_experience, '') as integer) as tdl_func_repeat_experience,
        cast(nullif(tdl_func_active_adventurous, '') as integer) as tdl_func_active_adventurous,
        cast(nullif(tdl_func_thrilling, '') as integer) as tdl_func_thrilling,
        cast(nullif(tdl_func_new_innovative, '') as integer) as tdl_func_new_innovative,
        cast(nullif(tdl_func_something_new, '') as integer) as tdl_func_something_new,
        cast(nullif(tdl_func_not_crowded, '') as integer) as tdl_func_not_crowded,
        cast(nullif(tdl_func_character_interaction, '') as integer) as tdl_func_character_interaction,
        cast(nullif(tdl_func_worth_short_vacation, '') as integer) as tdl_func_worth_short_vacation,
        cast(nullif(tdl_func_worth_price, '') as integer) as tdl_func_worth_price,
        cast(nullif(tdl_func_affordable, '') as integer) as tdl_func_affordable,
        cast(nullif(tdl_func_ticket_options, '') as integer) as tdl_func_ticket_options,
        
        -- ============================================================
        -- TDL EMOTIONAL ATTRIBUTES (5=strongly agree, 1=strongly disagree)
        -- ============================================================
        
        cast(nullif(tdl_emot_land_of_dreams, '') as integer) as tdl_emot_land_of_dreams,
        cast(nullif(tdl_emot_removed_from_reality, '') as integer) as tdl_emot_removed_from_reality,
        cast(nullif(tdl_emot_fantastical, '') as integer) as tdl_emot_fantastical,
        cast(nullif(tdl_emot_heartwarming, '') as integer) as tdl_emot_heartwarming,
        cast(nullif(tdl_emot_soothing_healing, '') as integer) as tdl_emot_soothing_healing,
        cast(nullif(tdl_emot_feeling_safe, '') as integer) as tdl_emot_feeling_safe,
        cast(nullif(tdl_emot_longing_aspiring, '') as integer) as tdl_emot_longing_aspiring,
        cast(nullif(tdl_emot_sparkling, '') as integer) as tdl_emot_sparkling,
        cast(nullif(tdl_emot_premium_feeling, '') as integer) as tdl_emot_premium_feeling,
        cast(nullif(tdl_emot_feel_good, '') as integer) as tdl_emot_feel_good,
        
        -- ============================================================
        -- BIPOLAR COMPARISONS (1=TDR, 4=neutral, 7=USJ)
        -- ============================================================
        
        cast(nullif(bipolar_fun, '') as integer) as bipolar_fun,
        cast(nullif(bipolar_feeling_special, '') as integer) as bipolar_feeling_special,
        cast(nullif(bipolar_anticipation, '') as integer) as bipolar_anticipation,
        cast(nullif(bipolar_excitement, '') as integer) as bipolar_excitement,
        cast(nullif(bipolar_playful_mind, '') as integer) as bipolar_playful_mind,
        cast(nullif(bipolar_relaxed_content, '') as integer) as bipolar_relaxed_content,
        cast(nullif(bipolar_only_one, '') as integer) as bipolar_only_one,
        cast(nullif(bipolar_oshi, '') as integer) as bipolar_oshi,
        cast(nullif(bipolar_return_childhood, '') as integer) as bipolar_return_childhood,
        cast(nullif(bipolar_trending, '') as integer) as bipolar_trending,
        cast(nullif(bipolar_realism, '') as integer) as bipolar_realism,
        cast(nullif(bipolar_innovative, '') as integer) as bipolar_innovative,
        cast(nullif(bipolar_unpredictability, '') as integer) as bipolar_unpredictability,
        cast(nullif(bipolar_refreshing_look, '') as integer) as bipolar_refreshing_look,
        cast(nullif(bipolar_edgy, '') as integer) as bipolar_edgy,
        cast(nullif(bipolar_feel_refreshed, '') as integer) as bipolar_feel_refreshed,
        cast(nullif(bipolar_heart_throbbing, '') as integer) as bipolar_heart_throbbing,
        cast(nullif(bipolar_be_merry, '') as integer) as bipolar_be_merry,
        cast(nullif(bipolar_suspenseful, '') as integer) as bipolar_suspenseful,
        
        -- ============================================================
        -- DISNEY FANDOM
        -- ============================================================
        
        cast(nullif(funderful_disney_member, '') as integer) as funderful_disney_member,
        cast(nullif(disney_plus_subscriber, '') as integer) as disney_plus_subscriber,
        cast(nullif(disney_card_club_member, '') as integer) as disney_card_club_member,
        cast(nullif(disney_store_card_member, '') as integer) as disney_store_card_member,
        case when disney_fandom = 'Yes' then 1 else 0 end as has_disney_fandom,
        
        -- Income
        cast(nullif(annual_personal_income, '') as integer) as annual_personal_income,
        cast(nullif(annual_household_income, '') as integer) as annual_household_income

    from source
)

select * from cleaned
