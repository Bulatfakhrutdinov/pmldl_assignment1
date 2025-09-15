import os
import requests
import streamlit as st


API_URL = os.getenv('API_URL', 'http://api:8000/predict')


st.title('Admission Predict')


gre = st.number_input('Enter GRE Score:', value=300)

toefl = st.number_input('Enter TOEFL Score:', value=90)

uni_rating = st.number_input(
    'Enter University Rating:',
    min_value=1,
    max_value=5,
    value=1,
    step=1
)

sop = st.number_input(
    'Enter SOP:',
    min_value=1.0,
    max_value=5.0,
    step=0.5,
    value=1.0
)

log = st.number_input(
    'Enter LOR:',
    min_value=1.0,
    max_value=5.0,
    step=0.5,
    value=1.0
)

cgpa = st.number_input('Enter CGPA:', value=7.0)

research = st.number_input(
    'Enter Research:',
    min_value=0,
    max_value=1,
    step=1,
    value=0
)

if st.button('Predict'):
    data = {
        "gre": gre,
        "toefl": toefl,
        "uni_rating": uni_rating,
        "sop": sop,
        "log": log,
        "cgpa": cgpa,
        "research": research
    }

    try:
        response = requests.post(
            API_URL,
            json=data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"]
            st.success(f"Predicted Admission Chance: {prediction:.2%}")
        else:
            st.error(f"Ошибка API: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Не удалось подключиться к API. Убедитесь, что FastAPI сервер запущен на localhost:8000")
    except Exception as e:
        st.error(f"Произошла ошибка: {str(e)}")