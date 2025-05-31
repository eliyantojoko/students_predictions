import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
import urllib.request
import io

# Load model yang sudah dilatih (ganti path sesuai file model kamu)
# model = joblib.load('./model/random_forest.joblib')
# model = joblib.load('https://raw.githubusercontent.com/eliyantojoko/students_predictions/main/random_forest.joblib')


url = "https://raw.githubusercontent.com/eliyantojoko/students_predictions/main/random_forest.joblib"

# Unduh dan buka sebagai file-like object
response = urllib.request.urlopen(url)
model_file = io.BytesIO(response.read())

# Load model
model = joblib.load(model_file)
# LabelEncoder dengan classes_ sesuai label asli
le = LabelEncoder()
le.classes_ = np.array(['Dropout', 'Graduate'])

# Mapping kategori (sama seperti sebelumnya, saya singkat di sini untuk fokus layout)
marital_status_map = {1: 'Single', 2: 'Married', 3: 'Widower', 4: 'Divorced',
                      5: 'Facto union', 6: 'Legally separated'}
application_mode_map = {1: '1st phase - general contingent', 2: 'Ordinance No. 612/93', 5: '1st phase - special contingent (Azores Island)', 
                        7: 'Holders of other higher courses', 10: 'Ordinance No. 854-B/99', 15: 'International student (bachelor)',
                        16: '1st phase - special contingent (Madeira Island)', 17: '2nd phase - general contingent', 18: '3rd phase - general contingent',
                        26: 'Ordinance No. 533-A/99, item b2) (Different Plan)', 27: 'Ordinance No. 533-A/99, item b3 (Other Institution)', 
                        39: 'Over 23 years old', 42: 'Transfer', 43: 'Change of course', 44: 'Technological specialization diploma holders',
                        51: 'Change of institution/course', 53: 'Short cycle diploma holders', 57: 'Change of institution/course (International)'}
course_map = {33: 'Biofuel Production Technologies', 171: 'Animation and Multimedia Design', 8014: 'Social Service (evening attendance)', 9003: 'Agronomy',
              9070: 'Communication Design', 9085: 'Veterinary Nursing', 9119: 'Informatics Engineering', 9130: 'Equinculture', 9147: 'Management',
              9238: 'Social Service', 9254: 'Tourism', 9500: 'Nursing', 9556: 'Oral Hygiene', 9670: 'Advertising and Marketing Management',
              9773: 'Journalism and Communication', 9853: 'Basic Education', 9991: 'Management (evening attendance)'}
daytime_evening_map = {1: 'Daytime', 0: 'Evening'}
previous_qualification_map = {1: "Secondary education", 2: "Higher education - bachelor's degree", 3: "Higher education - degree",
                              4: "Higher education - master's", 5: "Higher education - doctorate", 6: "Frequency of higher education",
                              9: "12th year of schooling - not completed", 10: "11th year of schooling - not completed",
                              12: "Other - 11th year of schooling", 14: "10th year of schooling", 15: "10th year of schooling - not completed",
                              19: "Basic education 3rd cycle (9th/10th/11th year) or equiv.", 38: "Basic education 2nd cycle (6th/7th/8th year) or equiv.",
                              39: "Technological specialization course", 40: "Higher education - degree (1st cycle)",
                              42: "Professional higher technical course", 43: "Higher education - master (2nd cycle)"}
nationality_map = {1: 'Portuguese', 2: 'German', 6: 'Spanish', 11: 'Italian', 13: 'Dutch', 14: 'English', 17: 'Lithuanian', 21: 'Angolan',
                   22: 'Cape Verdean', 24: 'Guinean', 25: 'Mozambican', 26: 'Santomean', 32: 'Turkish', 41: 'Brazilian', 62: 'Romanian',
                   100: 'Moldova (Republic of)', 101: 'Mexican', 103: 'Ukrainian', 105: 'Russian', 108: 'Cuban', 109: 'Colombian'}
