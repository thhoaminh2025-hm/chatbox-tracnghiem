# -------------------------------
# TÌM KIẾM (KHÔNG LỖI auto-clear)
# -------------------------------

# Tạo hàm clear để dùng trong on_click
def clear_keyword():
    st.session_state.keyword = ""

# Tạo input có state key
keyword = st.text_input("🔍 Nhập từ khóa để tìm", key="keyword")

# Khi nhấn nút, search sẽ chạy → sau đó auto-clear
search_btn = st.button("Tìm câu hỏi", on_click=clear_keyword)

if search_btn:
    if df is None:
        st.error("❌ Chưa có dữ liệu. Hãy nhập link RAW hoặc tải file CSV.")
    else:
        if keyword.strip() == "":
            st.warning("⚠️ Vui lòng nhập từ khóa.")
        else:
            # Tìm kiếm không phân biệt hoa/thường
            results = df[df["question"].str.contains(keyword, case=False, na=False)]

            if results.empty:
                st.info("❗ Không tìm thấy kết quả.")
            else:
                for _, row in results.iterrows():
                    st.write("### ❓ Câu hỏi:")
                    st.write(row["question"])
                    st.write("### ✅ Đáp án đúng:")
                    st.success(row["correct_answer"])
                    st.write("---")
