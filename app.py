import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
file_path = "data/U.S._Chronic_Disease_Indicators.csv"
df = pd.read_csv(file_path)

# Identify all unique chronic disease topics
disease_topics = df['Topic'].unique().tolist()

# Filter to only rows with a valid DataValue and required columns
df = df[['YearStart', 'LocationDesc', 'Topic', 'DataValue']].dropna()

# Pivot so each disease is a column
pivoted = df.pivot_table(
    index=['YearStart', 'LocationDesc'],
    columns='Topic',
    values='DataValue',
    aggfunc='mean'
).reset_index()

# Fill missing values with 0 (or you could use mean)
pivoted.fillna(0, inplace=True)

# Store results
results = pivoted[['YearStart', 'LocationDesc']].copy()

# For each disease, train a model to predict high risk (using median as threshold)
interventions = {}
for disease in disease_topics:
    if disease not in pivoted.columns:
        continue
    # Define high risk as above median value for that disease
    median_val = pivoted[disease].median()
    y = (pivoted[disease] > median_val).astype(int)
    X = pivoted[disease_topics].drop(columns=[disease], errors='ignore')
    # Remove the current disease from features to avoid leakage
    X = X.drop(columns=[col for col in X.columns if col == disease], errors='ignore')
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy for {disease}: {acc:.2f}")
    # Predict for all rows
    results[f'{disease}_Risk'] = model.predict(X)
    # Simple intervention logic
    def recommend(risk):
        if risk == 1:
            return f"Intervention needed for {disease}: consult a specialist, improve lifestyle."
        else:
            return f"No immediate intervention for {disease}. Maintain healthy habits."
    results[f'{disease}_Intervention'] = results[f'{disease}_Risk'].apply(recommend)
    interventions[disease] = recommend

# Show sample predictions/interventions
print("\nSample Chronic Disease Risk Predictions (per disease):\n")
show_cols = ['YearStart', 'LocationDesc']
for disease in disease_topics:
    if f'{disease}_Risk' in results.columns:
        show_cols += [f'{disease}_Risk', f'{disease}_Intervention']
print(results[show_cols].head(10))

# --- Individual-level monitoring and intervention planning ---
from monitoring.monitor import monitor_health
from interventions.planner import suggest_interventions

# Example: process individual health data
try:
    sample_data = pd.read_csv("data/sample_health_data.csv")
    all_diseases = disease_topics  # from earlier in the script
    for _, row in sample_data.iterrows():
        risks = monitor_health(row)
        # risks['detections'] is a dict of disease: True/False
        # Wrap in DataFrame for suggest_interventions
        risk_df = pd.DataFrame([{{f'{d}_Risk': int(risks['detections'].get(d, 0)) for d in all_diseases}}])
        plan_df = suggest_interventions(risk_df, all_diseases)
        print(f"Risks: {risks['detections']} → Plan: ")
        for d in all_diseases:
            print(f"  {d}: {plan_df.iloc[0][f'{d}_Intervention']}")
except FileNotFoundError:
    print("Sample health data file not found. Skipping individual-level monitoring.")

# --- Trend Analysis: Mean DataValue per Disease by Year ---
print("\nTrend Analysis: Mean DataValue per Disease by Year")
trend = df.groupby(['YearStart', 'Topic'])['DataValue'].mean().unstack()
print(trend.tail())

# --- User input prediction with options ---
print("\nYou can provide values for any of the following indicators/diseases:")
for idx, disease in enumerate(disease_topics, 1):
    print(f"{idx}. {disease}")
print("\nEnter the numbers (comma-separated) for which you want to provide values (e.g., 1,3,5). The rest will be set to 0.")
selected = input("Your selection: ")
selected_indices = set()
try:
    selected_indices = set(int(x.strip()) for x in selected.split(",") if x.strip().isdigit())
except Exception:
    selected_indices = set()
user_input = {}
for idx, disease in enumerate(disease_topics, 1):
    if idx in selected_indices:
        val = input(f"Enter value for {disease}: ")
        try:
            user_input[disease] = float(val) if val.strip() else 0.0
        except Exception:
            user_input[disease] = 0.0
    else:
        user_input[disease] = 0.0

# Prepare input as DataFrame
user_df = pd.DataFrame([user_input])
user_df = user_df.reindex(columns=disease_topics, fill_value=0.0)

print("\nUser Input Risk Prediction and Interventions:")
for disease in disease_topics:
    if disease not in pivoted.columns:
        continue
    median_val = pivoted[disease].median()
    X_user = user_df.drop(columns=[disease], errors='ignore')
    X_user = X_user.drop(columns=[col for col in X_user.columns if col == disease], errors='ignore')
    y = (pivoted[disease] > median_val).astype(int)
    X = pivoted[disease_topics].drop(columns=[disease], errors='ignore')
    X = X.drop(columns=[col for col in X.columns if col == disease], errors='ignore')
    model = RandomForestClassifier()
    model.fit(X, y)
    risk = model.predict(X_user)[0]
    if risk == 1:
        intervention = f"Intervention needed for {disease}: consult a specialist, improve lifestyle."
    else:
        intervention = f"No immediate intervention for {disease}. Maintain healthy habits."
    print(f"{disease}: Risk={risk} → {intervention}")
