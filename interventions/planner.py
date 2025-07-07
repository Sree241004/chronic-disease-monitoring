def suggest_interventions(risk_df, all_diseases):
    """
    Given a DataFrame with *_Risk columns, suggest interventions for each disease in all_diseases.
    Args:
        risk_df: DataFrame with columns like 'Diabetes_Risk', 'Asthma_Risk', etc.
        all_diseases: List of all disease/topic names in the dataset.
    Returns:
        DataFrame with intervention columns for each disease.
    """
    interventions = {}
    for disease in all_diseases:
        risk_col = f'{disease}_Risk'
        if risk_col in risk_df.columns:
            def recommend(risk):
                if risk == 1:
                    return f"Intervention needed for {disease}: consult a specialist, improve lifestyle."
                else:
                    return f"No immediate intervention for {disease}. Maintain healthy habits."
            interventions[f'{disease}_Intervention'] = risk_df[risk_col].apply(recommend)
        else:
            interventions[f'{disease}_Intervention'] = "No data available for this disease."
    return risk_df.assign(**interventions)
