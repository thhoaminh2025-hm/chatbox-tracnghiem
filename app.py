import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbox Trắc nghiệm", page_icon="📘")

st.title("📘 Chatbox Tìm Câu Hỏi Trắc Nghiệm")

# Load file CSV
uploaded_file = st.file_uploader("Tải lên file CSV (gồm question, answer)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("📌 **Các cột tìm thấy trong file:**", list(df.columns))

    # Kiểm tra cột
    if "question" not in df.columns or "answer" not in df.columns:
        st.error("❌ File CSV phải chứa 2 cột: 'question' và 'answer'. Vui lòng kiểm tra lại file.")
        st.stop()

    query = st.text_input("Nhập từ khóa để tìm câu hỏi:")
    
    if query:
        # Tìm kiếm không phân biệt hoa thường
        mask = df["question"].str.contains(query, case=False, na=False)
        results = df[mask]

        if results.empty:
            st.warning("⚠ Không tìm thấy câu hỏi nào phù hợp.")
        else:
            for i, row in results.iterrows():
                st.write(f"**Câu hỏi:** {row['question']}")
                st.write(f"➡ **Đáp án:** {row['answer']}")
                st.markdown("---")
else:
    st.info("📂 Vui lòng tải lên file CSV để bắt đầu.")
