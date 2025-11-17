import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbox Tìm Câu Hỏi Trắc Nghiệm", layout="centered")

st.markdown(
    "<h1 style='text-align:center;'>🔍 Chatbox Tìm Câu Hỏi Trắc Nghiệm</h1>",
    unsafe_allow_html=True
)

# ================================
# HÀM ĐỌC CSV CHỐNG LỖI
# ================================
def load_csv(file):
    # thử nhiều cách đọc khác nhau
    for delimiter in [",", ";", "|", "\t"]:
        try:
            df = pd.read_csv(
                file,
                encoding="utf-8",
                sep=delimiter,
                engine="python"
            ).dropna(how="all")  # bỏ dòng trống
            if len(df.columns) >= 2:
                return df
        except:
            pass

        try:
            df = pd.read_csv(
                file,
                encoding="latin-1",
                sep=delimiter,
                engine="python"
            ).dropna(how="all")
            if len(df.columns) >= 2:
                return df
        except:
            pass

    return None


# ================================
# UPLOAD FILE CSV
# ================================
uploaded_file = st.file_uploader("📂 Tải file questions.csv lên", type=["csv"])

if uploaded_file is not None:

    df = load_csv(uploaded_file)

    if df is None:
        st.error("❌ Không thể đọc CSV. Vui lòng kiểm tra lại file (phải có cột id, question, correct_answer).")
        st.stop()

    # Kiểm tra cột
    required_cols = ["id", "question", "correct_answer"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"❌ Thiếu cột: {col}. File CSV phải đúng cấu trúc.")
            st.stop()

    # ====================================
    # INPUT TỪ KHÓA (AUTO-CLEAR)
    # ====================================
    if "keyword" not in st.session_state:
        st.session_state.keyword = ""

    keyword = st.text_input("Nhập từ khóa để tìm câu hỏi:", key="keyword")

    # ====================================
    # TÌM KIẾM
    # ====================================
    if keyword.strip() != "":
        key_lower = keyword.lower()

        results = df[df["question"].str.lower().str.contains(key_lower)]

        if len(results) == 0:
            st.warning("❌ Không tìm thấy câu hỏi nào.")
        else:
            for _, row in results.iterrows():
                st.markdown("---")
                st.markdown("### ❓ Câu hỏi:")
                st.write(f"**{row['question']}**")

                st.markdown("### ✅ Đáp án đúng:")
                st.markdown(
                    f"<div style='font-size:22px;color:green;font-weight:bold;'>{row['correct_answer']}</div>",
                    unsafe_allow_html=True
                )

        # ⭐ AUTO-CLEAR TỪ KHÓA SAU KHI TÌM
        st.session_state.keyword = ""

else:
    st.info("📌 Vui lòng tải file questions.csv lên để bắt đầu.")
