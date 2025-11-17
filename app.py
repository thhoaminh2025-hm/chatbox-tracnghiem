# ===============================
# 🌿 GIAO DIỆN MÀU XANH
# ===============================
st.markdown("""
<style>

body {
    background-color: #e8f1ff !important;
}

/* Tiêu đề */
h1 {
    color: #0057b8 !important;
    font-weight: 900 !important;
    font-size: 38px !important;
    text-shadow: 1px 1px 2px #d0d7e0;
}

/* Label */
label, .stTextInput label {
    color: #003b73 !important;
    font-weight: 600;
}

/* Khung input */
.stTextInput>div>div>input {
    border-radius: 10px !important;
    padding: 12px !important;
    border: 2px solid #a9c6ff !important;
    background-color: #ffffff !important;
}

/* Nút */
.stButton>button {
    background-color: #0057b8 !important;
    color: white !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    border: none !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    transition: 0.2s;
}
.stButton>button:hover {
    background-color: #003b73 !important;
    transform: scale(1.03);
}

/* Khung câu hỏi */
.question-box {
    background: #ffffff;
    border-left: 6px solid #0057b8;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* Khung đáp án */
.answer-box {
    background: #dbffeb;
    border-left: 6px solid #1e9e4a;
    padding: 15px;
    border-radius: 12px;
    margin-top: 12px;
    font-size: 18px;
    font-weight: 600;
    color: #0a5a20;
}

</style>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbox Trắc Nghiệm", page_icon="📘", layout="centered")

st.title("📘 Chatbox Tìm Câu Hỏi Trắc Nghiệm")

# ----------------------------
# Upload file CSV
# ----------------------------
uploaded_file = st.file_uploader(
    "Tải lên file questions.csv (các cột: id, question, correct_answer)",
    type=["csv"]
)

# ----------------------------
# Helper callback khi bấm nút Tìm
# - lưu giá trị hiện tại của ô nhập vào last_query
# - bật flag search_now để main loop thực hiện tìm trên rerun
# ----------------------------
def on_search_click():
    # đọc giá trị hiện tại của ô text (session_state['query']) và lưu sang last_query
    st.session_state.last_query = st.session_state.get("query", "")
    st.session_state.search_now = True
    # clear the visible input right away (optional UX) — still safe because it's in callback
    st.session_state.query = ""

# Khởi tạo các key trong session_state nếu chưa có
if "query" not in st.session_state:
    st.session_state.query = ""
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "search_now" not in st.session_state:
    st.session_state.search_now = False

df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Không thể đọc CSV: {e}")
        df = None

# Nếu chưa upload, show hint
if df is None:
    st.info("📂 Vui lòng tải lên file CSV (questions.csv) có 3 cột: id, question, correct_answer")
else:
    # kiểm tra cột cần thiết
    required_cols = {"id", "question", "correct_answer"}
    if not required_cols.issubset(df.columns):
        st.error("❌ File CSV phải có 3 cột: id, question, correct_answer.")
        st.stop()

    # ----------------------------
    # Input tìm kiếm (liên kết với session_state 'query')
    # ----------------------------
    query = st.text_input("🔍 Nhập từ khóa để tìm câu hỏi:", key="query", value=st.session_state.get("query", ""))

    # Nút tìm có on_click callback để lưu giá trị và bật flag
    st.button("Tìm câu hỏi", on_click=on_search_click)

    # ----------------------------
    # Nếu callback đã bật flag, thực hiện tìm dựa trên last_query (không dùng query vì đã bị clear)
    # ----------------------------
    if st.session_state.get("search_now", False):
        q = st.session_state.get("last_query", "").strip()
        # Tắt flag ngay (để tránh lặp lại) — an toàn vì thay đổi do callback đã hoàn thành trước rerun
        st.session_state.search_now = False

        if q == "":
            st.warning("⚠ Vui lòng nhập từ khóa.")
        else:
            # tìm không phân biệt hoa/thường
            mask = df["question"].astype(str).str.contains(q, case=False, na=False)
            results = df[mask]

            if results.empty:
                st.warning("⚠ Không tìm thấy câu hỏi phù hợp.")
            else:
                for _, row in results.iterrows():
                    st.markdown("---")
                    st.markdown("### ❓ Câu hỏi:")
                    st.write(row["question"])

                    # Tô xanh đáp án đúng
                    st.markdown(
                        f"<div style='background-color:#d4edda; padding:10px; "
                        f"border-left:6px solid #28a745; border-radius:5px; font-size:18px;'>"
                        f"✔ <b>Đáp án đúng:</b> {row['correct_answer']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                st.markdown("---")

        # Clear last_query (đã dùng)
        st.session_state.last_query = ""
        # (query was already cleared in callback so input box is empty for next search)

