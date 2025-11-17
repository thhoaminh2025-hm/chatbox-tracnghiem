import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.title("🔎 Tìm câu hỏi & đáp án trong CSV")

st.subheader("📁 Chọn 1 trong 2 cách nhập dữ liệu:")

# -------------------------------
# 1️⃣ NHẬP LINK RAW CSV TRỰC TIẾP
# -------------------------------
csv_url = st.text_input("🔗 Dán link RAW CSV (tùy chọn):")

df = None  # Khởi tạo biến

if csv_url.strip() != "":
    try:
        response = requests.get(csv_url)

        if response.status_code != 200:
            st.error("❌ Không thể tải file từ URL. Kiểm tra lại link RAW.")
        else:
            data = StringIO(response.text)
            df = pd.read_csv(data)

    except Exception:
        st.error("❌ Lỗi khi tải dữ liệu từ URL. Kiểm tra link RAW.")
        df = None


# -------------------------------
# 2️⃣ UPLOAD FILE CSV
# -------------------------------
uploaded_file = st.file_uploader("📥 Hoặc tải lên file questions.csv", type=["csv"])

if uploaded_file and df is None:
    try:
        df = pd.read_csv(uploaded_file)
    except:
        st.error("❌ Không thể đọc CSV. Kiểm tra file.")
        df = None


# -------------------------------
# Kiểm tra định dạng CSV
# -------------------------------
if df is not None:
    required_cols = {"id", "question", "correct_answer"}
    if not required_cols.issubset(df.columns):
        st.error("❌ CSV phải có 3 cột: id, question, correct_answer")
        df = None


# -------------------------------
# TÌM KIẾM
# -------------------------------
keyword = st.text_input("🔍 Nhập từ khóa để tìm", key="search_box")

if st.button("Tìm câu hỏi"):
    if df is None:
        st.error("❌ Chưa có dữ liệu. Hãy nhập link RAW hoặc tải file CSV.")
    else:
        if keyword.strip() == "":
            st.warning("⚠️ Vui lòng nhập từ khóa.")
        else:
            results = df[df["question"].str.contains(keyword, case=False, na=False)]

            if results.empty:
                st.info("❗ Không tìm thấy kết quả.")
            else:
                for _, row in results.iterrows():
                    st.write(f"### ❓ Câu hỏi:")
                    st.write(row["question"])
                    st.write(f"### ✅ Đáp án đúng:")
                    st.success(row["correct_answer"])
                    st.write("---")

            # 🔥 Auto-clear từ khóa
            st.session_state.search_box = ""
