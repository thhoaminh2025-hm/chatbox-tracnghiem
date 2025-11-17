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

keyword = st.text_input("Nhập từ khóa để tìm câu hỏi:", key="keyword")


# ================================
# 3. TÌM KIẾM THEO TỪ KHÓA
# ================================
if keyword.strip() != "":
    keyword_lower = keyword.lower()

    results = df[df["question"].str.lower().str.contains(keyword_lower)]

    if len(results) == 0:
        st.warning("❌ Không tìm thấy câu hỏi nào phù hợp.")
    else:
        for _, row in results.iterrows():
            st.markdown("---")
            st.markdown("### ❓ Câu hỏi:")
            st.write(f"**{row['question']}**")

            st.markdown("### ✅ Đáp án đúng:")
            st.markdown(
                f"<div style='font-size:20px;color:green;font-weight:bold;'>"
                f"{row['correct_answer']}</div>",
                unsafe_allow_html=True
            )

    # ⭐ Sau khi xuất kết quả → reset ô nhập
    st.session_state.keyword = ""
else:
    st.info("👆 Nhập từ khóa để bắt đầu tìm câu hỏi…")
