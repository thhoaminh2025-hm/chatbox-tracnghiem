import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.title("🔎 Tìm câu hỏi & đáp án trong CSV")

# ======================
# 1. HÀM RESET TỪ KHÓA
# ======================
def reset_keyword():
    st.session_state.search_box = ""

# ======================
# 2. TẢI DỮ LIỆU
# ======================
csv_url = st.text_input("🔗 Dán link RAW CSV (tùy chọn):")
df = None

if csv_url.strip():
    try:
        r = requests.get(csv_url)
        if r.status_code == 200:
            df = pd.read_csv(StringIO(r.text))
            st.success("✅ Đã tải CSV từ URL!")
        else:
            st.error("❌ Không tải được file. Kiểm tra link RAW.")
    except Exception as e:
        st.error(f"❌ Lỗi tải dữ liệu: {e}")

uploaded = st.file_uploader("📥 Hoặc chọn file CSV", type=["csv"])
if uploaded and df is None:
    try:
        df = pd.read_csv(uploaded)
        st.success("✅ Đã đọc file CSV thành công!")
    except Exception as e:
        st.error(f"❌ Không đọc được CSV: {e}")

# ======================
# 3. KIỂM TRA CỘT
# ======================
if df is not None:
    required = {"id", "question", "correct_answer"}
    if not required.issubset(df.columns):
        st.error("❌ CSV phải có 3 cột: id, question, correct_answer")
        df = None

# ======================
# 4. TÌM KIẾM
# ======================
keyword = st.text_input("🔍 Nhập từ khóa để tìm", key="search_box")

# NÚT TÌM CÓ CALLBACK CLEAR
search = st.button("Tìm câu hỏi", on_click=reset_keyword)

if search:
    if df is None:
        st.error("❌ Chưa có dữ liệu.")
    elif not keyword.strip():
        st.warning("⚠️ Vui lòng nhập từ khóa.")
    else:
        results = df[df["question"].str.contains(keyword, case=False, na=False)]

        if results.empty:
            st.info("❗ Không tìm thấy kết quả.")
        else:
            for _, row in results.iterrows():
                st.write("### ❓ Câu hỏi")
                st.write(row["question"])

                st.write("### 🟩 Đáp án đúng")
                st.success(row["correct_answer"])
                st.write("---")