mothers_qualification_map = {1: "Secondary Education - 12th Year of Schooling or Eq.", 2: "Higher Education - Bachelor's Degree",
                             3: "Higher Education - Degree", 4: "Higher Education - Master's", 5: "Higher Education - Doctorate",
                             6: "Frequency of Higher Education", 9: "12th Year of Schooling - Not Completed",
                             10: "11th Year of Schooling - Not Completed", 11: "7th Year (Old)", 12: "Other - 11th Year of Schooling",
                             14: "10th Year of Schooling", 18: "General commerce course", 19: "Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.",
                             22: "Technical-professional course", 26: "7th year of schooling", 27: "2nd cycle of the general high school course",
                             29: "9th Year of Schooling - Not Completed", 30: "8th year of schooling", 34: "Unknown", 35: "Can't read or write",
                             36: "Can read without having a 4th year of schooling", 37: "Basic education 1st cycle (4th/5th year) or equiv.",
                             38: "Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.", 39: "Technological specialization course",
                             40: "Higher education - degree (1st cycle)", 41: "Specialized higher studies course",
                             42: "Professional higher technical course", 43: "Higher Education - Master (2nd cycle)", 44: "Higher Education - Doctorate (3rd cycle)"}
mothers_occupation_map = {0: "Student", 1: "Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers",
                         2: "Specialists in Intellectual and Scientific Activities", 3: "Intermediate level technicians and professions",
                         4: "Administrative staff", 5: "Personal services, security and safety workers and sellers",
                         6: "Farmers and skilled workers in agriculture, fisheries and forestry", 7: "Skilled workers in industry, construction and craftsmen",
                         8: "Installation and machine operators and assembly workers", 9: "Unskilled workers",
                         10: "Armed Forces Professions", 90: "Other Situation", 99: "Unknown"}
fathers_qualification_map = mothers_qualification_map.copy()
fathers_occupation_map = mothers_occupation_map.copy()
gender_map = {1: 'Male', 0: 'Female'}
yes_no_map = {1: 'Yes', 0: 'No'}


