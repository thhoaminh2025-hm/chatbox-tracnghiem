import streamlit as st
import pandas as pd

# ================================
# 1. ĐỌC FILE CSV TRONG THƯ MỤC
# ================================
@st.cache_data
def load_questions():
    try:
        df = pd.read_csv("questions.csv", encoding="utf-8")
    except:
        df = pd.read_csv("questions.csv", encoding="latin-1")
    return df

df = load_questions()

# ================================
# 2. GIAO DIỆN APP
# ================================
st.set_page_config(page_title="Chatbox Tìm Câu Hỏi Trắc Nghiệm", layout="centered")

st.markdown(
    "<h1 style='text-align: center;'>🔍 Chatbox Tìm Câu Hỏi Trắc Nghiệm</h1>",
    unsafe_allow_html=True
)

# Tạo session_state lưu từ khóa
if "keyword" not in st.session_state:
    st.session_state.keyword = ""

# Input có ràng buộc session_state
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
        for index, row in results.iterrows():
            st.markdown("---")
            st.markdown("### ❓ Câu hỏi:")
            st.write(f"**{row['question']}**")

            st.markdown("### ✅ Đáp án đúng:")
            st.markdown(
                f"<div style='font-size: 20px; color: green; font-weight: bold;'>"
                f"{row['correct_answer']}</div>",
                unsafe_allow_html=True
            )

    # 🔥 Sau khi hiển thị kết quả → Xóa ô nhập
    st.session_state.keyword = ""



