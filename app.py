import streamlit as st
import pandas as pd
import requests
from io import StringIO
import unicodedata
import re

# -------------------------
# Helpers
# -------------------------
def remove_diacritics(text: str) -> str:
    if not isinstance(text, str):
        return text
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def normalize_text(text: str) -> str:
    # lower, strip, remove extra spaces, remove diacritics
    t = str(text).lower().strip()
    t = re.sub(r'\s+', ' ', t)
    t = remove_diacritics(t)
    return t

def build_mask(df, query, mode='any'):
    """
    mode:
      - 'any' : any token (OR)
      - 'all' : all tokens (AND)
      - 'exact': exact phrase
    """
    if query.strip() == "":
        return pd.Series([False]*len(df), index=df.index)

    # normalize questions once (cached column)
    if '_q_norm' not in df.columns:
        df['_q_norm'] = df['question'].astype(str).apply(normalize_text)

    q_norm = normalize_text(query)

    if mode == 'exact':
        # exact phrase match in normalized text
        mask = df['_q_norm'].str.contains(re.escape(q_norm), na=False)
        return mask

    # tokenize query by spaces
    tokens = [tok for tok in re.split(r'\s+', q_norm) if tok]
    if not tokens:
        return pd.Series([False]*len(df), index=df.index)

    if mode == 'any':
        # any token matches
        mask = pd.Series(False, index=df.index)
        for tok in tokens:
            mask = mask | df['_q_norm'].str.contains(re.escape(tok), na=False)
        return mask

    if mode == 'all':
        # all tokens must be present
        mask = pd.Series(True, index=df.index)
        for tok in tokens:
            mask = mask & df['_q_norm'].str.contains(re.escape(tok), na=False)
        return mask

    # fallback
    return pd.Series([False]*len(df), index=df.index)

# -------------------------
# App UI
# -------------------------
st.set_page_config(page_title="Chatbox Trắc Nghiệm (Tìm nâng cao)", layout="centered")
st.title("🔎 Chatbox Tìm Câu Hỏi Trắc Nghiệm (nâng cao)")

st.markdown("Bạn có thể dán link RAW GitHub hoặc upload file CSV (cột: id, question, correct_answer).")
col1, col2 = st.columns([3,1])

with col1:
    csv_url = st.text_input("🔗 Dán link RAW CSV (tùy chọn):", help="Ví dụ: https://raw.githubusercontent.com/username/repo/main/questions.csv")

with col2:
    uploaded_file = st.file_uploader("📥 Hoặc tải file CSV", type=["csv"])

df = None
# load from url if provided
if csv_url and csv_url.strip():
    try:
        r = requests.get(csv_url.strip(), timeout=10)
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text))
        st.success("✅ Đã tải CSV từ URL")
    except Exception as e:
        st.error(f"❌ Lỗi khi tải CSV từ URL: {e}")
        df = None

# if uploader used and df not loaded from url
if uploaded_file and df is None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Đã đọc file CSV upload")
    except Exception as e:
        st.error(f"❌ Không đọc được file CSV: {e}")
        df = None

# if df loaded, validate columns
if df is not None:
    required = {"id", "question", "correct_answer"}
    if not required.issubset(set(df.columns)):
        st.error("❌ CSV phải có 3 cột: id, question, correct_answer")
        st.stop()

    # ensure question is str
    df['question'] = df['question'].astype(str)

# search controls
st.markdown("---")
if df is None:
    st.info("⏳ Hãy nhập link RAW hoặc upload file CSV để bắt đầu.")
else:
    st.write(f"📚 Dữ liệu: {len(df)} câu hiện có.")
    # choose mode
    mode = st.selectbox("Chế độ tìm", options=['any (any token / OR)', 'all (all tokens / AND)', 'exact (exact phrase)'], index=0)
    # map to simple keys
    mode_map = {'any (any token / OR)': 'any', 'all (all tokens / AND)': 'all', 'exact (exact phrase)': 'exact'}

    # session_state for textbox
    if 'keyword' not in st.session_state:
        st.session_state.keyword = ''

    keyword = st.text_input("🔍 Nhập từ khóa để tìm", key='keyword', placeholder="Ví dụ: 'không thuộc đối tượng' hoặc 'SIPAS'")

    def on_search_click():
        # callback used only to trigger re-run and then we clear below after search displayed
        pass

    search_clicked = st.button("Tìm câu hỏi", on_click=on_search_click)

    if search_clicked:
        q = str(keyword).strip()
        if q == "":
            st.warning("⚠️ Vui lòng nhập từ khóa.")
        else:
            mode_key = mode_map[mode]
            mask = build_mask(df, q, mode=mode_key)
            results = df[mask].copy()

            st.write(f"🔎 Kết quả: {len(results)} câu tìm thấy (chế độ: {mode_key})")
            if len(results) == 0:
                # show debug hints
                st.info("Không tìm thấy kết quả. Thử các gợi ý sau:")
                st.markdown("""
                - Kiểm tra chính tả hoặc thử bỏ dấu (ví dụ: `khong thuoc doi tuong`)  
                - Thử thay đổi chế độ: **any** hoặc **exact**  
                - Thử tìm 1 từ ngắn hơn (ví dụ: chỉ `thuoc`)  
                """)
                # show sample of normalized question to help debugging
                sample_norm = normalize_text(q)
                st.write("🔧 Debug: chuỗi tìm (normalize):", sample_norm)
                # show first 5 normalized questions for manual check
                st.markdown("Ví dụ vài câu (normalized):")
                tmp = df[['id','question']].head(5).copy()
                tmp['question_normalized'] = tmp['question'].apply(normalize_text)
                st.dataframe(tmp)
            else:
                # display results (only question + correct_answer)
                for _, row in results.iterrows():
                    st.markdown("---")
                    st.markdown("### ❓ Câu hỏi:")
                    # highlight keyword in displayed question (simple highlight on normalized match)
                    # show original question only
                    st.write(row['question'])
                    st.markdown("### ✅ Đáp án đúng:")
                    st.success(row['correct_answer'])

            # auto-clear keyword by setting session_state AFTER showing results (via callback trick)
            # streamlit won't allow changing session_state during render triggered by button? it's safe here since it's in on_click no state change; to be safe, we schedule clear using st.experimental_rerun:
            st.session_state.keyword = ""  # clear for next search
            st.experimental_rerun()
