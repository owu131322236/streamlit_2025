import streamlit as st
import datetime
import os

DIARY_FOLDER = "my_diaries"
os.makedirs(DIARY_FOLDER, exist_ok=True)

EMOTION_ICONS = {
    0: "最悪 😩",
    1: "悪い 😔",
    2: "普通 😐",
    3: "良い 😊",
    4: "最高 🤩"
}

def get_diary_filepath(date_str):
    return os.path.join(DIARY_FOLDER, f"{date_str}.txt")

def load_diary_content(date_str):
    filepath = get_diary_filepath(date_str)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_diary_content(date_str, content):
    filepath = get_diary_filepath(date_str)
    with open(filepath, "w", encoding="utf-8") as f:
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
    date_str = date_obj.strftime("%Y-%m-%d")
    diary_content = load_diary_content(date_str)

    if diary_content:
        with st.expander(f"{date_obj.strftime('%Y年%m月%d日')} の日記", expanded=is_expanded):
            st.write(diary_content)
    else:
        st.info(f"{date_obj.strftime('%Y年%m月%d日')} にはまだ日記が書かれていません。")
def custom_css():
    st.markdown(
        """<style>
        :root {
        --primaryColor: #3872fb;
        --backgroundColor: #FDFBF6;
        --secondaryBackgroundColor: #E0E6E9;
        --textColor: #5A5A5A;
        --font: monospace;
        }

        body {
        background-color: var(--backgroundColor);
        color: var(--textColor);
        font-family: var(--font);
        }
        </style>""",unsafe_allow_html = True
    )

custom_css()

st.set_page_config(layout="wide", page_title="シンプル日記アプリ")
st.title("📔日記アプリ")

view_mode_date_str = st.query_params.get("view_date")
is_view_mode = bool(view_mode_date_str)


### サイドバー

st.sidebar.header("過去の日記を閲覧")
available_dates = get_all_recorded_dates()

if available_dates:
    sidebar_initial_index = 0
    if is_view_mode:
        #このif文は、URLから日付を取得して、サイドバーの初期選択を設定するためのもの
        try:
            date_from_url = datetime.datetime.strptime(view_mode_date_str, "%Y-%m-%d").date()
            if date_from_url in available_dates:
                sidebar_initial_index = available_dates.index(date_from_url)
        except ValueError:
            pass

    st.sidebar.selectbox(
        "閲覧したい日付を選んでください:",
        available_dates,
        index=sidebar_initial_index,
        format_func=lambda d: d.strftime("%Y年%m月%d日"),
        key="sidebar_date_selector",
        on_change=lambda: st.query_params.update({"view_date": st.session_state.sidebar_date_selector.strftime("%Y-%m-%d")}) and st.rerun()
    )
else:
    st.sidebar.info("まだ日記が保存されていません。")

### メインコンテンツ

if is_view_mode:
    display_date_obj = datetime.datetime.strptime(view_mode_date_str, '%Y-%m-%d').date()
    
    st.subheader(f"{display_date_obj.strftime('%Y年%m月%d日')} の日記")
    display_diary_entry(display_date_obj, is_expanded=True)

    if st.button("日記一覧に戻る", key="back_to_edit_button_view_mode"): 
        st.query_params.clear()
        st.rerun()
    
else:
    current_selected_date = st.date_input("日付を選んでください:", value=datetime.date.today(), key="main_date_input")
    current_date_str = current_selected_date.strftime("%Y-%m-%d")

    if f"diary_text_{current_date_str}" not in st.session_state:
        st.session_state[f"diary_text_{current_date_str}"] = load_diary_content(current_date_str)

    diary_text_input = st.text_area(
        f"{current_selected_date.strftime('%Y年%m月%d日')} の日記を書いてください:",
        value=st.session_state[f"diary_text_{current_date_str}"],
        height=300,
        key=f"diary_editor_{current_date_str}"
    )

    selected_emotion = st.slider(
        "今日の気分はどうでしたか？",
        min_value=0,
        max_value=4,
        value=2, # 初期値は「普通」
        step=1,
        key=f"emotion_slider_{current_date_str}"
    )

    if st.button("日記を保存", key=f"save_button_{current_date_str}"):
        final_diary_content = diary_text_input.strip() # 余白を削除
        emotion_string = EMOTION_ICONS.get(selected_emotion, "不明") # 選択された感情の文字列を取得      
        # 既存の内容に感情情報が既にある場合は、古いものを削除
        for icon_text in EMOTION_ICONS.values():
            if icon_text in final_diary_content:
                final_diary_content = final_diary_content.replace(icon_text, "").strip()
                break # 
        final_diary_content += f"\n\n感情レベル: {emotion_string}"

        save_diary_content(current_date_str, final_diary_content)
        st.session_state[f"diary_text_{current_date_str}"] = final_diary_content
        
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

        display_diary_entry(current_selected_date, is_expanded=True)

    else:
        st.markdown("---")
        st.subheader("あなたへのメッセージ")
        st.write("今日の出来事を記録してみませんか？")

    st.markdown("---")
    st.header("全ての過去の日記")

    all_recorded_dates_for_display = get_all_recorded_dates()
    if all_recorded_dates_for_display:
        for date_obj in all_recorded_dates_for_display:
            if date_obj == current_selected_date:
                continue
            display_diary_entry(date_obj, is_expanded=False)
    else:
        st.info("まだ過去の日記がありません。")
  
