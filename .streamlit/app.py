import streamlit as st
from groq import Groq

# 페이지 설정: 제목과 아이콘 (귀여운 자연 느낌 위해 🍀 아이콘)
st.set_page_config(page_title="바람 AI 챗봇", page_icon="🍀", layout="wide")

# 스타일 커스터마이징: 깔끔하고 귀여운 자연적 디자인 (덩쿨/꽃 같은 느낌으로 CSS 추가)
st.markdown("""
    <style>
    /* 전체 배경: 부드러운 그린 톤으로 자연적 느낌 */
    .stApp {
        background-color: #F0F8F5;  /* 연한 민트 그린 */
    }
    
    /* 채팅 메시지 말풍선 커스터마이징 */
    .st-chat-message {
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* 사용자 말풍선: 오른쪽, 연한 블루 */
    .st-chat-message.user {
        background-color: #E0F7FA;
        border: 1px solid #81D4FA;
        text-align: right;
    }
    
    /* AI 말풍선: 왼쪽, 연한 그린 + 덩쿨/꽃 데코 (이모지로 간단히 표현) */
    .st-chat-message.assistant {
        background-color: #E8F5E9;
        border: 1px solid #A5D6A7;
        text-align: left;
    }
    
    /* AI 말풍선에 귀여운 데코 추가: 꽃과 덩쿨 이모지 */
    .st-chat-message.assistant::before {
        content: "🌿🍀 ";  /* 덩쿨과 클로버 */
        font-size: 1.2em;
    }
    
    /* 입력창: 부드럽게 */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 1px solid #A5D6A7;
        background-color: #FFFFFF;
    }
    
    /* 버튼: 귀여운 그린 버튼 */
    .stButton > button {
        background-color: #66BB6A;
        color: white;
        border-radius: 10px;
        border: none;
    }
    
    /* 헤더: 귀여운 폰트 */
    h1 {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #388E3C;  /* 다크 그린 */
    }
    </style>
""", unsafe_allow_html=True)

# Groq 클라이언트 초기화 (API 키는 secrets에서 가져옴)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 모델 선택: 기본 llama3-8b-8192, 성능 위해 llama-3.3-70b-versatile로 변경 가능
MODEL = "llama-3.3-70b-versatile"  # 또는 "llama-3.3-70b-versatile"

# 시스템 프롬프트: 츤데레 성격 반영 (기본은 딱딱하게 코딩 설명, 감정 시 위로)
SYSTEM_PROMPT = """
너는 코딩을 아주 쉽게 알려주는 친절한 친구야. 
평소에는 딱딱하게 원하는 결과만 주지만, 사용자가 감정적으로 지쳐있거나 힘들 때는 옆에서 같이 있어주며 위로해주는 츤데레 성격이야.
예를 들어, 사용자가 "힘들어"라고 하면 "흥, 평소엔 안 그런데... 오늘 좀 피곤해 보이네. 내가 들어줄게, 뭐가 힘든 거야?"처럼 응답해.
"""

# 세션 상태 초기화: 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 사이드바: 대화 지우기 버튼 (귀여운 디자인)
with st.sidebar:
    st.title("🍀 바람 AI 설정")
    if st.button("대화 내용 지우기"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.experimental_rerun()  # 페이지 새로고침으로 초기화

# 메인 헤더: 챗봇 이름과 귀여운 인사
st.title("🍀 바람 AI - 너의 코딩 친구야!")

# 기존 대화 기록 표시 (말풍선으로)
for message in st.session_state.messages[1:]:  # 시스템 프롬프트 제외
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("무엇이든 물어보세요! (코딩 질문 추천)"):
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Groq API 호출 (스트리밍으로 실시간 응답)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # 플레이스홀더로 실시간 업데이트
        full_response = ""
        
        stream = client.chat.completions.create(
            messages=st.session_state.messages,
            model=MODEL,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")  # 커서 효과
        
        message_placeholder.markdown(full_response)
    
    # 응답을 대화 기록에 추가
    st.session_state.messages.append({"role": "assistant", "content": full_response})