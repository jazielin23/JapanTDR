{{
    config(
        materialized='table'
    )
}}

/*
    TDL Brand Funnel Metrics
    
    This fact table captures the marketing funnel for Tokyo Disneyland:
    Awareness → Familiarity → Opinion → Consideration → Likelihood → Intent
    
    All metrics oriented so HIGHER = BETTER:
    - Likert scales: 5 = positive, 1 = negative
    - Binary: 1 = yes, 0 = no
*/

with survey as (
    select * from {{ ref('stg_survey_responses') }}
),

funnel_metrics as (
    select
        respondent_id,
        segment_name,
        age_group,
        gender,
        geography,
        
        -- Funnel Stage 1: Awareness (binary, 1=aware)
        aided_awareness_tdl,
        
        -- Funnel Stage 2: Familiarity (1-5, 5=very familiar)
        familiarity_tdl,
        case 
            when familiarity_tdl >= 4 then 'High'
            when familiarity_tdl = 3 then 'Medium'
            when familiarity_tdl <= 2 then 'Low'
            else 'Unknown'
        end as familiarity_tdl_tier,
        
        -- Funnel Stage 3: Opinion/Favorability (1-5, 5=excellent)
        opinion_tdl,
        case 
            when opinion_tdl >= 4 then 'Positive'
            when opinion_tdl = 3 then 'Neutral'
            when opinion_tdl <= 2 then 'Negative'
            else 'Unknown'
        end as opinion_tdl_tier,
        
        -- Funnel Stage 4: Consideration (1-5, 5=definitely consider)
        consideration_tdl,
        case 
            when consideration_tdl >= 4 then 'Strong'
            when consideration_tdl = 3 then 'Maybe'
            when consideration_tdl <= 2 then 'Weak'
            else 'Unknown'
        end as consideration_tdl_tier,
        
        -- Funnel Stage 5: Likelihood (1-5, 5=definitely likely)
        likelihood_visit_tdl,
        case 
            when likelihood_visit_tdl >= 4 then 'Likely'
            when likelihood_visit_tdl = 3 then 'Uncertain'
            when likelihood_visit_tdl <= 2 then 'Unlikely'
            else 'Unknown'
        end as likelihood_tdl_tier,
        
        -- Funnel Stage 6: Intent (binary, 1=plans to visit)
        intent_visit_tdl_12mo,
        
        -- NPS (0-10)
        nps_tdl,
        case
            when nps_tdl >= 9 then 'Promoter'
            when nps_tdl >= 7 then 'Passive'
            when nps_tdl >= 0 then 'Detractor'
            else 'Unknown'
        end as nps_tdl_category,
        
        -- Behavior context
        been_to_tdl_past_3yr,
        visit_count_tdl_estimated,
        has_disney_fandom,
        
        -- Competitor comparison
        familiarity_tds,
        familiarity_usj,
        opinion_tds,
        opinion_usj,
        consideration_tds,
        consideration_usj,
        likelihood_visit_tds,
        likelihood_visit_usj,
        
        -- Derived: TDL vs USJ preference
        (familiarity_tdl - familiarity_usj) as familiarity_tdl_vs_usj,
        (opinion_tdl - opinion_usj) as opinion_tdl_vs_usj,
        (consideration_tdl - consideration_usj) as consideration_tdl_vs_usj,
        (likelihood_visit_tdl - likelihood_visit_usj) as likelihood_tdl_vs_usj

    from survey
    where aided_awareness_tdl is not null
)

select * from funnel_metrics
