import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbox Trắc Nghiệm", page_icon="📘", layout="centered")

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


# ===============================
# KHỞI TẠO SESSION STATE
# ===============================
if "query" not in st.session_state:
    st.session_state.query = ""

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "search_now" not in st.session_state:
    st.session_state.search_now = False


# ===============================
# 📁 UPLOAD FILE CSV
# ===============================
st.title("TH Hòa Minh - Thi Cải Cách Hành Chính Và CĐS")

uploaded_file = st.file_uploader(
    "Tải lên file questions.csv (các cột: id, question, correct_answer)",
    type=["csv"]
)

df = None
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Đã đọc file CSV thành công!")
    except:
        st.error("❌ Không thể đọc file CSV.")


# ===============================
# CALLBACK NHẤN NÚT TÌM
# ===============================
def on_search_click():
    st.session_state.last_query = st.session_state.query.strip()
    st.session_state.query = ""        # Xóa ô nhập
    st.session_state.search_now = True


# ===============================
# Ô NHẬP TỪ KHÓA
# ===============================
query = st.text_input(
    "🔍 Nhập từ khóa để tìm câu hỏi:",
    key="query",
    placeholder="Nhập nội dung bất kỳ có trong câu hỏi..."
)

st.button("Tìm câu hỏi", on_click=on_search_click)


# ===============================
# 🔍 XỬ LÝ TÌM KIẾM
# ===============================
if st.session_state.search_now:

    # tắt chế độ tìm ngay để tránh lặp
    st.session_state.search_now = False

    if df is None:
        st.error("❌ Vui lòng tải file CSV trước.")
    else:
        q = st.session_state.last_query

        if q == "":
            st.warning("⚠ Vui lòng nhập từ khóa.")
        else:
            mask = df["question"].astype(str).str.contains(q, case=False, na=False)
            results = df[mask]

            if results.empty:
                st.warning("⚠ Không tìm thấy kết quả phù hợp.")
            else:
                for _, row in results.iterrows():
                    st.markdown(
                        f"<div class='question-box'><b>❓ Câu hỏi:</b><br>{row['question']}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div class='answer-box'>✔ <b>Đáp án đúng:</b> {row['correct_answer']}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("---")

    # Xóa last_query sau khi xong
    st.session_state.last_query = ""


