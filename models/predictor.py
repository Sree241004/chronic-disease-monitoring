import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def predict_diseases(df, topics=None):
    """
    Trains and predicts high risk for each disease/topic in the dataset using the best model per disease.
    Args:
        df: DataFrame with columns ['YearStart', 'LocationDesc', 'Topic', 'DataValue']
        topics: Optional list of topics to include. If None, uses all unique topics in df.
    Returns:
        results: DataFrame with predictions for each disease/topic.
        best_models: Dict of best model name and accuracy per disease/topic.
    """
    if topics is None:
        topics = df['Topic'].unique().tolist()
    # Pivot so each disease is a column
    pivoted = df.pivot_table(
        index=['YearStart', 'LocationDesc'],
        columns='Topic',
        values='DataValue',
        aggfunc='mean'
    ).reset_index()
    pivoted.fillna(0, inplace=True)
    results = pivoted[['YearStart', 'LocationDesc']].copy()
    best_models = {}
    classifiers = {
        'RandomForest': RandomForestClassifier(),
        'LogisticRegression': LogisticRegression(max_iter=1000),
        'SVC': SVC()
    }
    for disease in topics:
        if disease not in pivoted.columns:
            continue
        median_val = pivoted[disease].median()
        y = (pivoted[disease] > median_val).astype(int)
        X = pivoted[topics].drop(columns=[disease], errors='ignore')
        X = X.drop(columns=[col for col in X.columns if col == disease], errors='ignore')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        best_acc = 0
        best_model = None
        best_model_name = ''
        for name, clf in classifiers.items():
            try:
                clf.fit(X_train, y_train)
                preds = clf.predict(X_test)
                acc = accuracy_score(y_test, preds)
                if acc > best_acc:
                    best_acc = acc
                    best_model = clf
                    best_model_name = name
            except Exception:
                continue
        if best_model is not None:
            best_models[disease] = {'model': best_model_name, 'accuracy': best_acc}
            results[f'{disease}_Risk'] = best_model.predict(X)
    return results, best_models
