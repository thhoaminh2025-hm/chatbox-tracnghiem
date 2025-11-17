import streamlit as st
import pandas as pd

st.title("🔎 Tìm câu hỏi & đáp án trong CSV")

# --- Upload CSV ---
uploaded_file = st.file_uploader("📁 Tải lên file questions.csv", type=["csv"])

df = None  # Khởi tạo biến tránh lỗi

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Kiểm tra 3 cột bắt buộc
        required_cols = {"id", "question", "correct_answer"}
        if not required_cols.issubset(df.columns):
            st.error("❌ File CSV phải có 3 cột: id, question, correct_answer")
            df = None

    except Exception as e:
        st.error("❌ Không thể đọc CSV. Vui lòng kiểm tra lại file.")
        df = None


# --- Ô nhập từ khóa (auto-clear sau khi tìm) ---
keyword = st.text_input("🔍 Nhập từ khóa để tìm", key="search_box")

# --- Nút tìm kiếm ---
if st.button("Tìm câu hỏi"):
    if not df is None:
        if keyword.strip() == "":
            st.warning("⚠️ Vui lòng nhập từ khóa.")
        else:
            # Tìm trong câu hỏi
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
    else:
        st.error("❌ Không có dữ liệu CSV để tìm kiếm.")
