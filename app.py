import streamlit as st
import json
from PIL import Image

st.set_page_config(page_title="ssAI Engine", layout="wide")

# --- デザイン（HTML直接注入） ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    .status-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #6366f1; }
    </style>
    """, unsafe_allow_html=True)

# --- 学習データの管理 ---
if "study_logs" not in st.session_state:
    st.session_state.study_logs = []

# --- サイドバー：JSON保存・読込 ---
with st.sidebar:
    st.header("💾 学習データ管理")
    
    # 1. JSONとして書き出し（ダウンロードボタン）
    if st.session_state.study_logs:
        json_data = json.dumps(st.session_state.study_logs, ensure_ascii=False, indent=2)
        st.download_button(
            label="学習データをJSONで保存",
            data=json_data,
            file_name="ssai_memory.json",
            mime="application/json"
        )
    
    # 2. 保存したJSONを読み込み（アップロード）
    uploaded_json = st.file_uploader("過去のJSONを復元", type="json")
    if uploaded_json:
        st.session_state.study_logs = json.load(uploaded_json)
        st.success("データを復元しました！")

# --- メイン画面 ---
st.title("🤖 ssAI 学習エンジン")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 教材を渡す")
    img_file = st.file_uploader("ノートや問題をアップロード", type=["jpg", "png"])
    if img_file:
        st.image(img_file, use_container_width=True)

with col2:
    st.subheader("2. AIの思考")
    query = st.text_input("指示を入力")
    
    if st.button("実行"):
        # ここでAI処理（例：画像解析）を行う
        # Render無料枠では外部API（OpenAIやGroq）を叩くのが安全です
        res = f"「{query}」についての解析結果（ダミー）: 過去の学習内容を{len(st.session_state.study_logs)}件参照しました。"
        st.session_state.last_res = res
        st.info(res)

# --- フィードバック（JSONへの保存対象） ---
if "last_res" in st.session_state:
    st.divider()
    st.subheader("3. 学習させる（JSONに記録）")
    feedback = st.text_input("今の回答への修正・個性付け")
    
    if st.button("自我を保存"):
        new_memory = {
            "query": query,
            "response": st.session_state.last_res,
            "feedback": feedback
        }
        st.session_state.study_logs.append(new_memory)
        st.success("新しい個性を内部リストに追加しました。サイドバーからJSONを保存してください。")

# 現在の学習内容を表示
if st.session_state.study_logs:
    with st.expander("現在の学習データ一覧"):
        st.write(st.session_state.study_logs)
