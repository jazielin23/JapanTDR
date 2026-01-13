{{
    config(
        materialized='table'
    )
}}

/*
    TDR vs USJ Bipolar Comparison
    
    Captures head-to-head perceptual comparisons between Tokyo Disney Resort (TDR) and 
    Universal Studios Japan (USJ).
    
    Scale interpretation (7-point bipolar):
    - 1-2 = Strongly/Moderately favor TDR
    - 3 = Slightly favor TDR
    - 4 = Neutral / No difference
    - 5 = Slightly favor USJ
    - 6-7 = Moderately/Strongly favor USJ
    
    For TDR analysis: Lower scores = Better for TDR
*/

with survey as (
    select * from {{ ref('stg_survey_responses') }}
),

bipolar_analysis as (
    select
        respondent_id,
        segment_name,
        age_group,
        gender,
        geography,
        been_to_tdl_past_3yr,
        been_to_tds_past_3yr,
        recent_visit_usj_code,
        has_disney_fandom,
        
        -- ============================================================
        -- BIPOLAR COMPARISONS (1=TDR, 4=neutral, 7=USJ)
        -- ============================================================
        
        bipolar_fun,
        bipolar_feeling_special,
        bipolar_anticipation,
        bipolar_excitement,
        bipolar_playful_mind,
        bipolar_relaxed_content,
        bipolar_only_one,
        bipolar_oshi,
        bipolar_return_childhood,
        bipolar_trending,
        bipolar_realism,
        bipolar_innovative,
        bipolar_unpredictability,
        bipolar_refreshing_look,
        bipolar_edgy,
        bipolar_feel_refreshed,
        bipolar_heart_throbbing,
        bipolar_be_merry,
        bipolar_suspenseful,
        
        -- ============================================================
        -- CATEGORIZED PREFERENCES
        -- ============================================================
        
        case 
            when bipolar_fun <= 2 then 'Strong TDR'
            when bipolar_fun = 3 then 'Lean TDR'
            when bipolar_fun = 4 then 'Neutral'
            when bipolar_fun = 5 then 'Lean USJ'
            when bipolar_fun >= 6 then 'Strong USJ'
        end as fun_preference,
        
        case 
            when bipolar_innovative <= 2 then 'Strong TDR'
            when bipolar_innovative = 3 then 'Lean TDR'
            when bipolar_innovative = 4 then 'Neutral'
            when bipolar_innovative = 5 then 'Lean USJ'
            when bipolar_innovative >= 6 then 'Strong USJ'
        end as innovative_preference,
        
        case 
            when bipolar_trending <= 2 then 'Strong TDR'
            when bipolar_trending = 3 then 'Lean TDR'
            when bipolar_trending = 4 then 'Neutral'
            when bipolar_trending = 5 then 'Lean USJ'
            when bipolar_trending >= 6 then 'Strong USJ'
        end as trending_preference,
        
        -- ============================================================
        -- AGGREGATE SCORES
        -- ============================================================
        
        -- Average bipolar score (lower = more TDR preference)
        (coalesce(bipolar_fun, 4) + coalesce(bipolar_feeling_special, 4) + 
         coalesce(bipolar_anticipation, 4) + coalesce(bipolar_excitement, 4) +
         coalesce(bipolar_playful_mind, 4) + coalesce(bipolar_relaxed_content, 4) +
         coalesce(bipolar_only_one, 4) + coalesce(bipolar_oshi, 4) +
         coalesce(bipolar_return_childhood, 4) + coalesce(bipolar_trending, 4) +
         coalesce(bipolar_realism, 4) + coalesce(bipolar_innovative, 4) +
         coalesce(bipolar_unpredictability, 4) + coalesce(bipolar_refreshing_look, 4) +
         coalesce(bipolar_edgy, 4) + coalesce(bipolar_feel_refreshed, 4) +
         coalesce(bipolar_heart_throbbing, 4) + coalesce(bipolar_be_merry, 4) +
         coalesce(bipolar_suspenseful, 4)) / 19.0 as avg_bipolar_score,
        
        -- Count of TDR wins (scores 1-3)
        (case when bipolar_fun between 1 and 3 then 1 else 0 end +
         case when bipolar_feeling_special between 1 and 3 then 1 else 0 end +
         case when bipolar_anticipation between 1 and 3 then 1 else 0 end +
         case when bipolar_excitement between 1 and 3 then 1 else 0 end +
         case when bipolar_playful_mind between 1 and 3 then 1 else 0 end +
         case when bipolar_relaxed_content between 1 and 3 then 1 else 0 end +
         case when bipolar_only_one between 1 and 3 then 1 else 0 end +
         case when bipolar_oshi between 1 and 3 then 1 else 0 end +
         case when bipolar_return_childhood between 1 and 3 then 1 else 0 end +
         case when bipolar_trending between 1 and 3 then 1 else 0 end +
         case when bipolar_realism between 1 and 3 then 1 else 0 end +
         case when bipolar_innovative between 1 and 3 then 1 else 0 end +
         case when bipolar_unpredictability between 1 and 3 then 1 else 0 end +
         case when bipolar_refreshing_look between 1 and 3 then 1 else 0 end +
         case when bipolar_edgy between 1 and 3 then 1 else 0 end +
         case when bipolar_feel_refreshed between 1 and 3 then 1 else 0 end +
         case when bipolar_heart_throbbing between 1 and 3 then 1 else 0 end +
         case when bipolar_be_merry between 1 and 3 then 1 else 0 end +
         case when bipolar_suspenseful between 1 and 3 then 1 else 0 end) as tdr_wins_count,
        
        -- Count of USJ wins (scores 5-7)
        (case when bipolar_fun between 5 and 7 then 1 else 0 end +
         case when bipolar_feeling_special between 5 and 7 then 1 else 0 end +
         case when bipolar_anticipation between 5 and 7 then 1 else 0 end +
         case when bipolar_excitement between 5 and 7 then 1 else 0 end +
         case when bipolar_playful_mind between 5 and 7 then 1 else 0 end +
         case when bipolar_relaxed_content between 5 and 7 then 1 else 0 end +
         case when bipolar_only_one between 5 and 7 then 1 else 0 end +
         case when bipolar_oshi between 5 and 7 then 1 else 0 end +
         case when bipolar_return_childhood between 5 and 7 then 1 else 0 end +
         case when bipolar_trending between 5 and 7 then 1 else 0 end +
         case when bipolar_realism between 5 and 7 then 1 else 0 end +
         case when bipolar_innovative between 5 and 7 then 1 else 0 end +
         case when bipolar_unpredictability between 5 and 7 then 1 else 0 end +
         case when bipolar_refreshing_look between 5 and 7 then 1 else 0 end +
         case when bipolar_edgy between 5 and 7 then 1 else 0 end +
         case when bipolar_feel_refreshed between 5 and 7 then 1 else 0 end +
         case when bipolar_heart_throbbing between 5 and 7 then 1 else 0 end +
         case when bipolar_be_merry between 5 and 7 then 1 else 0 end +
         case when bipolar_suspenseful between 5 and 7 then 1 else 0 end) as usj_wins_count,
        
        -- Overall preference
        case
            when (coalesce(bipolar_fun, 4) + coalesce(bipolar_feeling_special, 4) + 
                  coalesce(bipolar_anticipation, 4) + coalesce(bipolar_excitement, 4) +
                  coalesce(bipolar_playful_mind, 4) + coalesce(bipolar_relaxed_content, 4) +
                  coalesce(bipolar_only_one, 4) + coalesce(bipolar_oshi, 4) +
                  coalesce(bipolar_return_childhood, 4)) / 9.0 < 3.5 then 'TDR Loyalist'
            when (coalesce(bipolar_fun, 4) + coalesce(bipolar_feeling_special, 4) + 
                  coalesce(bipolar_anticipation, 4) + coalesce(bipolar_excitement, 4) +
                  coalesce(bipolar_playful_mind, 4) + coalesce(bipolar_relaxed_content, 4) +
                  coalesce(bipolar_only_one, 4) + coalesce(bipolar_oshi, 4) +
                  coalesce(bipolar_return_childhood, 4)) / 9.0 > 4.5 then 'USJ Loyalist'
            else 'Switcher'
        end as overall_preference

    from survey
    -- Only include respondents who answered bipolar questions
    where bipolar_fun is not null
)

select * from bipolar_analysis
