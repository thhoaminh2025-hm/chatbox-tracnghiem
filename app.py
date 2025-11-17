import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chatbox Trắc nghiệm", page_icon="📘")

st.title("📘 Chatbox Tìm Câu Hỏi Trắc Nghiệm")

uploaded_file = st.file_uploader("Tải lên file questions.csv (id,question,correct_answer)", type=["csv"])

def load_custom_csv(file):
    """Đọc file CSV và xử lý dấu phẩy trong câu hỏi."""
    lines = file.read().decode("utf-8").splitlines()
    data = []

    for line in lines[1:]:  # bỏ dòng header
        parts = line.split(",")

        if len(parts) < 3:
            continue

        id_val = parts[0]
        correct_answer = parts[-1]
        question = ",".join(parts[1:-1])  # ghép lại phần câu hỏi

        data.append([id_val, question, correct_answer])

    return pd.DataFrame(data, columns=["id", "question", "correct_answer"])


if uploaded_file:
    df = load_custom_csv(uploaded_file)

    st.write("📌 **Các cột đã đọc được:**", list(df.columns))

    query = st.text_input("🔍 Nhập từ khóa để tìm câu hỏi:")

    if query:
        results = df[df["question"].str.contains(query, case=False, na=False)]

        if results.empty:
            st.warning("⚠ Không tìm thấy câu hỏi phù hợp.")
        else:
            for _, row in results.iterrows():
                st.write("### ❓ Câu hỏi:")
                st.write(row["question"])

                st.write(f"**➡ Đáp án đúng:** {row['correct_answer']}")
                st.markdown("---")

else:
    st.info("📂 Vui lòng tải lên file CSV để bắt đầu.")
