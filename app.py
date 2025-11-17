import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbox Tìm Câu Hỏi Trắc Nghiệm", layout="centered")

st.markdown(
    "<h1 style='text-align:center;'>🔍 Chatbox Tìm Câu Hỏi Trắc Nghiệm</h1>",
    unsafe_allow_html=True
)

# ================================
# 1. UPLOAD FILE CSV
# ================================
uploaded_file = st.file_uploader("📂 Tải file questions.csv lên", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
    except:
        df = pd.read_csv(uploaded_file, encoding="latin-1")

    # ================================
    # 2. INPUT TỪ KHÓA (CÓ AUTO-CLEAR)
    # ================================
    if "keyword" not in st.session_state:
        st.session_state.keyword = ""

    keyword = st.text_input("Nhập từ khóa để tìm câu hỏi:", key="keyword")

    # ================================
    # 3. XỬ LÝ TÌM KIẾM
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

        # ⭐ AUTO-CLEAR sau khi hiển thị kết quả
        st.session_state.keyword = ""

else:
    st.info("📌 Vui lòng tải file questions.csv lên để bắt đầu.")
