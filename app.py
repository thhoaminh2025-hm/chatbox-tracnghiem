import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Chatbox Trắc nghiệm", page_icon="📘")

st.title("📘 Chatbox Tìm Câu Hỏi Trắc Nghiệm")

csv_url = st.text_input("Nhập link RAW CSV từ GitHub:")

def normalize_url(url: str):
    """Tự thêm https:// nếu thiếu."""
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

def load_custom_csv_from_url(url):
    """Tải CSV và xử lý dấu phẩy trong câu hỏi."""
    try:
        response = requests.get(url)
    except Exception as e:
        st.error(f"❌ Lỗi URL: {e}")
        return None

    if response.status_code != 200:
        st.error("❌ Không tải được file CSV. Vui lòng kiểm tra link RAW GitHub.")
        return None

    lines = response.text.splitlines()
    data = []

    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) < 3:
            continue

        id_val = parts[0]
        correct_answer = parts[-1]
        question = ",".join(parts[1:-1])

        data.append([id_val, question, correct_answer])

    return pd.DataFrame(data, columns=["id", "question", "correct_answer"])


if csv_url:
    norm_url = normalize_url(csv_url)
    df = load_custom_csv_from_url(norm_url)

    if df is not None:
        st.success("✅ Tải file CSV thành công!")

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
