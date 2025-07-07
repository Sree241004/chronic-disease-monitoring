# chronic-disease-monitoring

Early warning system using ML for chronic diseases like pre-diabetes, hypertension, and more.

## Project Overview
This project provides a machine learning-based pipeline for monitoring, analyzing, and predicting risks for a wide range of chronic diseases using public health data. It also recommends personalized interventions based on predicted risks.

## Features
- Early detection of chronic disease risks
- Trend analysis by year and location
- Risk prediction for all diseases in the dataset
- Personalized intervention recommendations
- User-friendly input for individual risk assessment

## Installation
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd chronic-disease-monitoring
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- To run the main pipeline:
  ```bash
  python app.py
  ```
- You will be prompted to enter values for selected diseases/indicators for individual risk prediction.

## Input Format
- The main dataset should be a CSV file like `data/U.S._Chronic_Disease_Indicators.csv` with columns including:
  - `YearStart`, `LocationDesc`, `Topic`, `DataValue`, etc.
- For individual-level predictions, you can use a CSV like `data/sample_health_data.csv` or enter values interactively.

## Output
- Model accuracy for each disease
- Sample risk predictions and intervention recommendations
- Trend analysis table by year and disease
- Personalized risk and intervention output for user input

## Architecture
1. **Health Monitoring:** Detects early indicators from individual or population data
2. **Trend Analysis:** Analyzes disease trends over time and location
3. **Risk Prediction:** Predicts high-risk cases using ML models
4. **Intervention Planning:** Recommends actions based on predicted risks

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
For questions or support, please contact Boga Sudharshini Sree at sudharshinisree.boga@gmail.com.
