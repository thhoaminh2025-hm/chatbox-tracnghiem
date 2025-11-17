import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Chatbox Trắc Nghiệm", layout="wide")

st.title("🔎 Chatbox tìm câu hỏi trắc nghiệm")
st.markdown("Gõ **từ khóa** để tìm câu hỏi. Ứng dụng sẽ hiện câu hỏi + đáp án đúng.")

@st.cache_data
def load_data():
    return pd.read_csv("questions.csv")

df = load_data()

query = st.text_input("Nhập từ khóa để tìm câu hỏi:")

if query:
    tokens = query.lower().split()
    def match(text):
        t = str(text).lower()
        return all(tok in t for tok in tokens)

    results = df[df['question'].apply(match)]

    st.write(f"🔍 Tìm thấy **{len(results)}** câu hỏi:")

    for _, row in results.iterrows():
        st.markdown("---")
        st.markdown(f"**Câu hỏi:** {row['question']}")
        st.markdown(f"**Đáp án đúng:** 🟢 **{row['correct_answer']}**")
        if 'choices' in df.columns and not pd.isna(row['choices']):
            st.markdown(f"**Lựa chọn:** {row['choices']}")
