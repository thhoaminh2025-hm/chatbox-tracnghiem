import streamlit as st
import pandas as pd

st.set_page_config(page_title=" Tra cứu Thi Cải Cách Hành Chính Và CĐS", page_icon="📘")

st.title("📘 Tra cứu Thi Cải Cách Hành Chính Và CĐS")


# ------------------------------------
# Hàm reset từ khóa (auto-clear)
# ------------------------------------
def clear_keyword():
    st.session_state.query = ""


# Upload file CSV
uploaded_file = st.file_uploader(
    "Tải lên file questions.csv (các cột: id, question, correct_answer)",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Kiểm tra cột cần thiết
    required_cols = {"question", "correct_answer"}
    if not required_cols.issubset(df.columns):
        st.error("❌ File CSV phải có 2 cột: 'question' và 'correct_answer'.")
        st.stop()

    # Tạo session state cho ô từ khóa
    if "query" not in st.session_state:
        st.session_state.query = ""

    query = st.text_input("🔍 Nhập từ khóa để tìm câu hỏi:", key="query")

    # Nút tìm + auto-clear bằng on_click
    if st.button("Tìm câu hỏi", on_click=clear_keyword):
        if query.strip() == "":
            st.warning("⚠ Vui lòng nhập từ khóa.")
        else:
            mask = df["question"].str.contains(query, case=False, na=False)
            results = df[mask]

            if results.empty:
                st.warning("⚠ Không tìm thấy câu hỏi phù hợp.")
            else:
                for _, row in results.iterrows():
                    st.write("### ❓ Câu hỏi:")
                    st.write(row["question"])

                    # TÔ XANH ĐÁP ÁN ĐÚNG
                    st.markdown(
                        f"<div style='background-color:#d4edda; "
                        f"padding:10px; border-left:6px solid #28a745; "
                        f"border-radius:5px; font-size:18px;'>"
                        f"✔ <b>Đáp án đúng:</b> {row['correct_answer']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown("---")

else:
    st.info("📂 Vui lòng tải lên file CSV để bắt đầu.")
