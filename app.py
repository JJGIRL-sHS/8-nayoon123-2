import streamlit as st
import serial


from datetime import datetime
import json


# =========================================================
# [구역 1] 환경 설정
# =========================================================

st.set_page_config(page_title="8일간의 아두이노", layout="wide")


# =========================================================
# [구역 2] 리소스 및 외부 연결 관리
# =========================================================


@st.cache_resource
def get_ser(port):
    try:
        return serial.Serial(port, 115200, timeout=1)
    except:
        return None

port = st.sidebar.text_input("시리얼 포트", value="COM3")

st.session_state.ser = get_ser(port)

if st.session_state.ser is not None:
    st.sidebar.success(f"{port} 연결 성공!")
else:
    st.sidebar.error(f"{port}를 찾을 수 없습니다.")


# =========================================================
# [구역 3] 상태 초기화
# =========================================================

if "sonar_data" not in st.session_state:
    st.session_state.sonar_data = []

if "current_distance" not in st.session_state:
    st.session_state.current_distance = None

if "threshold" not in st.session_state:
    st.session_state.threshold = 15

# =========================================================
# [구역 4] AI 에이전트 및 도구(Tools) 정의
# =========================================================


# =========================================================
# [구역 5] 데이터 수집
# =========================================================

def fetch_data():
    ser = st.session_state.ser
    while ser and ser.is_open and ser.in_waiting > 0:
        try:
            message = ser.readline().decode("utf-8").strip()
            payload = json.loads(message)

            sensor_type = payload["type"]

            if sensor_type == "sonar":
                distance = payload["distance"]

                if 3 <= distance <= 200:
                    st.session_state.sonar_data.append({
                            "time": datetime.now(),
                            "distance": distance,
                    })

                    st.session_state.current_distance = distance

                    if len(st.session_state.sonar_data) > 200:
                        st.session_state.sonar_data.pop(0)

        except json.JSONDecodeError as e:
            continue
        except Exception as e:
            print(e)

with st.sidebar:
    @st.fragment(run_every="0.3s")
    def collect_data():
        fetch_data()

        if st.session_state.current_distance is None:
            st.info(f"아두이노와 연결 중입니다.")
        else :
            st.info(f"현재 거리: {st.session_state.current_distance}")

    collect_data()

# =========================================================
# [구역 6] 페이지 내비게이션 및 앱 실행
# =========================================================

pages = [
    st.Page("dashboard.py", title="대시보드", icon=":material/dashboard:", default=True),
    st.Page("control.py", title="수동 제어", icon=":material/adjust:"),
]

page = st.navigation(pages=pages)

st.title(f"{page.icon} {page.title}")

page.run()