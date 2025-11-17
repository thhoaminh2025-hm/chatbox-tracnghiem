import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbox Trắc nghiệm", page_icon="📘")

st.title("📘 Chatbox Tìm Câu Hỏi Trắc Nghiệm")

# Upload file CSV
uploaded_file = st.file_uploader("Tải lên file questions.csv (các cột: id, question, correct_answer, choices)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Hiển thị các cột tìm thấy
    st.write("📌 **Các cột trong file:**", list(df.columns))

    # Kiểm tra đủ cột
    required_cols = {"question", "correct_answer"}
    if not required_cols.issubset(df.columns):
        st.error("❌ File CSV phải có cột: 'question' và 'correct_answer'.")
        st.stop()

    query = st.text_input("🔍 Nhập từ khóa để tìm câu hỏi:")

    if query:
        mask = df["question"].str.contains(query, case=False, na=False)
        results = df[mask]

        if results.empty:
            st.warning("⚠ Không tìm thấy câu hỏi phù hợp.")
        else:
            for i, row in results.iterrows():
                st.write(f"### ❓ Câu hỏi:")
                st.write(row["question"])

                st.write(f"**➡ Đáp án đúng:** {row['correct_answer']}")

                # Nếu có cột choices thì hiển thị
                if "choices" in df.columns:
                    st.write("📌 **Các lựa chọn:**")
                    try:
                        # nếu choices dạng "A. xxx; B. yyy"
                        for ch in str(row["choices"]).split(";"):
                            st.write("- " + ch.strip())
                    except:
                        st.write(row["choices"])

                st.markdown("---")
else:
    st.info("📂 Vui lòng tải lên file CSV để bắt đầu.")
