import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting},
    ]
    st.session_state["job_content"] = ""
    st.session_state["ideal_candidate"] = ""
    st.session_state["company_pr"] = ""
    st.session_state["candidate_info"] = ""
    st.session_state["feedbacks"] = []  # feedbacksの初期化を追加

# チャットボットとやりとりする関数
def communicate(job_content, ideal_candidate, company_pr, candidate_info, feedback=None):
    messages = st.session_state["messages"].copy()  # メッセージリストをコピー

    user_message = {"role": "user", "content": f"求人内容: {job_content}\n求める人物像: {ideal_candidate}\nPR: {company_pr}\n求職者情報: {candidate_info}"}
    messages.append(user_message)

    if feedback:
        feedback_message = {"role": "user", "content": f"フィードバック: {feedback}"}
        messages.append(feedback_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=700
    )  

    bot_message = response["choices"][0]["message"]
    st.session_state["messages"].append(bot_message)  # ここでグローバルのメッセージリストにボットのメッセージを追加

    return bot_message

# ユーザーインターフェイスの構築
st.title("スカウトメッセージ作成bot")
st.image("syukyaku.jpg")
st.write("OpenAI's ChatGPTを使って、スカウトメッセージを作成します。")

job_content = st.text_input("求人内容を入力してください。", value=st.session_state["job_content"])
ideal_candidate = st.text_input("求める人物像を入力してください。", value=st.session_state["ideal_candidate"])
company_pr = st.text_input("企業のPRを入力してください。", value=st.session_state["company_pr"])
candidate_info = st.text_input("求職者情報を入力してください。", value=st.session_state["candidate_info"])

if st.button("送信"):
    result = communicate(job_content, ideal_candidate, company_pr, candidate_info)
    st.session_state["job_content"] = job_content
    st.session_state["ideal_candidate"] = ideal_candidate
    st.session_state["company_pr"] = company_pr
    st.session_state["candidate_info"] = candidate_info
    st.write("🤖: " + result["content"])

feedback = st.text_input("フィードバックを提供してください：", key="feedback")
if st.button("フィードバックを送信"):
    if st.session_state["messages"]:
        st.write("フィードバック前のメッセージ：")
        for message in st.session_state["messages"]:
            if message["role"] == "user":  # ユーザーからのメッセージのみ表示
                st.write("👤: " + message["content"])
    st.session_state["feedbacks"].append(feedback)
    result = communicate(job_content, ideal_candidate, company_pr, candidate_info, feedback)
    st.write("フィードバックを受け取りました！ AIがスカウトメッセージを修正しました：")
    st.write("🤖: " + result["content"])

if st.button("リセット"):
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting},
    ]
    st.session_state["job_content"] = ""
    st.session_state["ideal_candidate"] = ""
    st.session_state["company_pr"] = ""
    st.session_state["candidate_info"] = ""
    st.session_state["feedbacks"] = []  # リセット時にもfeedbacksを初期化
