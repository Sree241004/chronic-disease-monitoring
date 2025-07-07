def monitor_health(data):
    results = {}
    # Placeholder thresholds for each topic (customize as needed)
    thresholds = {
        'Disability': 1,  # 1 = has disability
        'Arthritis': 1,  # 1 = has arthritis
        'Immunization': 1,  # 0 = not immunized, 1 = immunized
        'Diabetes': 125,  # glucose > 125
        'Health Status': 2,  # 0=good, 1=fair, 2=poor
        'Alcohol': 14,  # drinks/week > 14
        'Asthma': 1,  # 1 = has asthma
        'Sleep': 6,  # hours < 6
        'Oral Health': 1,  # 1 = poor oral health
        'Mental Health': 1,  # 1 = poor mental health
        'Cardiovascular Disease': 1,  # 1 = has CVD
        'Cancer': 1,  # 1 = has cancer
        'Tobacco': 1,  # 1 = uses tobacco
        'Nutrition, Physical Activity, and Weight Status': 1,  # 1 = poor
        'Chronic Obstructive Pulmonary Disease': 1,  # 1 = has COPD
        'Social Determinants of Health': 1,  # 1 = at risk
        'Cognitive Health and Caregiving': 1,  # 1 = impaired
        'Maternal Health': 1,  # 1 = at risk
        'Chronic Kidney Disease': 1  # 1 = has CKD
    }
    # Detection logic (customize per topic as needed)
    for topic, threshold in thresholds.items():
        val = data.get(topic, 0)
        if topic == 'Sleep':
            results[topic] = val < threshold
        elif topic == 'Immunization':
            results[topic] = val == 0  # not immunized
        elif topic == 'Health Status':
            results[topic] = val >= threshold  # poor health
        elif topic == 'Alcohol':
            results[topic] = val > threshold
        elif topic == 'Diabetes':
            results[topic] = val > threshold
        else:
            results[topic] = val == threshold or val > threshold
    # Add simple intervention recommendations
    interventions = {}
    for key, flag in results.items():
        if flag:
            interventions[key] = f"Intervention needed for {key.replace('_', ' ')}: consult a specialist, improve lifestyle."
        else:
            interventions[key] = f"No immediate intervention for {key.replace('_', ' ')}. Maintain healthy habits."
    return {"detections": results, "interventions": interventions}
