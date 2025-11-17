import streamlit as st
import pandas as pd

# ================================
# 1. KHỞI TẠO SESSION STATE AN TOÀN
# ================================
if "keyword" not in st.session_state:
    st.session_state.keyword = ""

if "filter_subject" not in st.session_state:
    st.session_state.filter_subject = ""

if "filter_level" not in st.session_state:
    st.session_state.filter_level = ""

# ============================
# 2. LOAD FILE DỮ LIỆU
# ============================
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    return df

df = load_data()

st.title("Chatbox Trắc nghiệm – Bộ lọc câu hỏi")

# ============================
# 3. INPUT TỪ NGƯỜI DÙNG
# ============================
keyword = st.text_input("Tìm kiếm từ khoá", st.session_state.keyword)
subject_list = ["", "Toán", "Tiếng Việt", "TNXH", "Khoa học", "Lịch sử"]
level_list = ["", "Nhận biết", "Thông hiểu", "Vận dụng"]

subject = st.selectbox("Chọn môn", subject_list, index=subject_list.index(st.session_state.filter_subject))
level = st.selectbox("Chọn mức độ", level_list, index=level_list.index(st.session_state.filter_level))

# ============================
# 4. NÚT LỌC
# ============================
if st.button("Lọc dữ liệu"):
    st.session_state.keyword = keyword
    st.session_state.filter_subject = subject
    st.session_state.filter_level = level

# ============================
# 5. ÁP DỤNG LỌC
# ============================
filtered_df = df.copy()

if st.session_state.keyword:
    filtered_df = filtered_df[filtered_df["question"].str.contains(st.session_state.keyword, case=False, na=False)]

if st.session_state.filter_subject:
    filtered_df = filtered_df[filtered_df["subject"] == st.session_state.filter_subject]

if st.session_state.filter_level:
    filtered_df = filtered_df[filtered_df["level"] == st.session_state.filter_level]

st.write("### Kết quả lọc")
st.dataframe(filtered_df)

# ============================
# 6. XÓA BỘ LỌC
# ============================
if st.button("Reset bộ lọc"):
    st.session_state.keyword = ""
    st.session_state.filter_subject = ""
    st.session_state.filter_level = ""
    st.experimental_rerun()
