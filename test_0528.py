import streamlit as st

st.title("第7回 Streamlit フォーム演習 - テンプレート")
st.caption("st.form を使ってサークル入会申し込みフォームを作成しましょう。")

st.markdown("---")
st.subheader("演習: サークル入会申し込みフォーム")
st.write("**課題**: フォームを使って、サークル入会の申し込み情報をまとめて処理するアプリを作成する。")

# ここに演習のコードを記述してください
with st.form("サークル入会フォーム"):
    name = st.text_input("氏名", key="form_name")  # Add key
    grade = st.selectbox("学年", ["1年", "2年", "3年", "4年"], key="form_grade")  # Add key
    activity = st.selectbox("好きな活動", ["スポーツ", "音楽", "アート", "読書"], key="form_activity")  # Add key
    comment = st.text_area("コメント", key="form_comment")  # Add key
    submitted = st.form_submit_button("申し込む", key="form_submit")  # Add key
    if submitted:
        st.write(f"氏名: {name}, 学年: {grade}, 好きな活動: {activity}, コメント: {comment} で申し込みました。")
# ヒント: with st.form("フォーム名"): でフォームを作成し、st.form_submit_button() で送信ボタンを設置


st.markdown("---")
st.info("💡 全ての項目を入力してから「申し込む」ボタンを押すと、まとめて処理されることを確認してください。") 
