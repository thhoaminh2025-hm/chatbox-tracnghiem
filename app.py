import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Chatbox Trắc nghiệm", page_icon="📘")

st.title("📘 Chatbox Tìm Câu Hỏi Trắc Nghiệm")

# 🔗 Nhập link RAW của CSV từ GitHub
csv_url = st.text_input("Nhập link RAW của file CSV trên GitHub:")

def load_custom_csv_from_url(url):
    """Tải CSV và xử lý dấu phẩy trong câu hỏi."""
    response = requests.get(url)

    if response.status_code != 200:
        st.error("❌ Không tải được file CSV. Vui lòng kiểm tra lại link.")
        return None

    lines = response.text.splitlines()
    data = []

    for line in lines[1:]:  # bỏ dòng header
        parts = line.split(",")

        if len(parts) < 3:
            continue

        id_val = parts[0]
        correct_answer = parts[-1]
        question = ",".join(parts[1:-1])  # ghép lại câu hỏi có dấu phẩy

        data.append([id_val, question, correct_answer])

    return pd.DataFrame(data, columns=["id", "question", "correct_answer"])


# 🔍 Khi có link CSV
if csv_url:
    df = load_custom_csv_from_url(csv_url)

    if df is not None:
        st.success("✅ Tải file thành công!")

        query = st.text_input("Nhập từ khóa để tìm câu hỏi:")

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
