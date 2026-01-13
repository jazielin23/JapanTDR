{{
    config(
        materialized='table'
    )
}}

/*
    TDL Attribute Perceptions
    
    Captures how respondents perceive TDL on functional and emotional attributes.
    
    Scale interpretation (5-point Likert):
    - 5 = Strongly agree / High rating
    - 4 = Agree
    - 3 = Neutral
    - 2 = Disagree
    - 1 = Strongly disagree / Low rating
    
    Higher scores = More positive perception
*/

with survey as (
    select * from {{ ref('stg_survey_responses') }}
),

attribute_scores as (
    select
        respondent_id,
        segment_name,
        age_group,
        gender,
        geography,
        been_to_tdl_past_3yr,
        visit_count_tdl_estimated,
        has_disney_fandom,
        
        -- ============================================================
        -- FUNCTIONAL ATTRIBUTES (26 items, scale: 1-5)
        -- ============================================================
        
        -- Experience Quality
        tdl_func_relaxing,
        tdl_func_enjoy_myself,
        tdl_func_lifelong_memories,
        tdl_func_bond_family_friends,
        
        -- Family Suitability  
        tdl_func_great_for_kids_under_6,
        tdl_func_great_for_kids_7_17,
        tdl_func_great_for_adults,
        tdl_func_want_children_experience,
        tdl_func_expand_child_worldview,
        tdl_func_great_for_all_family,
        
        -- Personal Connection
        tdl_func_understands_what_i_like,
        tdl_func_feel_comfortable,
        
        -- Innovation & Variety
        tdl_func_keeping_up_with_times,
        tdl_func_variety_of_things,
        tdl_func_unique_experiences,
        tdl_func_repeat_experience,
        
        -- Excitement
        tdl_func_active_adventurous,
        tdl_func_thrilling,
        tdl_func_new_innovative,
        tdl_func_something_new,
        
        -- Practical Concerns
        tdl_func_not_crowded,
        tdl_func_character_interaction,
        tdl_func_worth_short_vacation,
        tdl_func_worth_price,
        tdl_func_affordable,
        tdl_func_ticket_options,
        
        -- ============================================================
        -- EMOTIONAL ATTRIBUTES (10 items, scale: 1-5)
        -- ============================================================
        
        tdl_emot_land_of_dreams,
        tdl_emot_removed_from_reality,
        tdl_emot_fantastical,
        tdl_emot_heartwarming,
        tdl_emot_soothing_healing,
        tdl_emot_feeling_safe,
        tdl_emot_longing_aspiring,
        tdl_emot_sparkling,
        tdl_emot_premium_feeling,
        tdl_emot_feel_good,
        
        -- ============================================================
        -- COMPOSITE SCORES (averages of related items)
        -- ============================================================
        
        -- Experience Quality Score (4 items)
        (coalesce(tdl_func_relaxing, 0) + coalesce(tdl_func_enjoy_myself, 0) + 
         coalesce(tdl_func_lifelong_memories, 0) + coalesce(tdl_func_bond_family_friends, 0)) / 
        nullif((case when tdl_func_relaxing is not null then 1 else 0 end +
                case when tdl_func_enjoy_myself is not null then 1 else 0 end +
                case when tdl_func_lifelong_memories is not null then 1 else 0 end +
                case when tdl_func_bond_family_friends is not null then 1 else 0 end), 0) 
        as experience_quality_score,
        
        -- Family Suitability Score (6 items)
        (coalesce(tdl_func_great_for_kids_under_6, 0) + coalesce(tdl_func_great_for_kids_7_17, 0) + 
         coalesce(tdl_func_great_for_adults, 0) + coalesce(tdl_func_want_children_experience, 0) +
         coalesce(tdl_func_expand_child_worldview, 0) + coalesce(tdl_func_great_for_all_family, 0)) / 
        nullif((case when tdl_func_great_for_kids_under_6 is not null then 1 else 0 end +
                case when tdl_func_great_for_kids_7_17 is not null then 1 else 0 end +
                case when tdl_func_great_for_adults is not null then 1 else 0 end +
                case when tdl_func_want_children_experience is not null then 1 else 0 end +
                case when tdl_func_expand_child_worldview is not null then 1 else 0 end +
                case when tdl_func_great_for_all_family is not null then 1 else 0 end), 0) 
        as family_suitability_score,
        
        -- Innovation Score (4 items)
        (coalesce(tdl_func_keeping_up_with_times, 0) + coalesce(tdl_func_new_innovative, 0) + 
         coalesce(tdl_func_something_new, 0) + coalesce(tdl_func_unique_experiences, 0)) / 
        nullif((case when tdl_func_keeping_up_with_times is not null then 1 else 0 end +
                case when tdl_func_new_innovative is not null then 1 else 0 end +
                case when tdl_func_something_new is not null then 1 else 0 end +
                case when tdl_func_unique_experiences is not null then 1 else 0 end), 0) 
        as innovation_score,
        
        -- Excitement Score (3 items)
        (coalesce(tdl_func_active_adventurous, 0) + coalesce(tdl_func_thrilling, 0) + 
         coalesce(tdl_func_repeat_experience, 0)) / 
        nullif((case when tdl_func_active_adventurous is not null then 1 else 0 end +
                case when tdl_func_thrilling is not null then 1 else 0 end +
                case when tdl_func_repeat_experience is not null then 1 else 0 end), 0) 
        as excitement_score,
        
        -- Value Score (3 items)
        (coalesce(tdl_func_worth_price, 0) + coalesce(tdl_func_affordable, 0) + 
         coalesce(tdl_func_ticket_options, 0)) / 
        nullif((case when tdl_func_worth_price is not null then 1 else 0 end +
                case when tdl_func_affordable is not null then 1 else 0 end +
                case when tdl_func_ticket_options is not null then 1 else 0 end), 0) 
        as value_perception_score,
        
        -- Emotional Score (10 items)
        (coalesce(tdl_emot_land_of_dreams, 0) + coalesce(tdl_emot_removed_from_reality, 0) + 
         coalesce(tdl_emot_fantastical, 0) + coalesce(tdl_emot_heartwarming, 0) +
         coalesce(tdl_emot_soothing_healing, 0) + coalesce(tdl_emot_feeling_safe, 0) +
         coalesce(tdl_emot_longing_aspiring, 0) + coalesce(tdl_emot_sparkling, 0) +
         coalesce(tdl_emot_premium_feeling, 0) + coalesce(tdl_emot_feel_good, 0)) / 
        nullif((case when tdl_emot_land_of_dreams is not null then 1 else 0 end +
                case when tdl_emot_removed_from_reality is not null then 1 else 0 end +
                case when tdl_emot_fantastical is not null then 1 else 0 end +
                case when tdl_emot_heartwarming is not null then 1 else 0 end +
                case when tdl_emot_soothing_healing is not null then 1 else 0 end +
                case when tdl_emot_feeling_safe is not null then 1 else 0 end +
                case when tdl_emot_longing_aspiring is not null then 1 else 0 end +
                case when tdl_emot_sparkling is not null then 1 else 0 end +
                case when tdl_emot_premium_feeling is not null then 1 else 0 end +
                case when tdl_emot_feel_good is not null then 1 else 0 end), 0) 
        as emotional_score
        
    from survey
)

select * from attribute_scores
