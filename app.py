import streamlit as st
import pandas as pd
import pickle


# Load saved objects

with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("loan_grade_encoder.pkl", "rb") as f:
    loan_grade_encoder = pickle.load(f)

with open("model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)


st.title("Loan Status Prediction & Card Eligibility App")
st.write("Predicts whether a loan will be Paid (0) or Not Paid (1) and checks card eligibility.")

# Inputs
person_age = st.number_input("Age of Person", min_value=18, max_value=100, value=30)
person_income = st.number_input("Annual Income (NPR)", min_value=0, value=500000)
person_emp_length = st.number_input("Employment Length (years)", min_value=0, max_value=50, value=5)
loan_grade = st.selectbox("Loan Grade", ["A", "B", "C", "D", "E", "F", "G"])
loan_amnt = st.number_input("Loan Amount (NPR)", min_value=0, value=100000)
loan_int_rate = st.number_input("Loan Interest Rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
loan_percent_income = st.number_input("Loan % of Income", min_value=0.0, max_value=1.0, value=0.2)
cb_person_cred_hist_length = st.number_input("Credit History Length (years)", min_value=0, max_value=50, value=5)
person_home_ownership = st.selectbox("Home Ownership", ["OTHER", "OWN", "RENT"])
loan_intent = st.selectbox("Loan Intent", ["EDUCATION", "HOMEIMPROVEMENT", "MEDICAL", "PERSONAL", "VENTURE"])
cb_person_default_on_file = st.selectbox("Default on File?", ["N", "Y"])

# Create DataFrame
input_df = pd.DataFrame({
    "person_age": [person_age],
    "person_income": [person_income],
    "person_emp_length": [person_emp_length],
    "loan_grade": [loan_grade],
    "loan_amnt": [loan_amnt],
    "loan_int_rate": [loan_int_rate],
    "loan_percent_income": [loan_percent_income],
    "cb_person_cred_hist_length": [cb_person_cred_hist_length],
    "person_home_ownership": [person_home_ownership],
    "loan_intent": [loan_intent],
    "cb_person_default_on_file": [cb_person_default_on_file]})

# Prediction Logic
if st.button("Predict"):

    # Step 1: Label encode loan_grade
    input_df["loan_grade"] = loan_grade_encoder.transform(input_df["loan_grade"])

    # Step 2: One-hot encode nominal variables
    nominal_vars = ["person_home_ownership", "loan_intent", "cb_person_default_on_file"]
    input_df = pd.get_dummies(input_df, columns=nominal_vars, drop_first=True)

    st.button('Made by @paras simkhada')

# Match training columns
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_columns]

# Predict
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0][1]

# Show results
    if prediction == 0:
        st.success(f"Applicant is Eligible. Risk Probability: {prediction_proba:.2%}")
    else:
        st.error(f"High Risk. Risk Probability: {prediction_proba:.2%}")

   
# Card Eligibility

    if prediction == 0 and cb_person_default_on_file == "N":
        eligible_standard = (person_income >= 40000) and (loan_percent_income < 0.4)
        eligible_platinum = (person_income >= 133000) and (loan_percent_income < 0.4)

        if eligible_platinum:
            st.info("Eligible for Platinum Card")
        elif eligible_standard:
            st.info("Eligible for Standard Card")
        else:
            st.warning("Not eligible for Standard or Platinum card.")
    elif prediction == 1:
        st.warning("Loan not paid — Not eligible for any card.")
    else:
        st.warning("Default on file — Not eligible for any card.")