def main():
    st.set_page_config(page_title="Student Status Prediction", layout="wide")
    st.title("Student Status Prediction")
    st.text("Web-app dor generating prediction of student status: Dropout or Graduate")
    st.text("By: Joko Eliyanto")

    with st.form("input_form"):
        

        # Kolom 1
        # Baris baru untuk units dan economic indicators agar tidak terlalu padat
        st.markdown("---")
        st.header("Demography Indicators")
        cols = st.columns(3)
        with cols[0]:
            gender              = st.selectbox( "Gender", 
                                                options=list(gender_map.keys()),
                                                format_func=lambda x: gender_map[x], index=0)

            age_at_enrollment   = st.number_input(  "Age at Enrollment", 
                                                    min_value=15, 
                                                    max_value=70, 
                                                    value=20)

            marital_status      = st.selectbox( "Marital Status", 
                                                options=list(marital_status_map.keys()),
                                                format_func=lambda x: marital_status_map[x], index=0)

            nationality         = st.selectbox( "Nationality", 
                                                options=list(nationality_map.keys()),
                                                format_func=lambda x: nationality_map[x], index=0)
            
        # Kolom 2
        with cols[1]:
            displaced           = st.selectbox( "Displaced", 
                                                options=list(yes_no_map.keys()),
                                                format_func=lambda x: yes_no_map[x], 
                                                index=1)

            educational_special_needs = st.selectbox( "Educational Special Needs", 
                                                      options=list(yes_no_map.keys()),
                                                      format_func=lambda x: yes_no_map[x], 
                                                      index=1)

            scholarship_holder  = st.selectbox( "Scholarship Holder", 
                                                options=list(yes_no_map.keys()),
                                                format_func=lambda x: yes_no_map[x], 
                                                index=1)
            
            international       = st.selectbox( "International", 
                                                options=list(yes_no_map.keys()),
                                                format_func=lambda x: yes_no_map[x], 
                                                index=0)
            
    
        # Kolom 3
        with cols[2]:
            mothers_qualification = st.selectbox( "Mother's Qualification", 
                                                  options=list(mothers_qualification_map.keys()),
                                                  format_func=lambda x: mothers_qualification_map[x], 
                                                  index=0)

            fathers_qualification = st.selectbox( "Father's Qualification", 
                                                  options=list(fathers_qualification_map.keys()),
                                                  format_func=lambda x: fathers_qualification_map[x], 
                                                  index=0)

            mothers_occupation    = st.selectbox("Mother's Occupation", 
                                                 options=list(mothers_occupation_map.keys()),
                                                 format_func=lambda x: mothers_occupation_map[x], 
                                                 index=0)

            fathers_occupation    = st.selectbox("Father's Occupation", 
                                                 options=list(fathers_occupation_map.keys()),
                                                 format_func=lambda x: fathers_occupation_map[x], 
                                                 index=0)

            
        # Baris baru untuk units dan economic indicators agar tidak terlalu padat
        st.markdown("---")
        st.header("Academic Performance and Economic Indicators")
        cols2 = st.columns(4)

        # Curricular units 1st semester
        with cols2[0]:
            course                  = st.selectbox( "Course", 
                                                    options=list(course_map.keys()),
                                                    format_func=lambda x: course_map[x], 
                                                    index=0)

            daytime_evening_attendance = st.selectbox("Daytime / Evening Attendance", 
                                                      options=list(daytime_evening_map.keys()),
                                                      format_func=lambda x: daytime_evening_map[x], 
                                                      index=0)

            admission_grade         = st.number_input("Admission Grade", 
                                                       min_value=0.0, 
                                                       max_value=20.0, 
                                                       value=12.0, 
                                                       step=0.1)
            
        with cols2[1]:
            curricular_units_1st_sem_credited = st.number_input("1st Sem Credited", min_value=0, max_value=60, value=15)
            curricular_units_1st_sem_enrolled = st.number_input("1st Sem Enrolled", min_value=0, max_value=60, value=20)
            curricular_units_1st_sem_evaluations = st.number_input("1st Sem Evaluations", min_value=0, max_value=60, value=18)
            curricular_units_1st_sem_approved = st.number_input("1st Sem Approved", min_value=0, max_value=60, value=16)
            curricular_units_1st_sem_grade = st.number_input("1st Sem Grade", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
            curricular_units_1st_sem_without_evaluations = st.number_input("1st Sem Without Eval", min_value=0, max_value=60, value=2)
        # Curricular units 2nd semester
        with cols2[2]:
            curricular_units_2nd_sem_credited = st.number_input("2nd Sem Credited", min_value=0, max_value=60, value=15)
            curricular_units_2nd_sem_enrolled = st.number_input("2nd Sem Enrolled", min_value=0, max_value=60, value=20)
            curricular_units_2nd_sem_evaluations = st.number_input("2nd Sem Evaluations", min_value=0, max_value=60, value=18)
            curricular_units_2nd_sem_approved = st.number_input("2nd Sem Approved", min_value=0, max_value=60, value=16)
            curricular_units_2nd_sem_grade = st.number_input("2nd Sem Grade", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
            curricular_units_2nd_sem_without_evaluations = st.number_input("2nd Sem Without Eval", min_value=0, max_value=60, value=2)
        with cols2[3]:
            application_mode = st.selectbox("Application Mode", options=list(application_mode_map.keys()),
                                            format_func=lambda x: application_mode_map[x], index=0)
            application_order = st.number_input("Application Order", min_value=1, max_value=100, value=1)
            previous_qualification = st.selectbox("Previous Qualification", options=list(previous_qualification_map.keys()),
                                                 format_func=lambda x: previous_qualification_map[x], index=0)
            previous_qualification_grade = st.number_input("Previous Qualification Grade", min_value=0.0, max_value=20.0,
                                                          value=12.0, step=0.1)

        # Baris baru untuk units dan economic indicators agar tidak terlalu padat
        st.markdown("---")
        st.header("Academic Performance and Economic Indicators")
        # Economic indicators
        tuition_fees_up_to_date = st.selectbox("Tuition Fees Up To Date", options=list(yes_no_map.keys()),
                                                   format_func=lambda x: yes_no_map[x], index=0)
        debtor = st.selectbox("Debtor", options=list(yes_no_map.keys()),
                                  format_func=lambda x: yes_no_map[x], index=1)
        unemployment_rate = st.number_input("Unemployment Rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        inflation_rate = st.number_input("Inflation Rate (%)", min_value=-10.0, max_value=100.0, value=2.0, step=0.1)
        gdp = st.number_input("GDP (billion €)", min_value=0.0, value=200.0, step=0.1)

        submitted = st.form_submit_button("Predict")

    if submitted:
        # Buat DataFrame input sesuai fitur model
        input_data = pd.DataFrame({
            "Marital_status": [marital_status],
            "Application_mode": [application_mode],
            "Application_order": [application_order],
            "Course": [course],
            "Daytime_evening_attendance": [daytime_evening_attendance],
            "Previous_qualification": [previous_qualification],
            "Previous_qualification_grade": [previous_qualification_grade],
            "Nationality": [nationality],
            "Mothers_qualification": [mothers_qualification],
            "Fathers_qualification": [fathers_qualification],
            "Mothers_occupation": [mothers_occupation],
            "Fathers_occupation": [fathers_occupation],
            "Admission_grade": [admission_grade],
            "Displaced": [displaced],
            "Educational_special_needs": [educational_special_needs],
            "Debtor": [debtor],
            "Tuition_fees_up_to_date": [tuition_fees_up_to_date],
            "Gender": [gender],
            "Scholarship_holder": [scholarship_holder],
            "Age_at_enrollment": [age_at_enrollment],
            "International": [international],
            "Curricular_units_1st_sem_credited": [curricular_units_1st_sem_credited],
            "Curricular_units_1st_sem_enrolled": [curricular_units_1st_sem_enrolled],
            "Curricular_units_1st_sem_evaluations": [curricular_units_1st_sem_evaluations],
            "Curricular_units_1st_sem_approved": [curricular_units_1st_sem_approved],
            "Curricular_units_1st_sem_grade": [curricular_units_1st_sem_grade],
            "Curricular_units_1st_sem_without_evaluations": [curricular_units_1st_sem_without_evaluations],
            "Curricular_units_2nd_sem_credited": [curricular_units_2nd_sem_credited],
            "Curricular_units_2nd_sem_enrolled": [curricular_units_2nd_sem_enrolled],
            "Curricular_units_2nd_sem_evaluations": [curricular_units_2nd_sem_evaluations],
            "Curricular_units_2nd_sem_approved": [curricular_units_2nd_sem_approved],
            "Curricular_units_2nd_sem_grade": [curricular_units_2nd_sem_grade],
            "Curricular_units_2nd_sem_without_evaluations": [curricular_units_2nd_sem_without_evaluations],
            "Unemployment_rate": [unemployment_rate],
            "Inflation_rate": [inflation_rate],
            "GDP": [gdp]
        })

        prediction = model.predict(input_data)[0]
        prediction_proba = model.predict_proba(input_data)[0]
        pred_label = le.inverse_transform([prediction])[0]

        st.markdown("---")
        st.subheader("Prediction Result")
        st.write(f"**Predicted Status:** {pred_label}")
        st.write(f"**Probability:** Dropout: {prediction_proba[0]:.2f}, Graduate: {prediction_proba[1]:.2f}")

        st.subheader("Input Data")
        st.dataframe(input_data.T.rename(columns={0: "Value"}))

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; font-size: 14px;'>
            &copy; 2024 <strong>Joko Eliyanto</strong>. All rights reserved.
            <br><br>
            <a href="https://wa.me/+6282183112655" target="_blank">
                <img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white">
            </a>
            <a href="https://www.linkedin.com/in/joko-eliyanto-23a1b6143/" target="_blank">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
            </a>
            <a href="https://github.com/jokoeliyanto" target="_blank">
                <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
            </a>
            <a href="mailto:jokoeliyanto@gmail.com" target="_blank">
                <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white">
            </a>
            <a href="https://medium.com/@jokoeliyanto" target="_blank">
                <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
