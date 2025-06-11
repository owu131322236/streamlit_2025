import streamlit as st
import datetime
import os

#保存用フォルダの設定
DIARY_FOLDER = "my_diaries"
os.makedirs(DIARY_FOLDER, exist_ok=True)

# ここから関数---------------------------------------------------------------

def get_diary_filepath(date_str):
    #ファイルの場所を返す関数
    return os.path.join(DIARY_FOLDER, f"{date_str}.txt")

def load_diary_content(date_str):
    filepath = get_diary_filepath(date_str)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_diary_content(date_str, content):
    filepath = get_diary_filepath(date_str)
    #openでファイルを開き、wで書き込む。開いたファイルオブジェクトを f という変数名で扱えるように
    with open(filepath, "w", encoding="utf-8") as f:
        #ファイルにcontentを書き込む
        f.write(content)

def get_all_recorded_dates():
    dates = set()
    for filename in os.listdir(DIARY_FOLDER):
        if filename.endswith(".txt"):
            date_str = filename.replace(".txt", "")
            try:
                dates.add(datetime.datetime.strptime(date_str, "%Y-%m-%d").date())
            except ValueError:
                pass
    return sorted(list(dates), reverse=True)

def display_diary_entry(date_obj, is_expanded=False):
    #この関数は特定の日付の日記を表示するためのもの
    date_str = date_obj.strftime("%Y-%m-%d")
    diary_content = load_diary_content(date_str)

    if diary_content:
        with st.expander(f"{date_obj.strftime('%Y年%m月%d日')} の日記", expanded=is_expanded):
            st.write(diary_content)
    else:
        st.info(f"{date_obj.strftime('%Y年%m月%d日')} にはまだ日記が書かれていません。")

# ----------------------------------------------------------------

st.set_page_config(layout="wide", page_title="シンプル日記アプリ")

st.title("日記アプリ")
view_mode_date_str = st.query_params.get("view_date")


st.sidebar.header("過去の日記を閲覧")
available_dates = get_all_recorded_dates()

if available_dates:
    selected_date_for_view = st.sidebar.selectbox(
        "閲覧したい日付を選んでください:",
        available_dates,
        format_func=lambda d: d.strftime("%Y年%m月%d日"),
        key ="sidebar_date_selector" # キーを slider_date_selector から変更
    )
    
    if selected_date_for_view: 
        # query_paramsを設定すると、Streamlitはページを再実行し、メインコンテンツが切り替わる
        st.query_params["view_date"] = selected_date_for_view.strftime("%Y-%m-%d")
else:
    st.sidebar.info("まだ日記が保存されていません。")

# main-content-------------------------------------------------
if view_mode_date_str:
    display_date_obj = datetime.datetime.strptime(view_mode_date_str, '%Y-%m-%d').date()
    
    st.subheader(f"{display_date_obj.strftime('%Y年%m月%d日')} の日記")
    display_diary_entry(display_date_obj, is_expanded=True) # 常に展開して表示

    if st.button("日記一覧に戻る"): 
        st.query_params.clear() # URLのクエリパラメータをクリア
        st.rerun() #強制的にホームへ
    
else:
    # URLパラメータがない場合（通常の日記入力/過去の日記一覧モード）
    current_selected_date = st.date_input("日付を選んでください:", value=datetime.date.today())
    current_date_str = current_selected_date.strftime("%Y-%m-%d")

    if f"diary_text_{current_date_str}" not in st.session_state:
        st.session_state[f"diary_text_{current_date_str}"] = load_diary_content(current_date_str)

    diary_text_input = st.text_area(
        f"{current_selected_date.strftime('%Y年%m月%d日')} の日記を書いてください:",
        value=st.session_state[f"diary_text_{current_date_str}"],
        height=300,
        key=f"diary_editor_{current_date_str}"
    )

    if st.button("日記を保存", key=f"save_button_{current_date_str}"):
        save_diary_content(current_date_str, diary_text_input)
        st.session_state[f"diary_text_{current_date_str}"] = diary_text_input
        
        st.success("日記を保存しました！")

        st.markdown("---")
        st.subheader("あなたへのメッセージ")
        diary_length = len(diary_text_input)
        if diary_length == 0:
            st.info("今日の出来事を少しでも記録してみませんか？")
        elif diary_length < 50:
            st.write("短くても、今日の出来事を記録できて素晴らしいです！")
        elif diary_length < 200:
            st.write("たくさん書いて、今日の気持ちを整理できましたね。よく頑張りました！")
        elif diary_length < 500:
            st.write("素晴らしい！深く考察し、たくさんのことを書き記しましたね。")
        else:
            st.write("とても充実した内容ですね！詳細な記録、お疲れ様でした。")

        # 保存後、その日の日記をすぐに表示（展開）
        display_diary_entry(current_selected_date, is_expanded=True) #is_expanded=Trueは展開して表示するため
    else:
        # 保存ボタンが押されていない場合、現在の編集中の記録を表示
        st.markdown("---")
        st.subheader("あなたへのメッセージ")
        st.write("今日の出来事を記録してみませんか？")

    st.markdown("---")
    st.header("全ての過去の日記")

    all_recorded_dates_for_display = get_all_recorded_dates()
    if all_recorded_dates_for_display: # 過去の日記が存在する場合
        for date_obj in all_recorded_dates_for_display:
            if date_obj == current_selected_date:
                continue
            display_diary_entry(date_obj, is_expanded=False) # デフォルトは閉じる
    else:
        st.info("まだ過去の日記がありません。")
