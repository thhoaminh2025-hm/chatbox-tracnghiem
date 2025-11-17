import streamlit as st
import pandas as pd
import requests
from io import StringIO

# ================================
# 1. TẢI CSV TRỰC TIẾP TỪ GITHUB
# ================================

CSV_URL = "https://raw.githubusercontent.com/thhoaminh2025-hm/chatbox-tracnghiem/main/questions.csv"

@st.cache_data
def load_questions_from_github(url):
    response = requests.get(url)
    response.raise_for_status()  # báo lỗi nếu URL sai

    csv_data = StringIO(response.text)

    try:
        df = pd.read_csv(csv_data, encoding="utf-8")
    except:
        df = pd.read_csv(csv_data, encoding="latin-1")

    return df

df = load_questions_from_github(CSV_URL)


# ================================
# 2. GIAO DIỆN APP
# ================================
st.set_page_config(page_title="Chatbox Tìm Câu Hỏi Trắc Nghiệm", layout="centered")

st.markdown(
    "<h1 style='text-align: center;'>🔍 Chatbox Tìm Câu Hỏi Trắc Nghiệm</h1>",
    unsafe_allow_html=True
)

# Tạo session_state để reset text_input
if "keyword" not in st.session_state:
    st.session_state.keyword = ""

keyword = st.text_input("Nhập từ khóa để tìm câ_
