import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.title("🔎 Tìm câu hỏi & đáp án trong CSV")

st.subheader("📁 Chọn 1 trong 2 cách nhập dữ liệu:")

# =========================================
# 1️⃣ ĐỌC LINK RAW GITHUB
# =========================================
csv_url = st.text_input("🔗 Dán link RAW CSV (tùy chọn):")

df = None

if csv_url.strip():
    try:
        st.info("⏳ Đang tải dữ liệu từ URL...")
        response = requests.get(csv_url)

        if response.status_code != 200:
            st.error(f"❌ Không tải được CSV (HTTP {response.status_code}). Kiểm tra link RAW.")
        else:
            df = pd.read_csv(StringIO(response.text))
            st.success("✅ Đã tải thành công từ URL!")

    except Exception as e:
        st.error(f"❌ Lỗi khi tải dữ liệu từ URL:\n{e}")
        df = None


# =========================================
# 2️⃣ UPLOAD FILE CSV
# =========================================
uploaded_file = st.file_uploader("📥 Hoặc tải lên file questions.csv", type=["csv"])

if uploaded_file and df is None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Đã đọc file CSV thành công!")
    except Exception as e:
        st.error(f"❌ Không thể đọc CSV: {e}")
        df = None


# =========================================
# KIỂM TRA CẤU TRÚC CSV
# =========================================
if df is not None:
    required_cols = {"id", "question", "correct_answer"}
    if not required_cols.issubset(df.columns):
        st.error("❌ CSV phải có 3 cột đúng tên: id, question, correct_answer")
        df = None


# =========================================
# 3️⃣ NHẬP TỪ KHÓA + TÌM KIẾM
# =========================================
if "search_box" not in st.session_state:
    st.session_state.search_box = ""

keyword = st.text_input("🔍 Nhập từ khóa để tìm", key="search_box")

search = st.button("Tìm câu hỏi")

if search:
    if df is None:
        st.error("❌ Chưa có dữ liệu. Nhập link RAW hoặc tải file CSV.")
    else:
        if keyword.strip() == "":
            st.warning("⚠️ Vui lòng nhập từ khóa.")
        else:
            results = df[df["question"].str.contains(keyword, case=False, na=False)]

            if results.empty:
                st.info("❗ Không tìm thấy kết quả.")
            else:
                for _, row in results.iterrows():
                    st.write("### ❓ Câu hỏi")
                    st.write(row["question"])
                    st.write("### ✅ Đáp án đúng")
                    st.success(row["correct_answer"])
                    st.write("---")

    # 🔥 AUTO CLEAR KEYWORD SAU KHI TÌM
    st.session_state.search_box = ""
