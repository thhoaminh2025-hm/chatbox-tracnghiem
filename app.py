import streamlit as st
import pandas as pd

st.title("📘 Chatbox Tìm Câu Hỏi Trắc Nghiệm")

@st.cache_data
def load_questions():
    try:
        df = pd.read_csv("questions.csv", encoding="utf-8")
        return df
    except Exception as e:
        st.error(f"Lỗi đọc file CSV: {e}")
        return None

df = load_questions()

if df is not None:
    query = st.text_input("Nhập từ khóa tìm câu hỏi:")

    if query:
        results = df[df['question'].str.contains(query, case=False, na=False)]

        if results.empty:
            st.warning("❌ Không tìm thấy câu hỏi.")
        else:
            for _, row in results.iterrows():
                st.write(f"### ❓ Câu hỏi:\n{row['question']}")
                st.success(f"**Đáp án đúng:** {row['correct_answer']}")
