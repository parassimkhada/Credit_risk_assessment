

       Project Documentation: Loan Risk Assessment – Commercial Bank

 
1. Dataset Description

• Source: loan risk assessment_dataset.csv
• Size: 32,581 rows × 12 columns
• Objective: Identify potential loan defaulters based on customer and loan characteristics.


2. Features Overview
Feature Name: person_age,person_income,person_home_ownership i.e. RENT, OWN, MORTGAGE,person_emp_length(in years), loan_intent(EDUCATION, PERSONAL, etc.),loan_int_rate,loan_status	Default status (1 = default, 0 = paid),loan_percent_income,cb_person_default_on_file,cb_person_cred_hist_length	


3. Data Cleaning & Transformation

(i) Cleaning Steps:
•	Missing Values
o	person_emp_length → filled with 0
o	loan_int_rate → filled with 0
•	Data Types Checked: Ensured numerical/categorical


Types are correct.
•	Outlier Detection:
o	IQR method applied on all numeric fields.
o	Specifically filtered out outliers from person_income


(ii) Feature Engineering

• Converted categorical columns using One-Hot Encoding for modeling and label encoding model  i.e loan intent, home_ownership, loan_percent_income.


4. Exploratory Data Analysis (EDA)

Key Insights:

•	Most common loan intents: PERSONAL, EDUCATION, MEDICAL
•	Most risky group: Low income + high loan % of income
•	Loan grade distribution: Concentrated around grades A B, C, D, E ,F,G

•	Default Rate of loan                 : ~21.80%
.   Highest No defaulted case on MORTGAGE:  85.18%
.   Standard card eligible applicant     :  53.13%
.   Platinum card eligible applicant     :  4.21%




Visualizations:
•	Histograms of person_income, loan_amnt
•	Boxplots to observe income and employment patterns
•	Correlation heatmap showing relationships between variables


5. Model Development

Steps:
1.	Train-Test Split: Dataset split into training (80%) and testing (20%)
•	Preprocessing:
o	Scaled numerical features using StandardScaler
o	Encoded categorical features


2.	Algorithms Considered:
o	Logistic Regression
o	Random Forest
o	Gradient Boosting


3. Evaluation Metrics:
o	Accuracy
o	Precision, Recall
o	Confusion Matrix


6. Model Evaluation:
Logistic Regression Accuracy: 0.8508
Random Forest Accuracy: 0.9324
SVC: 0.9081
Gradient Boosting: 0.9218

Best Model: Random Forest with Accuracy = 0.9324


7. Deployment Plan

•  Save model with pickle.
•  Streamlit app to expose prediction service

## Inputs:
Users provide the following information through a web form:

Person's Age             : Age in years (18-100).
Annual Income (NPR)      : The person's yearly income.
Employment Length (years): The length of employment.
Loan Grade               : A letter grade from A to G.
Loan Amount (NPR)        : The amount of the loan.
Loan Interest Rate (%)   : The interest rate of the loan.
Loan % of Income         : The percentage of the person's income that the loan represents.
Credit History Length (years): The length of the credit history.
Home Ownership         : "OTHER," "OWN," or "RENT."
Loan Intent            : "EDUCATION," "HOMEIMPROVEMENT," "MEDICAL," "PERSONAL," or "VENTURE."
Default on File?       : "N" (No) or "Y" (Yes).


## Output:

# Loan Status:

(a) Eligible: If the prediction is "Paid" (0), it shows a success message with the risk probability.

High Risk: If the prediction is "Not Paid" (1), it shows an error message with the risk probability.

(b) Card Eligibility:

Platinum Card: The user is eligible if they are predicted to be "Paid," have "N" for default, an income of at least 133,000 NPR, and a loan percentage of income under 40%.

Standard Card: The user is eligible if they are predicted to be "Paid," have "N" for default, an income of at least 40,000 NPR, and a loan percentage of income under 40%.

Not Eligible: If the user doesn't meet the criteria for a Standard or Platinum card, or if their loan is predicted as "Not Paid," or they have a default on file.